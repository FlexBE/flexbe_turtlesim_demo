# FlexBE Introductory Examples

In addition to the basic TurtleSim quickstart demo, this
repo includes several example behaviors to illustrate key
FlexBE capabilities.

You are free to jump into any example, but they are designed to
get progressively more complex and take advantage of earlier
behaviors.

Each example requires the FlexBE onboard and OCS to be running.
The quickest way to start the full FlexBE suite (FlexBE WebUI v4.1+):

```bash
ros2 launch flexbe_webui flexbe_full.launch.py
```

> Note: TurtleSim does **not** publish a `/clock` topic, so `use_sim_time` must remain `False` (the default).
> Do **not** pass `use_sim_time:=True`.

See [Detailed Startup Options](quickstart_details.md) for separate onboard/OCS launches
and headless server options.

* [Example 1](example1.md) - Basic FlexBE state implementations
* [Example 2](example2.md) - Basic state machine
* [Example 3](example3.md) - A HFSM behavior with concurrent states
* [Example 4](example4.md) - Behavior composition - using behaviors in other behaviors (a 3-layer HFSM)
* [Example 5](example5.md) - Priority containers
