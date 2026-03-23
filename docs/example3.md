# Example 3 - Hierarchical Finite State Machines (HFSM) with ConcurrencyContainers

The `Example 3` behavior constructs a HFSM with a [`ConcurrencyContainer`](https://github.com/FlexBE/flexbe_behavior_engine/blob/ros2-devel/flexbe_core/flexbe_core/core/concurrency_container.py).


After starting the FlexBE system, including both the FlexBE onboard and OCS, as
described in [Detailed Startup Options](quickstart_details.md).

Load the `Example 3`
behavior from the FlexBE UI dashboard.  The leftmost image below shows the
configuration dashboard after loading, and the right image shows the top-level state machine with the
`ConcurrencyContainer`s shown.  Click on any image to see the high-resolution version.

<p float="center">
  <img src="../img/example3_dashboard.png" alt="Example 3 loaded." width="30%">
  <img src="../img/example3_top_level_sm.png" alt="Example 3 top-level state machine." width="30%">
</p>

In FlexBE there are three types of "containers" which hold other state machines: `StateMachine`, `ConcurrencyContainer`, and `PriorityContainer`.  In this example, we will use a `ConcurrencyContainer` as shown in the right hand image above.
`ConcurrencyContainers` execute all of their sub-states on the same FlexBE "tic" of the execute cycle, but they do not execute in actual concurrent time or in true "parallel" fashion.  Interconnections are not allowed within a concurrent container; however, a `ConcurrencyContainer` may contain other containers with more complex state machines as individual hierarchical states.

In Example 3, the top-level state machine uses four `LogState` states named `Start`, `EnterAnd`, `Done`, and `Failed`.
The `Start` and `Done` states use the private configuration variables for their messages, while `EnterAnd` and `Failed` define strings
in their state property edit boxes.  The `WaitState` instance named `Delay` uses a `1.0` second wait time parameter.
Single clicking on either of the `Concurrent` containers (the state implementation is a `ConcurrencyContainer`, but the label says `Concurrent`), will open up their state property editor pane as shown in the leftmost image below.
The property pane for `ConcurrencyContainer`s allows one to specify the specific outcomes that are allowed, and to configure `userdata` key names for the container.

From the property pane you can select "Open this container", or you may directly open by
double clicking on the `Concurrent`  container box in the state machine.  The open container view shows the state machines under the top-level in the HFSM.  The two (sub-)state machines are shown below.

<p float="center">
  <img src="../img/example3_concurrent_or_property.png" alt="Example 3 Concurrent OR container properties." width="30%">
  <img src="../img/example3_concurrent_or.png" alt="Example 3 Concurrent OR state machine." width="30%">
  <img src="../img/example3_concurrent_and.png" alt="Example 3 Concurrent AND state machine." width="30%">
</p>

As shown above in the leftmost image, the `Concurrent_OR` container has two instances of the `ExampleState` labeled `A` and `B`.
The container outcomes are connected separately so that either `A` or `B` returning `done` will cause the container to return `finished`.

As shown above in the rightmost image, the `Concurrent_AND` container has two instances of the `ExampleState` labeled `C` and `D`.
Both of the `done` outcomes from `C` and `D` are connected to a single container `finished` outcome; thus, both `C` and `D` must return
`done` before the container returns `finished` (i.e., `finished` if both `C` *and* `D` are `done`); any `failed` outcome will cause the container to return `failed` (i.e., failed if `C` *or* `D` fails).

The "Runtime Control" panel allows the operator to adjust the wait times as shown in the leftmost image below.  For this example, `waiting_time_a` is set to `4.0` seconds, and `waiting_time_b` is set to `2.0` seconds.  Thus, state `B` will return `done` first, which will preempt state `A` after approximately 2.0 seconds.  Likewise, `waiting_time_c` is set to `4.0` seconds, and `waiting_time_d_` is set to `2.0` seconds.  State `D` will finish execution and call `on_exit` after approximately 2 seconds, but state `C` will continue to execute for another 2 seconds.

<p float="center">
  <img src="../img/example3_runtime.png" alt="Example 3 runtime start configuration." width="30%">
  <img src="../img/example3_start.png" alt="Example 3 awaiting manual transition after Start." width="30%">
  <img src="../img/example3_or_progress.png" alt="Example 3 Concurrent_OR in progress." width="30%">
</p>

The onboard terminal logging includes the `Logger.localinfo` from `execute` method, and shows the alternating "concurrent"
tics until one state in the concurrent container executes.  Then the behavior depends on how the outputs are connected.
The leftmost image below shows the behavior of the `Concurrent_OR` container, and the rightmost image shows the behavior
of the `Concurrent_AND` container given the respective 4.0 and 2.0 second wait times for this example.

<p float="center">
  <img src="../img/example3_onboard_or.png" alt="Example 3 onboard terminal logging during Concurrent_OR" width="45%">
  <img src="../img/example3_onboard_and.png" alt="Example 3 onboard terminal logging during Concurrent_AND." width="45%">
</p>

Try running the behavior at varying autonomy levels.

Now, let us look at the behavior state machine implementation code a bit more.
This behavior is defined in [`example_3_sm.py`](../flexbe_turtlesim_demo_flexbe_behaviors/flexbe_turtlesim_demo_flexbe_behaviors/example_3_sm.py).  All of the code (listed below) is generated by the FlexBE UI state machine editor and saved via the dashboard when the behavior was first created (and subsequently modified.)
The file name and class name `Example3SM` are derived from the assigned behavior name `Example 3` from when it is first created.
The behavior implementation class inherits from the [`Behavior` class](https://github.com/FlexBE/flexbe_behavior_engine/blob/ros2-devel/flexbe_core/flexbe_core/behavior.py).

> Note: This links to the source version.  Any edits or changes are saved in the `install` folder.

The operator adjustable parameters are defined and initialized using the `add_parameter` instance method of the `Behavior` class.
Any states used in the instance are initialized with the ROS node instance reference.
These values are communicated with the `/flexbe/request_behavior` message from the OCS UI.
In contrast the private configuration variables are defined locally in the `create` method, and are not communicated from the OCS side.

```python
class Example3SM(Behavior):
    """
    Define Example Concurrent Behavior.

    This is a simple example for a behavior using custom example_state that logs each function in life cycle.

    Here we demonstrate concurrent behaviors with both OR and AND style exit conditions.

    """

    def __init__(self, node):
        super().__init__()
        self.name = 'Example Concurrent Behavior'

        # parameters of this behavior
        self.add_parameter('waiting_time_a', 4.0)
        self.add_parameter('waiting_time_b', 2.0)
        self.add_parameter('waiting_time_c', 4.0)
        self.add_parameter('waiting_time_d', 2.0)

        # references to used behaviors
        OperatableStateMachine.initialize_ros(node)
        ConcurrencyContainer.initialize_ros(node)
        PriorityContainer.initialize_ros(node)
        Logger.initialize(node)
        flexbe_turtlesim_demo_flexbe_states__ExampleState.initialize_ros(node)
        LogState.initialize_ros(node)
        WaitState.initialize_ros(node)
```


The state machine is defined and created using the `create` instance method.
First each container is instantiated, and their substates are added.
Then the top-level state machine is instantiated, and its internal states are added, including
the container state machines, which are themselves state instances.
The state definitions include both the transition target and required autonomy level
(e.g. the `Start` state `done` outcome transitions to `Concurrent_OR`, and
requires `Low` autonomy).
Notice that some states have their package name prepended
(e.g. `flexbe_turtlesim_demo_flexbe_states__ExampleState`);
this occurs automatically if the same state name occurs multiple times in a workspace.

The comment lines with x- and y-coordinates (e.g., `# x: 500 y:78`) are used to record state locations or transition
arc coordinates in the UI state machine editor.  Thus this file serves as both the executable Python script,
and the UI graphics source.


```python
    def create(self):
        start_msg = "Demo started!"
        done_msg = "Demo finished!"
        # x:920 y:78, x:909 y:171
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]

        # [/MANUAL_CREATE]
        # x:500 y:78, x:482 y:226, x:230 y:365, x:475 y:287, x:430 y:365
        _sm_container_and_0 = ConcurrencyContainer(outcomes=['finished', 'failed'], conditions=[
                                        ('finished', [('C', 'done'), ('D', 'done')]),
                                        ('failed', [('C', 'failed')]),
                                        ('failed', [('D', 'failed')])
                                        ])

        with _sm_container_and_0:
            # x:108 y:72
            OperatableStateMachine.add('C',
                                        flexbe_turtlesim_demo_flexbe_states__ExampleState(target_time=self.waiting_time_c),
                                        transitions={'done': 'finished', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

            # x:110 y:173
            OperatableStateMachine.add('D',
                                        flexbe_turtlesim_demo_flexbe_states__ExampleState(target_time=self.waiting_time_d),
                                        transitions={'done': 'finished', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})


        # x:478 y:55, x:469 y:111, x:455 y:259, x:462 y:183, x:448 y:317, x:444 y:365
        _sm_concurrent_or_1 = ConcurrencyContainer(outcomes=['finished', 'failed'], conditions=[
                                        ('finished', [('A', 'done')]),
                                        ('finished', [('B', 'done')]),
                                        ('failed', [('A', 'failed')]),
                                        ('failed', [('B', 'failed')])
                                        ])

        with _sm_concurrent_or_1:
            # x:30 y:40
            OperatableStateMachine.add('A',
                                        flexbe_turtlesim_demo_flexbe_states__ExampleState(target_time=self.waiting_time_a),
                                        transitions={'done': 'finished', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

            # x:30 y:168
            OperatableStateMachine.add('B',
                                        flexbe_turtlesim_demo_flexbe_states__ExampleState(target_time=self.waiting_time_b),
                                        transitions={'done': 'finished', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})


        with _state_machine:
            # x:52 y:78
            OperatableStateMachine.add('Start',
                                        LogState(text=start_msg, severity=Logger.REPORT_HINT),
                                        transitions={'done': 'Concurrent_OR'},
                                        autonomy={'done': Autonomy.Low})

            # x:565 y:166
            OperatableStateMachine.add('Container_AND',
                                        _sm_container_and_0,
                                        transitions={'finished': 'Done', 'failed': 'Failed'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

            # x:273 y:106
            OperatableStateMachine.add('Delay',
                                        WaitState(wait_time=1.0),
                                        transitions={'done': 'EnterAnd'},
                                        autonomy={'done': Autonomy.Off})

            # x:740 y:72
            OperatableStateMachine.add('Done',
                                        LogState(text=done_msg, severity=Logger.REPORT_HINT),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.High})

            # x:424 y:107
            OperatableStateMachine.add('EnterAnd',
                                        LogState(text="Enter the AND Concurrent state ...", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'Container_AND'},
                                        autonomy={'done': Autonomy.Off})

            # x:750 y:301
            OperatableStateMachine.add('Failed',
                                        LogState(text="Failure encountered", severity=Logger.REPORT_ERROR),
                                        transitions={'done': 'failed'},
                                        autonomy={'done': Autonomy.High})

            # x:128 y:201
            OperatableStateMachine.add('Concurrent_OR',
                                        _sm_concurrent_or_1,
                                        transitions={'finished': 'Delay', 'failed': 'Failed'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

        return _state_machine
```

After experimenting with `Example 3`, continue on to [Example 4](example4.md) for a look at our second Hierarchical Finite State Machine (HFSM) that includes this entire `Example 3` behavior as a sub-behavior using a `StateMachine` container.

[Back to the overview](examples.md)
