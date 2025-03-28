## FlexBE WebUI Startup

There are 3 approaches to launching the full FlexBE suite for operator supervised autonomy-based control.
Use one (and only one) of the following approaches:

#### 1) FlexBE Quickstart

`ros2 launch flexbe_webui flexbe_full.launch.py use_sim_time:=False`

  This starts all of FlexBE including both the *OCS* and *Onboard* software in one terminal.

#### 2) Launch the *OCS* and *Onboard* separately:

`ros2 launch flexbe_onboard behavior_onboard.launch.py use_sim_time:=False`

`ros2 launch flexbe_webui flexbe_ocs.launch.py use_sim_time:=False`

  The `flexbe_ocs.launch.py` launches several nodes, along with the `webui_client` user interface.

  The seperate launches allows running the *Onboard* software *on board* the robot, and the *OCS* software
  on a separate machine to allow remote supervision.
  However, you can easily run this TurtleSim demonstration on one machine in three terminals.

#### 3) Launch each FlexBE component in separate terminals:

##### *Onboard*

`ros2 launch flexbe_onboard behavior_onboard.launch.py use_sim_time:=False`
  * This runs onboard and executes the HFSM behavior

##### *OCS*

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
    * If the `webui_client` is blank, you may invoke software rendering using the `--qt_software` option
  * `python3 -m webbrowser -n http://127.0.0.1:8000`
      * Browser-based user interface
  * Use `http://127.0.0.1:8000` in your browser window


You may also run `ros2 launch flexbe_webui flexbe_ocs.launch.py headless:=true use_sim_time:=False`
to launch the `flexbe_mirror`, `be_launcher`, and `webui_node` at one time, and then
run the UI in a seperately (e.g. `ros2 run flexbe_webui webui_client`).

This is our standard mode for testing.
