# Example 5 - Priority Containers

A `PriorityContainer` works inside a `ConcurrencyContainer` to claim exclusive execution priority
over all sibling states while it is active.
This example builds on [Example 3](example3.md) (ConcurrencyContainer) and demonstrates the key
behavioral difference that a `PriorityContainer` introduces.

---

## What is a PriorityContainer?

In a standard `ConcurrencyContainer`, **all** contained states execute every tic — each call to
`execute()` on the container triggers `execute()` on every child state.

A `PriorityContainer` is a subclass of `OperatableStateMachine` that, while active, sets a global
`PriorityContainer.active_container` flag to its own path.
The `ConcurrencyContainer` checks this flag each tic and **skips** any sibling state whose path
does not start with the active container's path.
Skipped states have `_notify_skipped()` called instead of `execute()`.

When the `PriorityContainer` finishes (returns an outcome), it restores the previous
`active_container` value, and sibling states resume normal execution the following tic.

---

## Key Behavioral Properties

### 1. on_enter is deferred for skipped states

The `ConcurrencyContainer` sets `_entering = True` for **all** states when it enters.
Each state's `on_enter()` is only called the first time its `execute()` is called with `_entering = True`.
Because skipped states never have `execute()` called, their `on_enter()` — and therefore
any timer or resource setup done there — is deferred until the `PriorityContainer` finishes.

In this example, `Normal_Work.on_enter()` is not called until `Priority_Work` completes.
`Normal_Work`'s timer does not start counting until that point.

### 2. Priority_Work must be added first

The `ConcurrencyContainer` iterates its states in insertion order each tic.
`Priority_Work` must be added **before** `Normal_Work` so that it sets `active_container`
on the very first tic.
If `Normal_Work` were added first, it would execute once before priority is claimed.

### 3. The ConcurrencyContainer uses an AND exit condition

Both `Priority_Work` and `Normal_Work` must complete before the container exits.
This is the same AND pattern used in [Example 3](example3.md)'s `Container_AND`.

```python
conditions=[('finished', [('Priority_Work', 'done'), ('Normal_Work', 'done')]),
            ('failed',   [('Priority_Work', 'failed')]),
            ('failed',   [('Normal_Work', 'failed')])]
```

This is structurally identical to `Container_AND` in Example 3 — both states must return `done`
before the container exits with `finished`.
Because `Priority_Work` blocks `Normal_Work` from starting, this AND condition effectively
enforces sequential execution: `Priority_Work` completes first, then `Normal_Work` runs to completion,
then the container exits. Neither state completing alone is enough to exit with `finished`.

---

## Behavior Structure

```
_state_machine (OperatableStateMachine)
├── Start (LogState)
│     done → Concurrent_Priority
│
├── Concurrent_Priority (ConcurrencyContainer)
│     exit conditions:
│       finished ← Priority_Work.done AND Normal_Work.done
│       failed   ← Priority_Work.failed
│       failed   ← Normal_Work.failed
│     │
│     ├── Priority_Work (PriorityContainer)  ← added FIRST
│     │     ├── Init_A (ExampleState, waiting_time_priority_a)
│     │     │     done → Init_B
│     │     └── Init_B (ExampleState, waiting_time_priority_b)
│     │           done → done
│     │
│     └── Normal_Work (ExampleState, waiting_time_normal)
│           (on_enter deferred until Priority_Work completes)
│
├── Done (LogState)   → finished
└── Failed (LogState) → failed
```

---

## Execution Walkthrough

With default parameters (`waiting_time_priority_a=1.0`, `waiting_time_priority_b=1.0`,
`waiting_time_normal=5.0`):

| Time (approx.) | Event |
|----------------|-------|
| t=0 s          | Behavior starts; `Start` logs and transitions to `Concurrent_Priority` |
| t=0 s          | `Concurrent_Priority` enters; all states get `_entering=True`; `Priority_Work.on_enter()` called |
| t=0 – 1 s      | `Priority_Work` active; `Init_A` runs; `Normal_Work` is skipped every tic |
| t=1 s          | `Init_A` returns `done`; `Priority_Work` transitions to `Init_B` |
| t=1 – 2 s      | `Init_B` runs; `Normal_Work` still skipped |
| t=2 s          | `Init_B` returns `done`; `Priority_Work` returns `done`; `active_container` cleared |
| t=2 s          | `Normal_Work.on_enter()` called **now** (first tic it is not skipped); timer starts |
| t=2 – 7 s      | `Normal_Work` executes normally for 5 seconds |
| t=7 s          | `Normal_Work` returns `done`; AND condition `('finished', [('Priority_Work', 'done'), ('Normal_Work', 'done')])` now fully met (Priority_Work completed at t=2 s) |
| t=7 s          | `Concurrent_Priority` exits `finished`; `Done` logs; behavior ends |

Total elapsed time ≈ `waiting_time_priority_a + waiting_time_priority_b + waiting_time_normal`.

Compare this to a plain `ConcurrencyContainer` where both states would start simultaneously:
`Normal_Work` would enter and begin its 5-second timer at t=0, finishing at t=5 s.
The `PriorityContainer` adds the priority sequence time before `Normal_Work` begins.

---

## Code Highlights

### PriorityContainer setup (inside ConcurrencyContainer)

```python
_sm_priority_work_0 = PriorityContainer(outcomes=['done', 'failed'])

with _sm_priority_work_0:
    OperatableStateMachine.add('Init_A',
                               ExampleState(target_time=self.waiting_time_priority_a),
                               transitions={'done': 'Init_B', 'failed': 'failed'},
                               autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

    OperatableStateMachine.add('Init_B',
                               ExampleState(target_time=self.waiting_time_priority_b),
                               transitions={'done': 'done', 'failed': 'failed'},
                               autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})
```

`PriorityContainer` is used exactly like `OperatableStateMachine` internally — states are added
sequentially and it executes them in order.

### Adding states to ConcurrencyContainer (order matters!)

```python
_sm_concurrent_priority_1 = ConcurrencyContainer(outcomes=['finished', 'failed'],
                                                  conditions=[('finished', [('Priority_Work', 'done'), ('Normal_Work', 'done')]),
                                                              ('failed', [('Priority_Work', 'failed')]),
                                                              ('failed', [('Normal_Work', 'failed')])
                                                              ])

with _sm_concurrent_priority_1:
    # Priority_Work MUST be added first to claim active_container on tic 1
    OperatableStateMachine.add('Priority_Work',
                               _sm_priority_work_0,
                               transitions={'done': 'finished', 'failed': 'failed'},
                               autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

    # Normal_Work added second; its on_enter is deferred until Priority_Work completes
    OperatableStateMachine.add('Normal_Work', ExampleState(...),
                               transitions={'done': 'finished', 'failed': 'failed'},
                               autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})
```

---

## Running Example 5

Start the FlexBE system (FlexBE WebUI v4.1+):

```bash
ros2 launch flexbe_webui flexbe_full.launch.py
```

> Note: TurtleSim does **not** publish a `/clock` topic, so keep `use_sim_time` at its default `False`.

Then load `Example 5` from the *Behavior Dashboard* and start it from *Runtime Control*.

Alternatively, run in fully autonomous mode without the OCS:

```bash
ros2 run flexbe_widget be_launcher -b "Example 5" \
    --ros-args --remap __node:="behavior_launcher"
```

To observe the deferred `on_enter` clearly, watch the terminal logs:
`Normal_Work`'s `on_enter` log line will not appear until approximately
`waiting_time_priority_a + waiting_time_priority_b` seconds after the behavior starts.

[Back to the overview](examples.md)
