# Turtlesim Demo Clear Behavior

The "Clear" sub-behavior is implemented by a sequence of states as in the main editor view

<p float="center">
  <img src="img/editor_view.png" alt="State machine editor view" width="45%">
</p>

This discussion presumed you have already read through the ["Home"](home_behavior.md) discussion.

The "Clear" transition first invokes the "ClearLog" [LogState](https://github.com/FlexBE/flexbe_behavior_engine/blob/ros2-devel/flexbe_states/flexbe_states/log_state.py) to display the `"Clear turtlesim window ..."` text, then transitions to the 
"ClearWindow" state instance of the [`ClearTurtlesimState`](../flexbe_turtlesim_demo_flexbe_states/flexbe_turtlesim_demo_flexbe_states/clear_turtlesim_state.py).  After the `ClearTurtlesimState` returns, the system either transitions back to the "Operator" decision state, or
into the "ClearFailed" `LogState` to notify the operator of problems.

The key difference between `ClearTurtlesimState` and the [`TeleportAbsoluteState`](../flexbe_turtlesim_demo_flexbe_states/flexbe_turtlesim_demo_flexbe_states/teleport_absolute_state.py) discussed in "Home" is that `ClearTurtlesimState` uses a *blocking* service call.


```python
    def on_enter(self, userdata):
        """
        Call when the state becomes active.

        This example does NOT use any userdata passed from upstream states.

        , i.e. a transition from another state to this one is taken.
        """
        self._start_time = self._node.get_clock().now()
        self._return = None  # reset the completion flag
        self._srv_result = None
        self._service_called = False
        try:
            if self._srv.is_available(self._srv_topic, wait_duration=0.0):
                Logger.localinfo(f"{self._name}: Service {self._srv_topic} is available ...")
                self._do_service_call()
            else:
                Logger.logwarn(f"{self._name}: Service {self._srv_topic} is not yet available ...")
        except Exception as exc:
            Logger.logerr(f"{self._name}: Service {self._srv_topic} exception {type(exc)} - {str(exc)}")

    def _do_service_call(self):
        """Make the service call using synchronous blocking call."""
        try:
            Logger.localinfo(f"{self._name}: Calling service {self._srv_topic} ...")
            self._service_called = True
            self._srv_result = self._srv.call(self._srv_topic, self._srv_request, wait_duration=0.0)
        except Exception as e:
            Logger.logerr(f"{self._name}: Service {self._srv_topic} exception {type(e)} - {str(e)}")
            self._srv_result = None
```

Use of blocking calls are discouraged with FlexBE and in most cases you should prefer the asynchronous model.

The typical state machine model assumes that `on_enter`, `execute`, and `on_exit` calls are relatively fast compared to the
desired update rate of the system.  This is especially important if the state can be embedded into a `ConcurrencyContainer` (discussed in [Examples](examples.md)).

That said, blocking calls are possible as demonstrated here, and can be appropriate in some instances.
Just beware that this impacts the timing of all other states as the state machine is executed in a single thread, even for *concurrent* containers.

----

This example has demonstrated using an blocking synchronous service call within FlexBE.
For comparison with a non-blocking asynchronous service call, see the ["Home"](home_behavior.md) discussion.

[Back to the overview](quickstart_details.md#selectable-transitions)

