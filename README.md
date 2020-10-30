**This is a standalone package for the Teleportation environment that is part of [SciGym](https://github.com/hendrikpn/scigym). In general I would recommend just using it via scigym instead.**

### Teleportation

The task in this environment is for the agent to find a protocol that uses an already distributed entangled state to teleport an arbitrary quantum state, i.e. the agent should learn to reconstruct the well-known quantum teleportation protocol when provided with a universal gate set and quantum measurements.

An earlier version of this environment has been used in
> Machine learning for long-distance quantum communication  
> Julius Wallnöfer, Alexey A. Melnikov, Wolfgang Dür, Hans J. Briegel  
> [arXiv:1904.10797v1 \[quant-ph\]](https://arxiv.org/abs/1904.10797v1)  

**Initializing the environment**
```python
import scigym
env = scigym.make("teleportation-v0")
```

#### Environment description

The agent is presented with the following situation:

<img src="https://user-images.githubusercontent.com/33934646/62476416-3ea60580-b7a7-11e9-9ee2-7bd6d79ce4dd.png" width="200">

where the input qubit is an arbitrary state Ψ.

*Available actions:*

* T gate T = diag(1, exp(iπ/4)) on each qubit (3 actions)
* Hadamard gate H on each qubit (3 actions)
* CNOT-gate on the two qubits at location A (1 actions)
* Z-measurements on each qubit (3 actions)

In total: **10 actions**

The Z-measurements are considered to be destructive, i.e. the qubit is removed and actions acting on that qubit are no longer valid (and will not change the state).
If the agent can handle changing action sets, the currently available actions can be accessed via the attribute `env.available_actions` or the info dictionary returned by the `env.step(action)` method.

*Observations*

The observations perceived by the agent are a list of previous actions and measurement outcomes. Invalid actions (on qubits that have already been measured) are not added to this list.

*Reward*

If qubit B is in state Ψ, the protocol is considered successful and the agent receives a reward of 1.


#### Known solution

The quantum teleportation protocol in this formulation is performed by:

1. Hadamard on qubit A'
2. CNOT with qubit A' as the source and qubit A as the target
3. Measure qubit A'
4. Measure qubit A

Then, depending on the measurement outcome, a correction needs to be applied on qubit B. This is (equally likely):
* Nothing
* Pauli-Z correction: T^4
* Pauli-X correction: H T^4 H
* Pauli-Y correction: T^4 H T^4 H (up to global phase)

So, depending on the measure outcome, the favored solution will either need
4, 8, 10 or 14 actions.

In order to have discovered a functioning protocol, the agent should find all those solutions, i.e. it should always be successful regardless of the measurement outcomes.

#### Implementation details

In order to make sure that the solution does not depend on the input state,
we compare the Jamiolkowski fidelity of the effective channel generated by the
gate sequence picked by the agent with the ideal channel. We do this by
initializing the qubit A' in a state where it is entangled with an
auxiliary qubit in a maximally entangled state Φ<sup>+</sup>.

*Careful:* Because the environment will return `done` as `True` once no valid
actions remain, this can lead to very short, but unrewarded trials.

#### Discussion

In this formulation the quantum protocol is presented to the agent as essentially
a black box. The observations are only the previous actions and measurement
outcomes and the agent has no access to the physical parameters at all.

Furthermore, coming up with the gate sequence when being given the resources is
certainly a very different task from discovering the quantum teleportation
protocol in the first place. Because the entangled state is already given and
the agent does not gain any information about quantum mechanics, it also has
no chance to realize that entanglement is the crucial resource that makes this
protocol possible.

Nevertheless this limited re-discovery of the quantum teleportation protocol is
of interest because it is a good example of having to deal with the inherent
stochastic nature of quantum measurements. Furthermore, the specific structure
found in the solutions (i.e. they all start the same way and only need
modifications depending on measurement outcomes) lends itself very well to
reinforcement learning as randomly finding the solution needing no correction
operations will lead to easier discovery of the other solutions as the
size of the remaining action space that needs to be explored is drastically
reduced.
