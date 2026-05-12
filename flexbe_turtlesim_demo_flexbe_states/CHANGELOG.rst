^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package flexbe_turtlesim_demo_flexbe_states
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

0.0.4 (2026-03-25)
------------------
* Behaviors, manifests, metadata, and tooling cleanup
* State implementation cleanup
* Add conditional turtlesim_msgs dependency for Kilted and later
* Add FlexBE state docstring validation to colcon tests

0.0.3 (2026-03-20)
------------------
* add tests and flake8 cleanup
* Align docs and package metadata with current implementation
* Account for paused time in TimedCmdVelState
* Auto-discover FlexBE state tests for colcon
* Fail TeleportAbsoluteState on invalid pose userdata
* chore: add runtime msg/service/action dependencies to flexbe_turtlesim_demo_flexbe_states/package.xml
* fix stale test
* Stop TimedCmdVelState on interruption
* Handle RotateTurtleState terminal action statuses

0.0.2 (2024-06-17)
------------------
* reduce unavailable timeouts in simple state tests
* update to avoid deprecated createPublisher function call
* Modify turtlesim import to work with Kilted+ turtlesim_msgs or older turtlesim imports
* depend on flexbe_webui not older flexbe_app
* set up clients on start, and remove on stop

0.0.1 (2023-07-21)
------------------
* Initial release of FlexBE Turtlesim Quick-start demonstrations and detailed examples
