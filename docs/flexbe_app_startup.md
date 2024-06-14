
## Directions for staring with the classic FlexBE App

## FlexBE App Installation

The classic [FlexBE App](https://github.com/flexbe/flexbe_app/tree/ros2-devel) can be used as well.

If building the FlexBE App from source, you must download and install the required `nwjs` binaries
*before* you can run the FlexBE App:

`ros2 run flexbe_app nwjs_install`

  > Note: These are installed in the `install` folder.  If the `install` folder is deleted, then the `nwjs` binaries
  will need to be reinstalled with this script.

## FlexBE App Start Up

Start the FlexBE system using either

`ros2 launch flexbe_app flexbe_full.launch.py use_sim_time:=False`

or the individual components

  `ros2 launch flexbe_onboard behavior_onboard.launch.py use_sim_time:=False`

  `ros2 run flexbe_mirror behavior_mirror_sm --ros-args --remap __node:="behavior_mirror" -p use_sim_time:=False`

  `ros2 run flexbe_app run_app --ros-args --remap name:="flexbe_app" -p use_sim_time:=False`

  `ros2 run flexbe_widget be_launcher --ros-args --remap name:="behavior_launcher" -p use_sim_time:=False`

Afterwards, the basic directions are the same for `flexbe_webui`.

