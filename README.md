# Flexbe Turtlesim-based Demonstration

This repo provides an introduction to the FlexBE Hierarchical Finite State Machine (HFSM) Behavior Engine.
FlexBE includes both an *Onboard* robot control behavior executive and an
Operator Control Station (*OCS*) for supervisory control and *collaborative autonomy*.

This repo provides a self contained introduction to FlexBE with a
"Quick Start" based on the simple 2D ROS Turtlesim [Turtlesim] simulator.
The repo provides all of the flexbe_turtlesim_demo-specific states and behaviors to provide a simple demonstration of FlexBE's capabilities using a minimal number of the ROS  packages.

## Tutorial Examples

In addition to the Turtlesim demonstration presented below, the repo includes several
detailed [Examples](docs/examples.md) states and behaviors to illustrate the use and capabilities of FlexBE.

----

## Installation

In addition to the standard FlexBE [flexbe_app](https://github.com/flexbe/flexbe_app/tree/ros2-devel) and
[flexbe_behavior_engine](https://github.com/flexbe/flexbe_behavior_engine/tree/ros2-devel) packages,
clone this repo into your ROS workspace:

`git clone https://github.com/flexbe/flexbe_turtlesim_demo.git`

Make sure that the branches are consistent (e.g. `git checkout ros2-devel`)
with the FlexBE App and Behavior Engine installations.

Install any required dependencies.

  * `rosdep update`
  * `rosdep install --from-paths src --ignore-src`


Build your workspace:

  `colcon build`

If building the FlexBE App from source, you must download and install the required `nwjs` binaries
*before* you can run the FlexBE App:

`ros2 run flexbe_app nwjs_install`

  > Note: These are installed in the `install` folder.  If the `install` folder is deleted, then the `nwjs` binaries
  will need to be reinstalled with this script.

----

For an in-depth discussion of FlexBE capabilities refer to the [Examples](docs/examples.md).

See the main [FlexBE tutorials] for more information about the history and development of FlexBE, and 
for more information about loading and launching behaviors.

----

## Quick Start Usage

Launch the Turtlesim node, FlexBE UI App, and Flexible Behavior engine

For each command, we assume the ROS environment is set up in the terminal using `setup.bash` after a build.

### Autonomous Control Demonstration

Launch TurtleSim:

`ros2 run  turtlesim turtlesim_node`

> Note: Unlike simulators such as `Gazebo`, `TurtleSim` does NOT
> publish a `\clock` topic to ROS.  Therefore, do NOT set `use_sim_time:=True` with these demonstrations!
> Without a `clock`, nothing gets published and so the system will appear hung; therefore TurtleSim should
> use the real wallclock time.

Start theFlexBE *Onboard* system using

`ros2 launch flexbe_onboard behavior_onboard.launch.py use_sim_time:=False`

Start a demonstration behavior in fully autonomous mode

`ros2 run flexbe_widget be_launcher -b "FlexBE Turtlesim Demo" --ros-args --remap name:="behavior_launcher" -p use_sim_time:=False`

  This will launch the `FlexBE Turtlesim Demo`, which will move the turtle through a series of motions to generate
  a figure 8 pattern in full autonomy mode.  
  This example demonstrates using FlexBE to control a system fully autonomously without operator supervision,
  and serves to verify that the installation is working properly.

<p float="center">
  <img src="img/turtlesim_figure8.png" alt="Turtlesim figure 8 under FlexBE 'FlexBE Turtlesim Demo' behavior." width="35%">
</p>
 > Note: Clicking on any image will give the high resolution view.

 After seeing the system run a few loops, just `Ctrl-C` to end the `behavior_onboard` and `be_launcher` nodes, 
 and move on to the next demonstrations.

----

### FlexBE Collaborative Autonomy Demonstration

A key design goal of the FlexBE is to support "Collaborative Autonomy" where an operator (or team of operators) can supervise and modify behaviors in response to changing conditions.  For more information about collaborative autonomy see [this paper](https://onlinelibrary.wiley.com/doi/full/10.1002/rob.21671)

Ensure that a `turtlesim` node is running and its graphic window is open; if not

`ros2 run  turtlesim turtlesim_node`

There are 3 approaches to launching the full FlexBE suite for operator supervised autonomy-based control.
Use one (and only one) of the following approaches:

#### 1) FlexBE Quickstart

`ros2 launch flexbe_app flexbe_full.launch.py use_sim_time:=False`

  This starts all of FlexBE including both the *OCS* and *Onboard* software in one terminal.

#### 2) Launch the *OCS* and *Onboard* separately:

`ros2 launch flexbe_onboard behavior_onboard.launch.py use_sim_time:=False`

`ros2 launch flexbe_app flexbe_ocs.launch.py use_sim_time:=False`

  This allows running the *Onboard* software *on board* the robot, and the *OCS* software on a separate machine to allow remote supervision.

#### 3) Launch each FlexBE component in separate terminals:

##### *Onboard*

`ros2 launch flexbe_onboard behavior_onboard.launch.py use_sim_time:=False`
  * This runs onboard and executes the HFSM behavior

##### *OCS*

`ros2 run flexbe_mirror behavior_mirror_sm --ros-args --remap __node:="behavior_mirror" -p use_sim_time:=False`
  * This runs on OCS computer, listens to `'flexbe/mirror/outcome'` topic to follow the state-to-state transitions.
    This allows the OCS to "mirror" what is happening onboard the robot

`ros2 run flexbe_app run_app --ros-args --remap name:="flexbe_app" -p use_sim_time:=False`
  * This launches the FlexBE user interface

`ros2 run flexbe_widget be_launcher --ros-args --remap name:="behavior_launcher" -p use_sim_time:=False`
  * This node listens to the UI and sends behavior structures and start requests to onboard 
  * This can also be used separately from UI to launch behavior either on start up or by sending requests

The *OCS* components can be run on a separate computer from the *onboard* components.

After starting the system using one of these three approaches, the primary interaction is through the FlexBE UI, although
you may monitor the terminals to see the confirming messages that are posted during operation.

#### Optional Operator Input

Some of the (sub-)behaviors below request operator input.  For this we provide a simple pop-up dialog window 
as part of the `flexbe_input` package in the `flexbe_behavior_engine` repository.

To use this operator input feature, run the [`input_action_server`](https://github.com/FlexBE/flexbe_behavior_engine/blob/ros2-devel/flexbe_input/flexbe_input/input_action_server.py) on the OCS computer:

`ros2 run flexbe_input input_action_server`

This interacts with the [`InputState`](https://github.com/FlexBE/flexbe_behavior_engine/blob/ros2-devel/flexbe_states/flexbe_states/input_state.py).  This simple `input_action_server` demonstration is intended to provide basic functionality for limited 
primitive inputs such as numbers or `list`/`tuple`s of numbers.

See [Complex Data Input](docs/complex_data_input.md) for more information about the `InputState` usage.

> Note: The `InputState` makes use of the `pickle` module, and is subject to this warning from the Pickle manual:

>   Warning The pickle module is not secure against erroneous or maliciously constructed data. 
>   Never unpickle data received from an untrusted or unauthenticated source.

If using the `InputState` it is up to the user to protect their network from untrusted data.

### Controlling Behaviors Via FlexBE User Interface (UI)

Using the FlexBE UI application *Behavior Dashboard*, select *Load Behavior* from the upper middle tool bar, and
select the `flexbe_turtlesim_demo_flexbe_behaviors` package from the dropdown menu and the `FlexBE Turtlesim Demo` behavior.

> Note: Here we use the term "behavior" to mean the state machine that induces a desired system behavior. We will use the term "state" 
> to refer to a particular parameterized instance of a python class that defines the "state implementation".

<p float="center">
  <img src="img/loading_behavior.png" alt="Loading behavior via FlexBE UI Dashboard" width="30%">
  <img src="img/behavior_dashboard.png" alt="Behavior dashboard view" width="30%">
  <img src="img/editor_view.png" alt="State machine editor view" width="30%">
</p>
Once loaded, the behavior dashboard (middle image) is used to configure variables and inputs to the behavior as a whole.
In this example we specify the topic for the turtle command velocity and the location of the "home" position for our turtle.

The *Statemachine Editor* tab is used to inspect or edit existing behaviors, or to build new behaviors.
The `FlexBE Turtlesim Demo` behavior is shown above in the rightmost image.  
FlexBE supports Hierarchical Finite State Machines (HFSM) so that the "EightMove" state is actually a "container" for
 a simple state machine that executes the figure 8 pattern using the provided FlexBE state implementations, and "Turtlesim Input State Behavior" is a container for another entire behavior.  This allows users to define complex behaviors using composition of other behaviors 
 as a HFSM.

The `flexbe_turtlesim_demo_flexbe_states` package in this repository includes custom Python-based state implementations for:

  * [`clear_turtlesim_state`](flexbe_turtlesim_demo_flexbe_states/flexbe_turtlesim_demo_flexbe_states/clear_turtlesim_state.py) - clear the turtlesim window using a *blocking* service call
  * [`rotate_turtle_state`](flexbe_turtlesim_demo_flexbe_states/flexbe_turtlesim_demo_flexbe_states/rotate_turtle_state.py) - Rotate turtle to user input angle using an `action` interface
  * [`teleport_absolute_state`](flexbe_turtlesim_demo_flexbe_states/flexbe_turtlesim_demo_flexbe_states/teleport_absolute_state.py) - go to designated position using a *non-blocking* service call
  * [`timed_cmd_vel_state`](flexbe_turtlesim_demo_flexbe_states/flexbe_turtlesim_demo_flexbe_states/timed_cmd_vel_state.py) - publish command velocity using a specified desired update rate

    > NOTE: The desired state update rate is only best effort.  FlexBE is NOT a real time controller, and
    > is generally suited for lower rate (10s to 100s of Hz) periodic monitoring that does not require precise timing.

For example, the [`timed_cmd_vel_state`](flexbe_turtlesim_demo_flexbe_states/flexbe_turtlesim_demo_flexbe_states/timed_cmd_vel_state.py) 
implements the `TimeCmdVelState` that publishes a fixed command velocity as a [Twist](https://docs.ros2.org/latest/api/geometry_msgs/msg/TwistStamped.html) (forward speed and turning rate) for a given time duration.  The `FlexBE Turtlesim Demo` behavior includes the `EightMove` sub-state machine container.  Opening that container - either by double clicking on container or single clicking and requesting to open the container - shows five state instances of the `TimedCmdVelState`.  The specific parameters values are set in the FlexBE Editor by clicking on a particular state; the "EightMove" state machine with specific "LeftTurn" state values are shown below.

<p float="center">
  <img src="img/timed_cmd_vel.png" alt="LeftTurn state parameters within the 'EightMove' state machine container." width="45%">
</p>

Other types of containers are described in the detailed [Examples](docs/examples.md).

----

The *Runtime Control* tab allows the operator to launch behaviors on the onboard system, and monitor their execution.

<p float="center">
  <img src="img/execute_view.png" alt="Ready to launch loaded behavior." width="45%">
  <img src="img/monitoring_view.png" alt="Monitoring running behavior." width="45%">
</p>

Click on the transition oval labeled "Eight" to make one loop in the figure 8 pattern.  
After completion it will bring you back to the *Operator* Decision state.  

From there you can choose

#### Selectable Transitions

* ["Home"](docs/home_behavior.md) to recenter your turtle, or
* ["Clear"](docs/clear_behavior.md) to clear the path trace, or
* ["Eight"](docs/eight_loop.md) to do another loop, or
* ["Rotate"](docs/rotate_behavior.md) to allow operator to input a desired angle and pass using FlexBE `userdata`
* ["Pose"](docs/pose_behavior.md) allow operator to input a desired pose
  * position as ('[x, y]') or pose as ('[x, y, angle_in_radians]')
* "Quit" to complete the statemachine behavior and exit the
runtime control.

Clicking on the transition names above will take you to a page detailing that particular sub-behavior.

FlexBE supports variable autonomy levels, so choosing "Full" autonomy allows the system to automatically choose to
autonomously repeat the "Eight" transition.  As shown below, the other transitions in the `OperatorDecisionState` 
are configured to require "Full" autonomy, but "Eight" only requires "High" autonomy; 
in "Full" autonomy mode this "Eight" transition is selected automatically. 
This was the mode first demonstrated above without the OCS.

<p float="center">
  <img src="img/operator_decision_state.png" alt="Configuring the operator decision state." width="35%">
  <img src="img/full_autonomy_loops.png" alt="Autonomous behavior in Full autonomy." width="45%">
</p>

Read the descriptions linked to each transition and practice executing the different behaviors above.

## Further Examples

Review the detailed [Examples](docs/examples.md) for a more in depth discussion of the theory and implementation of FlexBE.

----

## TODO write ups:

 * Discuss advanced operations such as "Attaching" to a running behavior.
 * FAQ and debugging help.

----

## Publications

Please use the following publications for reference when using FlexBE:

- Philipp Schillinger, Stefan Kohlbrecher, and Oskar von Stryk, ["Human-Robot Collaborative High-Level Control with Application to Rescue Robotics"](http://dx.doi.org/10.1109/ICRA.2016.7487442), IEEE International Conference on Robotics and Automation (ICRA), Stockholm, Sweden, May 2016.

- Joshua Zutell, David C. Conner and Philipp Schillinger, ["ROS 2-Based Flexible Behavior Engine for Flexible Navigation ,"](http://dx.doi.org/10.1109/SoutheastCon48659.2022.9764047), IEEE SouthEastCon, April 2022.

-----

[Turtlesim]:https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim.html
[FlexBE tutorials]:http://flexbe.github.io
