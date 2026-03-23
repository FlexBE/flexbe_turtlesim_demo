# Flexbe Turtlesim-based Demonstration

This repo provides an introduction to the FlexBE Hierarchical Finite State Machine (HFSM) Behavior Engine.
FlexBE includes both an *Onboard* robot control behavior executive and an
Operator Control Station (*OCS*) for supervisory control and *collaborative autonomy*.

This repo provides a self contained introduction to FlexBE with a
"Quick Start" based on the simple 2D ROS Turtlesim [Turtlesim] simulator.
The repo provides all of the flexbe_turtlesim_demo-specific states and behaviors to provide a simple demonstration of FlexBE's capabilities using a minimal number of the ROS  packages.

For a more complete introduction to FlexBE see the [FlexBE Documentation].

## Tutorial Examples

In addition to the Turtlesim demonstration presented below, the repo includes several
detailed [Examples](docs/examples.md) with custom states and behaviors to illustrate the use and capabilities of FlexBE.

----

## Installation

These directions presumes installation of the [flexbe_behavior_engine] for ROS 2 `iron` or later.
You may do so via the binaries using `sudo apt install ros-<DISTRO>-flexbe-behavior-engine` or
from source at [flexbe_behavior_engine].

Additionally you need the user interface (UI).  These directions use the [flexbe_webui] v4.1+.

In addition to the basic FlexBE system , clone this repo into your ROS workspace:

`git clone https://github.com/flexbe/flexbe_turtlesim_demo.git`

Make sure that the branches are consistent (e.g. `git checkout ros2-devel`)
with the FlexBE UI and Behavior Engine installations.

Install any required dependencies.

  * `rosdep update`
  * `rosdep install --from-paths src --ignore-src -y`


Build your workspace:

  `colcon build`


----

This page describes the TurtleSim tutorial, for an in-depth discussion of FlexBE capabilities refer to the [Examples](docs/examples.md).

See the main [FlexBE Documentation] for more information about the history and development of FlexBE, and
for more information about loading and launching behaviors.

----

## Quick Start Usage

Launch the Turtlesim node, FlexBE UI (OCS), and onboard Flexible Behavior engine from a terminal screen.

For each command, we assume the ROS environment is set up in each terminal using `setup.bash` after a build.

### Autonomous Control Demonstration

Launch TurtleSim:

`ros2 run  turtlesim turtlesim_node`

> Note: Unlike simulators such as `Gazebo`, `TurtleSim` does NOT
> publish a `\clock` topic to ROS.  Therefore, do NOT set `use_sim_time:=True` with these demonstrations!
> Without a `clock`, nothing gets published and so the system will appear hung; therefore TurtleSim should
> use the real wallclock time.

Start the FlexBE *Onboard* system using

`ros2 launch flexbe_onboard behavior_onboard.launch.py use_sim_time:=False`

Start a demonstration behavior in fully autonomous mode

`ros2 run flexbe_widget be_launcher -b "FlexBE Turtlesim Demo" --ros-args --remap name:="behavior_launcher" -p use_sim_time:=False`

  This will launch the `FlexBE Turtlesim Demo` behavior, which will move the turtle through a series of motions to generate
  a figure 8 pattern in full autonomy mode.
  This example demonstrates using FlexBE to control a system in "full autonomy" without operator supervision,
  and serves to verify that the installation is working properly.

<p float="center">
  <img src="img/turtlesim_figure8.png" alt="Turtlesim figure 8 under FlexBE 'FlexBE Turtlesim Demo' behavior." width="35%">
</p>

 > Note: Clicking on any image in these examples will give the high resolution view.  These images are taken from the FlexBE App,
 > but are still relevant to the FlexBE WebUI.

 After seeing the system run a few loops, we will attach the OCS to this running behavior to
 observe and interact with it from the UI before transitioning to collaborative operator control.

Since `be_launcher` is already running, start only the mirror and web server — do **not** use
`flexbe_ocs.launch.py` here, as that would start a second `be_launcher`:

```
ros2 run flexbe_mirror behavior_mirror_sm --ros-args --remap __node:="behavior_mirror" -p use_sim_time:=False
```

Then open the UI:

```
ros2 run flexbe_webui webui_node
```

If you experience GPU/rendering issues, run `webui_node` in headless mode:

```
ros2 run flexbe_webui webui_node --ros-args -p headless:=True
```

and open the UI client (recommended) in a separate terminal:
```
ros2 run flexbe_webui webui_client
```

Optionally, you can run the UI client in a browser:
```
python3 -m webbrowser -n http://127.0.0.1:8000
```

In the FlexBE UI, the *Runtime Control* tab will show an **"External Behavior Running"** panel because
the behavior was started by `be_launcher` rather than the OCS.
Load the `FlexBE Turtlesim Demo` behavior from the *Behavior Dashboard*, then click **Attach** in the
*Runtime Control* tab.  The OCS will sync with the running behavior and you can monitor execution and
issue operator confirmations just as if you had started the behavior from the UI as described in the [Detailed Startup Options](docs/quickstart_details.md).

The behavior starts in `Full` autonomy, you can use the runtime view to drop to `Low` autonomy,
which will pause the behavior at the end of a
figure 8. Click on a transition label to select that transition.

> Note: For `Pose` or `Rotate` transitions, you will need to also open a separate terminal and start the input action server:

```
ros2 run flexbe_input input_action_server
```

After watching a few loops, and experimenting
with the UI,  `Ctrl-C` to end all nodes
(`turtlesim_node`, `behavior_onboard`, `be_launcher`, `behavior_mirror`, and `webui_node`),
then move on to the complete demonstration in [Detailed Startup Options](docs/quickstart_details.md).


----

### FlexBE Collaborative Autonomy Demonstration

A key design goal of FlexBE is to support "Collaborative Autonomy" where an operator (or team of operators)
can supervise and modify behaviors in response to changing conditions.
For more information about collaborative autonomy see [this paper](https://onlinelibrary.wiley.com/doi/full/10.1002/rob.21671).


See [Detailed Startup Options](docs/quickstart_details.md) for alternative ways to launch the OCS and
Onboard components separately (e.g. onboard on the robot, OCS on a remote machine), headless server
options, instructions on the optional operator input server used by the
["Rotate"](docs/rotate_behavior.md) and ["Pose"](docs/pose_behavior.md) behaviors, and a complete
walkthrough of the UI, state machine editor, and all selectable transitions.

> Note: These directions use the newer FlexBE WebUI v4.1+.

## Further Examples

Review the detailed [Examples](docs/examples.md) for a more in depth discussion of the theory and implementation of FlexBE.

----

## Publications

Please use the following publications for reference when using FlexBE:

- Philipp Schillinger, Stefan Kohlbrecher, and Oskar von Stryk, ["Human-Robot Collaborative High-Level Control with Application to Rescue Robotics"](http://dx.doi.org/10.1109/ICRA.2016.7487442), IEEE International Conference on Robotics and Automation (ICRA), Stockholm, Sweden, May 2016.

- Joshua Zutell, David C. Conner and Philipp Schillinger, ["ROS 2-Based Flexible Behavior Engine for Flexible Navigation ,"](http://dx.doi.org/10.1109/SoutheastCon48659.2022.9764047), IEEE SouthEastCon, April 2022.

- Samuel Raymond, Grace Walters, Joshua Luzier, and David C. Conner, ["Design and Development of the FlexBE WebUI with Introductory Tutorials"](https://dl.acm.org/doi/10.5555/3722479.3722523), Journal of Computing Sciences in Colleges, Volume 40, Issue 3, October 2024.

-----

[Turtlesim]:https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim.html
[FlexBE Documentation]:https://flexbe.readthedocs.io
[flexbe_behavior_engine]:https://github.com/flexbe/flexbe_behavior_engine
[flexbe_webui]:https://github.com/flexbe/flexbe_webui
