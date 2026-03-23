# FlexBE Turtlesim Quick Start — Detailed Instructions

This page provides the detailed startup and usage instructions for the
[FlexBE Turtlesim Quick Start](../README.md).

----

## Launching the FlexBE OCS and Onboard System

Ensure that a `turtlesim` node is running and its graphic window is open; if not, restart using

`ros2 run  turtlesim turtlesim_node`

There are 3 approaches to launching the full FlexBE suite for operator supervised autonomy-based control.
Use one (and only one) of the following approaches:

### 1) FlexBE Quickstart

`ros2 launch flexbe_webui flexbe_full.launch.py use_sim_time:=False`

  This starts all of FlexBE including both the *OCS* and *Onboard* software in one terminal.

### 2) Launch the *OCS* and *Onboard* separately:

`ros2 launch flexbe_onboard behavior_onboard.launch.py use_sim_time:=False`

`ros2 launch flexbe_webui flexbe_ocs.launch.py use_sim_time:=False`

  The `flexbe_ocs.launch.py` launches several nodes, along with the `webui_client` user interface.

  The separate launches allows running the *Onboard* software *on board* the robot, and the *OCS* software
  on a separate machine to allow remote supervision.
  However, you can easily run this TurtleSim demonstration on one machine in three terminals.

### 3) Launch each FlexBE component in separate terminals:

#### *Onboard*

`ros2 launch flexbe_onboard behavior_onboard.launch.py use_sim_time:=False`
  * This runs onboard and executes the HFSM behavior

#### *OCS*

`ros2 run flexbe_mirror behavior_mirror_sm --ros-args --remap __node:="behavior_mirror" -p use_sim_time:=False`
  * This runs on OCS computer, listens to `'flexbe/mirror/outcome'` topic to follow the state-to-state transitions.
    This allows the OCS to "mirror" what is happening onboard the robot

`ros2 run flexbe_widget be_launcher --ros-args --remap name:="behavior_launcher" -p use_sim_time:=False`
  * This node listens to the UI and sends behavior structures and start requests to onboard
  * This can also be used separately from UI to launch behavior either on start up or by sending requests

`ros2 run flexbe_webui webui_node`
   * Operates the web server that coordinates communication with UI

To run the UI, you may choose one (and only one) of either:
  * `ros2 run flexbe_webui webui_client` (Recommended)
  * `python3 -m webbrowser -n http://127.0.0.1:8000`
      * Browser-based user interface
  * Use `http://127.0.0.1:8000` in your browser window

If you experience GPU/rendering issues with the Electron client, run `webui_node` in headless mode
and open the client separately:

```
ros2 run flexbe_webui webui_node --ros-args -p headless:=True
ros2 run flexbe_webui webui_client
```

You may also run `ros2 launch flexbe_webui flexbe_ocs.launch.py headless:=true use_sim_time:=False`
to launch the `flexbe_mirror`, `be_launcher`, and `webui_node` at one time, and then
run the UI separately (e.g. `ros2 run flexbe_webui webui_client`).  This is our standard mode of testing.

After starting the FlexBE system using one of these three approaches, the primary interaction is through the FlexBE UI, although
you may monitor the terminals to see the confirming messages that are posted during operation.

> Note: These directions use the FlexBE WebUI v4.1+.

----

## Optional Operator Input

The ["Rotate"](rotate_behavior.md) and ["Pose"](pose_behavior.md) (sub-)behaviors described below request operator input.

For this we provide a simple pop-up dialog window
as part of the `flexbe_input` package in the `flexbe_behavior_engine` repository.

To use this operator input feature, run the [`input_action_server`](https://github.com/FlexBE/flexbe_behavior_engine/blob/ros2-devel/flexbe_input/flexbe_input/input_action_server.py) on the OCS computer:

`ros2 run flexbe_input input_action_server`

See the discussions linked later for ["Rotate"](rotate_behavior.md) and ["Pose"](pose_behavior.md) for specific usage instructions
and *warnings* therein.

----

## Definitions

Before we get started, let us define some terms:

 * **"behavior"** - a "behavior" in FlexBE is a state machine that induces a desired system behavior.

    This includes simple state machines with one or two basic *states* to more complex state machines created by composing state machines into a *"Hierarchical Finite State Machine (HFSM)"* with state machines themselves being *states* in a higher level state machine.

 * **"state"** - we use *state* in two ways:

   1) we refer to a "state" in our finite state machine as a particular node in the state machine graph (at whatever layer in the hierarchy).  These *states* correspond either: a) instances of the Python state implementations (defined below), b) instances of a "state machine" defined as a collection of the states in a container state, or c) an entire "behavior" state machine included as a state within a higher level behavior. In this usage, a *state* in a high-level *behavior* might be a *state machine* that itself contains other low level *behaviors* made up of their *states*.

   2) we refer to a particular "state implementation" in Python corresponding to a Python class and script; FlexBE uses these *state* implementations to build state machines.  So a "FlexBE state" refers to a class defined in a specific "state implementation" file available to the "behavior" designer.  The classes are instantiated as "states" within a behavior.

----

## Controlling Behaviors Via FlexBE User Interface (UI)

Using the FlexBE UI application *Behavior Dashboard*, select *Load Behavior* from the upper middle tool bar, and
select the `flexbe_turtlesim_demo_flexbe_behaviors` package from the dropdown menu and the `FlexBE Turtlesim Demo` behavior.

<p float="center">
  <img src="../img/loading_behavior.png" alt="Loading behavior via FlexBE UI Dashboard" width="30%">
  <img src="../img/behavior_dashboard.png" alt="Behavior dashboard view" width="30%">
  <img src="../img/editor_view.png" alt="State machine editor view" width="30%">
</p>
Once loaded, the behavior dashboard (middle image) is used to configure variables and inputs to the behavior as a whole.
In this example we specify the topic for the turtle command velocity and the location of the "home" position for our turtle.

The *Statemachine Editor* tab is used to inspect or edit existing behaviors, or to build new behaviors.
The `FlexBE Turtlesim Demo` behavior is shown above in the rightmost image.
FlexBE supports Hierarchical Finite State Machines (HFSM) so that the "EightMove" state is actually a "container" for
 a simple state machine that executes the figure 8 pattern using the provided FlexBE state implementations, and "Turtlesim Input State Behavior" is a container for another entire behavior.  This allows users to define complex behaviors using composition of other behaviors
 as a HFSM.

The [`flexbe_turtlesim_demo_flexbe_states`](../flexbe_turtlesim_demo_flexbe_states) package in this repository
includes custom Python-based state implementations for:

  * [`clear_turtlesim_state`](../flexbe_turtlesim_demo_flexbe_states/flexbe_turtlesim_demo_flexbe_states/clear_turtlesim_state.py) - clear the turtlesim window using a *blocking* service call
  * [`rotate_turtle_state`](../flexbe_turtlesim_demo_flexbe_states/flexbe_turtlesim_demo_flexbe_states/rotate_turtle_state.py) - Rotate turtle to user input angle using an `action` interface
  * [`teleport_absolute_state`](../flexbe_turtlesim_demo_flexbe_states/flexbe_turtlesim_demo_flexbe_states/teleport_absolute_state.py) - go to designated position using a *non-blocking* service call
  * [`timed_cmd_vel_state`](../flexbe_turtlesim_demo_flexbe_states/flexbe_turtlesim_demo_flexbe_states/timed_cmd_vel_state.py) - publish command velocity using a specified desired update rate

    > NOTE: The desired state update rate is only best effort.  FlexBE is NOT a real time controller, and
    > is generally suited for lower rate (10s to 100s of Hz) periodic monitoring that does not require precise timing.

For example, the [`timed_cmd_vel_state`](../flexbe_turtlesim_demo_flexbe_states/flexbe_turtlesim_demo_flexbe_states/timed_cmd_vel_state.py)
implements the `TimeCmdVelState` that publishes a fixed command velocity as a [Twist](https://docs.ros2.org/latest/api/geometry_msgs/msg/TwistStamped.html) (forward speed and turning rate) for a given time duration.  The `FlexBE Turtlesim Demo` behavior includes the `EightMove` sub-state machine container.  Opening that container - either by double clicking on container or single clicking and requesting to open the container - shows five state instances of the `TimedCmdVelState`.  The specific parameters values are set in the FlexBE Editor by clicking on a particular state; the "EightMove" state machine with specific "LeftTurn" state values are shown below.

<p float="center">
  <img src="../img/timed_cmd_vel.png" alt="LeftTurn state parameters within the 'EightMove' state machine container." width="45%">
</p>

Other types of containers are described in the detailed [Examples](examples.md).

----

The *Runtime Control* tab allows the operator to launch behaviors on the onboard system, and monitor their execution.

<p float="center">
  <img src="../img/execute_view.png" alt="Ready to launch loaded behavior." width="45%">
  <img src="../img/monitoring_view.png" alt="Monitoring running behavior." width="45%">
</p>

Click on the transition oval labeled "Eight" to make one loop in the figure 8 pattern.
After completion it will bring you back to the *Operator* Decision state.

From there you can choose from multiple outcomes that transition into different transition paths/behaviors.

### Selectable Transitions

Clicking on the transition names below will take you to a page detailing that particular sub-behavior.

* ["Home"](home_behavior.md) to recenter your turtle
* ["Clear"](clear_behavior.md) to clear the path trace
* ["Eight"](eight_loop.md) to do another loop
* ["Rotate"](rotate_behavior.md) to allow operator to input a desired angle and pass using FlexBE `userdata`
* ["Pose"](pose_behavior.md) allow operator to input a desired pose
  * position as ('[x, y]') or pose as ('[x, y, angle_in_radians]')
* "Quit" to complete the state machine behavior and exit the runtime control.

FlexBE supports variable autonomy levels, so choosing "Full" autonomy allows the system to automatically choose to
autonomously repeat the "Eight" transition.  As shown below, the other transitions in the `OperatorDecisionState`
are configured to require "Full" autonomy, but "Eight" only requires "High" autonomy;
in "Full" autonomy mode this suggested "Eight" transition is selected automatically.
This was the mode used in the initial autonomous demonstration started with `be_launcher`.

<p float="center">
  <img src="../img/operator_decision_state.png" alt="Configuring the operator decision state." width="35%">
  <img src="../img/full_autonomy_loops.png" alt="Autonomous behavior in Full autonomy." width="45%">
</p>

Read the descriptions linked to each transition and practice executing the different behaviors above.
