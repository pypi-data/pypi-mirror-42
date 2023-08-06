"""Tests for krotov.Objective in isolation"""
import os
import copy

import numpy as np
import scipy
import qutip
from qutip import tensor, sigmaz, sigmax, sigmam, identity
from itertools import product

import krotov

import pytest


@pytest.fixture
def transmon_ham_and_states(Ec=0.386, EjEc=45, nstates=2, ng=0.0, T=10.0):
    """Transmon Hamiltonian"""
    Ej = EjEc * Ec
    n = np.arange(-nstates, nstates + 1)
    up = np.diag(np.ones(2 * nstates), k=-1)
    do = up.T
    H0 = qutip.Qobj(np.diag(4 * Ec * (n - ng) ** 2) - Ej * (up + do) / 2.0)
    H1 = qutip.Qobj(-2 * np.diag(n))

    eigenvals, eigenvecs = scipy.linalg.eig(H0.full())
    ndx = np.argsort(eigenvals.real)
    E = eigenvals[ndx].real
    V = eigenvecs[:, ndx]
    w01 = E[1] - E[0]  # Transition energy between states

    psi0 = qutip.Qobj(V[:, 0])
    psi1 = qutip.Qobj(V[:, 1])

    profile = lambda t: np.exp(-40.0 * (t / T - 0.5) ** 2)
    eps0 = lambda t, args: 0.5 * profile(t) * np.cos(8 * np.pi * w01 * t)
    return ([H0, [H1, eps0]], psi0, psi1)


def test_krotov_objective_initialization(transmon_ham_and_states):
    """Test basic instantiation of a krotov.Objective with qutip objects"""
    H, psi0, psi1 = transmon_ham_and_states
    obj = krotov.Objective(initial_state=psi0, target=psi1, H=H)
    assert obj.H == H
    assert obj.initial_state == psi0
    assert obj.target == psi1
    assert obj == krotov.Objective(H=H, initial_state=psi0, target=psi1)


def test_objective_copy(transmon_ham_and_states):
    """Test that copy.copy(objective) produces the expected equalities by value
    and by reference"""
    H, psi0, psi1 = transmon_ham_and_states
    c1 = H[1].copy()  # we just need something structurally sound ...
    c2 = H[1].copy()  # ... It doesn't need to make sense physically
    assert c1 == c2  # equal by value
    assert c1 is not c2  # not equal by reference

    target1 = krotov.Objective(
        initial_state=psi0, target=psi1, H=H, c_ops=[c1, c2]
    )
    target2 = copy.copy(target1)
    assert target1 == target2
    assert target1 is not target2
    assert target1.H == target2.H
    assert target1.H is not target2.H
    assert target1.H[0] is target2.H[0]
    assert target1.H[1] is not target2.H[1]
    assert target1.H[1][0] is target2.H[1][0]
    assert target1.H[1][1] is target2.H[1][1]
    assert target1.c_ops[0] == target2.c_ops[0]
    assert target1.c_ops[0] is not target2.c_ops[0]
    assert target1.c_ops[0][0] is target2.c_ops[0][0]
    assert target1.c_ops[0][1] is target2.c_ops[0][1]


def test_adoint_objective(transmon_ham_and_states):
    """Test taking the adjoint of an objective"""
    H, psi0, psi1 = transmon_ham_and_states
    target = krotov.Objective(initial_state=psi0, target=psi1, H=H)
    adjoint_target = target.adjoint
    assert isinstance(adjoint_target.H, list)
    assert isinstance(adjoint_target.H[0], qutip.Qobj)
    assert isinstance(adjoint_target.H[1], list)
    assert isinstance(adjoint_target.H[1][0], qutip.Qobj)
    assert (adjoint_target.H[0] - target.H[0]).norm() < 1e-12
    assert (adjoint_target.H[1][0] - target.H[1][0]).norm() < 1e-12
    assert adjoint_target.H[1][1] == target.H[1][1]
    assert adjoint_target.initial_state.isbra
    assert adjoint_target.target.isbra


def test_adoint_objective_with_no_target(transmon_ham_and_states):
    """Test taking the adjoint of an objective if target is None"""
    H, psi0, _ = transmon_ham_and_states
    target = krotov.Objective(initial_state=psi0, target=None, H=H)
    adjoint_target = target.adjoint
    assert (adjoint_target.H[0] - target.H[0]).norm() < 1e-12
    assert (adjoint_target.H[1][0] - target.H[1][0]).norm() < 1e-12
    assert adjoint_target.H[1][1] == target.H[1][1]
    assert adjoint_target.initial_state.isbra
    assert adjoint_target.target is None


def test_invalid_objective(transmon_ham_and_states):
    """Test that invalid objectives raise a ValueError"""
    H, psi0, psi1 = transmon_ham_and_states
    with pytest.raises(ValueError) as exc_info:
        krotov.Objective(initial_state=psi0.full, target=psi1, H=H)
    assert "Invalid initial_state" in str(exc_info.value)
    with pytest.raises(ValueError) as exc_info:
        krotov.Objective(initial_state=None, target=psi1, H=H)
    assert "Invalid initial_state" in str(exc_info.value)
    with pytest.raises(ValueError) as exc_info:
        krotov.Objective(initial_state=psi0, target=psi1, H=tuple(H))
    assert "Invalid H" in str(exc_info.value)
    with pytest.raises(ValueError) as exc_info:
        krotov.Objective(initial_state=psi0, target=psi1, H=None)
    assert "Invalid H" in str(exc_info.value)
    with pytest.raises(ValueError) as exc_info:
        krotov.Objective(initial_state=psi0, target=psi1, H=H[0].full)
    assert "Invalid H" in str(exc_info.value)
    with pytest.raises(ValueError) as exc_info:
        krotov.Objective(initial_state=psi0, target=psi1, H=H, c_ops=H[0])
    assert "Invalid c_ops" in str(exc_info.value)


@pytest.fixture
def tlist_control(request):
    testdir = os.path.splitext(request.module.__file__)[0]
    tlist, control = np.genfromtxt(
        os.path.join(testdir, 'pulse.dat'), unpack=True
    )
    return tlist, control


def test_objective_mesolve_propagate(transmon_ham_and_states, tlist_control):
    """Test propagation method of objective"""
    tlist, control = tlist_control
    H, psi0, psi1 = transmon_ham_and_states
    H = copy.deepcopy(H)
    T = tlist[-1]
    nt = len(tlist)
    H[1][1] = lambda t, args: (
        0
        if (t > float(T))
        else control[int(round(float(nt - 1) * (t / float(T))))]
    )
    target = krotov.Objective(initial_state=psi0, target=psi1, H=H)

    assert len(tlist) == len(control) > 0

    res1 = target.mesolve(tlist)
    res2 = target.propagate(tlist, propagator=krotov.propagators.expm)
    assert len(res1.states) == len(res2.states) == len(tlist)
    assert (1 - np.abs(res1.states[-1].overlap(res2.states[-1]))) < 1e-4

    P0 = psi0 * psi0.dag()
    P1 = psi1 * psi1.dag()
    e_ops = [P0, P1]

    res1 = target.mesolve(tlist, e_ops=e_ops)
    res2 = target.propagate(
        tlist, e_ops=e_ops, propagator=krotov.propagators.expm
    )

    assert len(res1.states) == len(res2.states) == 0
    assert len(res1.expect) == len(res2.expect) == 2
    assert len(res1.expect[0]) == len(res2.expect[0]) == len(tlist)
    assert len(res1.expect[1]) == len(res2.expect[1]) == len(tlist)
    assert abs(res1.expect[0][-1] - res2.expect[0][-1]) < 1e-2
    assert abs(res1.expect[1][-1] - res2.expect[1][-1]) < 1e-2
    assert abs(res1.expect[0][-1] - 0.1925542) < 1e-7
    assert abs(res1.expect[1][-1] - 0.7595435) < 1e-7


def test_plug_in_array_controls_as_func():
    """Test _plug_in_array_controls_as_func, specifically that it generates a
    function that switches between the points in tlist"""
    nt = 4
    T = 5.0
    u1 = np.random.random(nt)
    u2 = np.random.random(nt)
    H = ['H0', ['H1', u1], ['H2', u2]]
    controls = [u1, u2]
    mapping = [[1], [2]]  # u1  # u2
    tlist = np.linspace(0, T, nt)
    H_with_funcs = krotov.objectives._plug_in_array_controls_as_func(
        H, controls, mapping, tlist
    )
    assert callable(H_with_funcs[1][1])
    assert callable(H_with_funcs[2][1])

    u1_func = H_with_funcs[1][1]
    assert u1_func(T + 0.1, None) == 0
    assert u1_func(T, None) == u1[-1]
    assert u1_func(0, None) == u1[0]
    dt = tlist[1] - tlist[0]
    assert u1_func(tlist[2] + 0.4 * dt, None) == u1[2]
    assert u1_func(tlist[2] + 0.6 * dt, None) == u1[3]

    u2_func = H_with_funcs[2][1]
    assert u2_func(T + 0.1, None) == 0
    assert u2_func(T, None) == u2[-1]
    assert u2_func(0, None) == u2[0]
    dt = tlist[1] - tlist[0]
    assert u2_func(tlist[2] + 0.4 * dt, None) == u2[2]
    assert u2_func(tlist[2] + 0.6 * dt, None) == u2[3]


def test_gate_objectives_shape_error():
    """Test that trying to construct gate objectives with a gate whose shape
    mismatches the basis throws an exception"""
    basis = [qutip.ket([0]), qutip.ket([1])]
    gate = qutip.tensor(qutip.operators.sigmay(), qutip.identity(2))
    H = [
        qutip.operators.sigmaz(),
        [qutip.operators.sigmax(), lambda t, args: 1.0],
    ]
    with pytest.raises(ValueError) as exc_info:
        krotov.objectives.gate_objectives(basis, gate, H)
    assert "same dimension as the number of basis" in str(exc_info.value)


def test_ensemble_objectives(transmon_ham_and_states):
    """Test creation of ensemble objectives"""
    H, psi0, psi1 = transmon_ham_and_states
    objectives = [
        krotov.Objective(initial_state=psi0, target=psi1, H=H),
        krotov.Objective(initial_state=psi1, target=psi0, H=H),
    ]
    (H0, (H1, eps)) = H
    Hs = [[H0, [mu * H1, eps]] for mu in [0.95, 0.99, 1.01, 1.05]]
    ensemble_objectives = krotov.ensemble_objectives(objectives, Hs)
    assert len(ensemble_objectives) == 10
    assert ensemble_objectives[0] == objectives[0]
    assert ensemble_objectives[1] == objectives[1]
    assert (ensemble_objectives[2].H[1][0] - (0.95 * H1)).norm() < 1e-15
    assert (ensemble_objectives[9].H[1][0] - (1.05 * H1)).norm() < 1e-15


def test_gate_objectives_pe():
    """Test gate objectives for a PE optimization"""
    from qutip import ket, tensor, sigmaz, sigmax, identity
    from weylchamber import bell_basis

    basis = [ket(n) for n in [(0, 0), (0, 1), (1, 0), (1, 1)]]
    H = [
        tensor(sigmaz(), identity(2)) + tensor(identity(2), sigmaz()),
        [tensor(sigmax(), identity(2)), lambda t, args: 1.0],
        [tensor(identity(2), sigmax()), lambda t, args: 1.0],
    ]
    objectives = krotov.gate_objectives(basis, 'PE', H)
    assert len(objectives) == 4
    for i in range(4):
        assert objectives[i] == krotov.Objective(
            initial_state=bell_basis(basis)[i], target='PE', H=H
        )
    assert krotov.gate_objectives(basis, 'perfect_entangler', H) == objectives
    assert krotov.gate_objectives(basis, 'perfect entangler', H) == objectives
    assert krotov.gate_objectives(basis, 'Perfect Entangler', H) == objectives
    with pytest.raises(ValueError):
        krotov.gate_objectives(basis, 'prefect(!) entanglers', H)


def test_liouvillian():
    """Test conversion of Hamiltonian/Lindblad operators into a Liouvillian"""
    H = [
        tensor(sigmaz(), identity(2)) + tensor(identity(2), sigmaz()),
        [tensor(sigmax(), identity(2)), lambda t, args: 1.0],
        [tensor(identity(2), sigmax()), lambda t, args: 1.0],
    ]
    c_ops = [tensor(sigmam(), identity(2)), tensor(identity(2), sigmam())]

    assert (
        krotov.objectives.liouvillian(H[0], c_ops)
        - qutip.liouvillian(H[0], c_ops)
    ).norm('max') < 1e-15

    L = krotov.objectives.liouvillian(H, c_ops)
    assert isinstance(L, list)
    assert len(L) == 3
    assert (L[0] - qutip.liouvillian(H[0], c_ops)).norm('max') < 1e-15
    assert (L[1][0] - qutip.liouvillian(H[1][0])).norm('max') < 1e-15
    assert (L[2][0] - qutip.liouvillian(H[2][0])).norm('max') < 1e-15
    assert L[1][1] is H[1][1]
    assert L[2][1] is H[2][1]

    with pytest.raises(ValueError):
        krotov.objectives.liouvillian(tuple(H), c_ops)


@pytest.fixture
def two_qubit_liouvillian():
    H = [
        tensor(sigmaz(), identity(2)) + tensor(identity(2), sigmaz()),
        [tensor(sigmax(), identity(2)), lambda t, args: 1.0],
        [tensor(identity(2), sigmax()), lambda t, args: 1.0],
    ]
    c_ops = [tensor(sigmam(), identity(2)), tensor(identity(2), sigmam())]
    return krotov.objectives.liouvillian(H, c_ops)


def test_gate_objectives_3states(two_qubit_liouvillian):
    """Test the initialization of the "3states" objectives"""
    L = two_qubit_liouvillian
    basis = [qutip.ket(n) for n in [(0, 0), (0, 1), (1, 0), (1, 1)]]
    CNOT = qutip.gates.cnot()
    objectives = krotov.objectives.gate_objectives(
        basis, CNOT, L, liouville_states_set='3states'
    )

    assert len(objectives) == 3

    dims = [[2, 2], [2, 2]]
    rho_1 = qutip.Qobj(np.diag([(0.1 * (4 - i)) for i in range(4)]), dims=dims)
    rho_2 = qutip.Qobj(np.full((4, 4), 1 / 4), dims=dims)
    rho_3 = qutip.Qobj(np.diag([1 / 4, 1 / 4, 1 / 4, 1 / 4]), dims=dims)

    tgt_1 = CNOT * rho_1 * CNOT.dag()
    tgt_2 = CNOT * rho_2 * CNOT.dag()
    tgt_3 = CNOT * rho_3 * CNOT.dag()

    assert (objectives[0].initial_state - rho_1).norm('max') < 1e-14
    assert (objectives[1].initial_state - rho_2).norm('max') < 1e-14
    assert (objectives[2].initial_state - rho_3).norm('max') < 1e-14

    assert (objectives[0].target - tgt_1).norm('max') < 1e-14
    assert (objectives[1].target - tgt_2).norm('max') < 1e-14
    assert (objectives[2].target - tgt_3).norm('max') < 1e-14

    for obj in objectives:
        assert not hasattr(obj, 'weight')

    objectives = krotov.objectives.gate_objectives(
        basis, CNOT, L, liouville_states_set='3states', weights=[1, 0, 2]
    )
    assert len(objectives) == 2
    assert (objectives[0].initial_state - rho_1).norm('max') < 1e-14
    assert (objectives[1].initial_state - rho_3).norm('max') < 1e-14
    for obj in objectives:
        assert isinstance(obj.weight, float)
    assert objectives[0].weight == 1
    assert objectives[1].weight == 2

    with pytest.raises(ValueError):
        krotov.objectives.gate_objectives(
            basis, CNOT, L, liouville_states_set='3states', weights=[1, 2]
        )
    with pytest.raises(ValueError):
        krotov.objectives.gate_objectives(
            basis, CNOT, L, liouville_states_set='3states', weights=[1, 1, -1]
        )


def test_gate_objectives_5states(two_qubit_liouvillian):
    """Test the initialization of the "d + 1" objectives"""
    L = two_qubit_liouvillian
    basis = [qutip.ket(n) for n in [(0, 0), (0, 1), (1, 0), (1, 1)]]
    CNOT = qutip.gates.cnot()
    objectives = krotov.objectives.gate_objectives(
        basis, CNOT, L, liouville_states_set='d+1'
    )

    assert len(objectives) == 5

    rho_1 = basis[0] * basis[0].dag()
    rho_2 = basis[1] * basis[1].dag()
    rho_3 = basis[2] * basis[2].dag()
    rho_4 = basis[3] * basis[3].dag()
    rho_5 = qutip.Qobj(np.full((4, 4), 1 / 4), dims=[[2, 2], [2, 2]])

    tgt_1 = CNOT * rho_1 * CNOT.dag()
    tgt_2 = CNOT * rho_2 * CNOT.dag()
    tgt_3 = CNOT * rho_3 * CNOT.dag()
    tgt_4 = CNOT * rho_4 * CNOT.dag()
    tgt_5 = CNOT * rho_5 * CNOT.dag()

    assert (objectives[0].initial_state - rho_1).norm('max') < 1e-14
    assert (objectives[1].initial_state - rho_2).norm('max') < 1e-14
    assert (objectives[2].initial_state - rho_3).norm('max') < 1e-14
    assert (objectives[3].initial_state - rho_4).norm('max') < 1e-14
    assert (objectives[4].initial_state - rho_5).norm('max') < 1e-14

    assert (objectives[0].target - tgt_1).norm('max') < 1e-14
    assert (objectives[1].target - tgt_2).norm('max') < 1e-14
    assert (objectives[2].target - tgt_3).norm('max') < 1e-14
    assert (objectives[3].target - tgt_4).norm('max') < 1e-14
    assert (objectives[4].target - tgt_5).norm('max') < 1e-14


def test_gate_objectives_16states(two_qubit_liouvillian):
    """Test the initialization of the "full" objectives"""
    L = two_qubit_liouvillian
    basis = [qutip.ket(n) for n in [(0, 0), (0, 1), (1, 0), (1, 1)]]
    CNOT = qutip.gates.cnot()
    objectives = krotov.objectives.gate_objectives(
        basis, CNOT, L, liouville_states_set='full'
    )

    assert len(objectives) == 16

    initial_states = [
        basis[0] * basis[0].dag(),
        basis[0] * basis[1].dag(),
        basis[0] * basis[2].dag(),
        basis[0] * basis[3].dag(),
        basis[1] * basis[0].dag(),
        basis[1] * basis[1].dag(),
        basis[1] * basis[2].dag(),
        basis[1] * basis[3].dag(),
        basis[2] * basis[0].dag(),
        basis[2] * basis[1].dag(),
        basis[2] * basis[2].dag(),
        basis[2] * basis[3].dag(),
        basis[3] * basis[0].dag(),
        basis[3] * basis[1].dag(),
        basis[3] * basis[2].dag(),
        basis[3] * basis[3].dag(),
    ]

    target_states = [CNOT * rho * CNOT.dag() for rho in initial_states]

    for (i, obj) in enumerate(objectives):
        assert (obj.initial_state - initial_states[i]).norm('max') < 1e-14

    for (i, obj) in enumerate(objectives):
        assert (obj.target - target_states[i]).norm('max') < 1e-14


def test_transmon_3states_objectives():
    L = qutip.Qobj()  # dummy Liouvillian (won't be used)
    n_qubit = 3
    ket00 = qutip.ket((0, 0), dim=(n_qubit, n_qubit))
    ket01 = qutip.ket((0, 1), dim=(n_qubit, n_qubit))
    ket10 = qutip.ket((1, 0), dim=(n_qubit, n_qubit))
    ket11 = qutip.ket((1, 1), dim=(n_qubit, n_qubit))
    basis = [ket00, ket01, ket10, ket11]
    weights = [20, 1, 1]
    objectives = krotov.gate_objectives(
        basis,
        qutip.gates.sqrtiswap(),
        L,
        liouville_states_set='3states',
        weights=weights,
    )

    rho1_tgt = (
        0.4 * ket00 * ket00.dag()
        + (0.5 / 2) * ket01 * ket01.dag()
        - (0.1j / 2) * ket01 * ket10.dag()
        + (0.1j / 2) * ket10 * ket01.dag()
        + (0.5 / 2) * ket10 * ket10.dag()
        + 0.1 * ket11 * ket11.dag()
    )

    ket00_tgt = ket00
    ket01_tgt = (ket01 + 1j * ket10) / np.sqrt(2)
    ket10_tgt = (1j * ket01 + ket10) / np.sqrt(2)
    ket11_tgt = ket11
    target_basis = [ket00_tgt, ket01_tgt, ket10_tgt, ket11_tgt]
    rho2_tgt = 0.25 * sum(
        [psi * phi.dag() for (psi, phi) in product(target_basis, target_basis)]
    )

    rho3_tgt = 0.25 * (
        ket00 * ket00.dag()
        + ket01 * ket01.dag()
        + ket10 * ket10.dag()
        + ket11 * ket11.dag()
    )
    assert (objectives[0].target - rho1_tgt).norm('max') < 1e-14
    assert (objectives[1].target - rho2_tgt).norm('max') < 1e-14
    assert (objectives[2].target - rho3_tgt).norm('max') < 1e-14

    assert objectives[0].weight == 60.0 / 22.0
    assert objectives[1].weight == 3.0 / 22.0
    assert objectives[2].weight == 3.0 / 22.0
