#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2026 David Conner
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

"""
Define FlexBE Turtlesim Demo.

Created on July 2023
@author: David Conner
"""


from flexbe_core import Autonomy, Behavior, ConcurrencyContainer, Logger, OperatableStateMachine, PriorityContainer

from flexbe_states.input_state import InputState
from flexbe_states.log_state import LogState
from flexbe_states.operator_decision_state import OperatorDecisionState

from flexbe_turtlesim_demo_flexbe_behaviors.turtlesim_input_state_behavior_sm import TurtlesimInputStateBehaviorSM

from flexbe_turtlesim_demo_flexbe_states.clear_turtlesim_state import ClearTurtlesimState
from flexbe_turtlesim_demo_flexbe_states.teleport_absolute_state import TeleportAbsoluteState
from flexbe_turtlesim_demo_flexbe_states.timed_cmd_vel_state import TimedCmdVelState

# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


class FlexBETurtlesimDemoSM(Behavior):
    """
    Define FlexBE Turtlesim Demo.

    FlexBE demonstration using ROS Turtlesim from ROS tutorials.

    Demonstrates several FlexBE capabilities including synchronous and async service calls,
    action interfaces, and  operator input.

    """

    def __init__(self, node):
        """Initialize ROS resources and nested behaviors for the demo."""
        super().__init__()
        self.name = 'FlexBE Turtlesim Demo'

        # parameters of this behavior

        # references to used behaviors
        OperatableStateMachine.initialize_ros(node)
        ConcurrencyContainer.initialize_ros(node)
        PriorityContainer.initialize_ros(node)
        Logger.initialize(node)
        ClearTurtlesimState.initialize_ros(node)
        InputState.initialize_ros(node)
        LogState.initialize_ros(node)
        OperatorDecisionState.initialize_ros(node)
        TeleportAbsoluteState.initialize_ros(node)
        TimedCmdVelState.initialize_ros(node)
        self.add_behavior(TurtlesimInputStateBehaviorSM, 'Turtlesim Input State Behavior', node)

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]

        # [/MANUAL_INIT]

        # Behavior comments:

    def create(self):
        """Build the top-level turtlesim demo state machine."""
        cmd_vel = '/turtle1/cmd_vel'
        # x:1086 y:238
        _state_machine = OperatableStateMachine(outcomes=['finished'])
        _state_machine.userdata.home = [5.5, 5.5, 0.]

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]

        # [/MANUAL_CREATE]
        # x:788 y:126, x:783 y:273
        _sm_goto_0 = OperatableStateMachine(outcomes=['finished', 'failed'])

        with _sm_goto_0:
            # x:41 y:116
            OperatableStateMachine.add('GetPose',
                                       InputState(request=3, message='Input pose (x, y, radians)', timeout=1.0),
                                       transitions={'received': 'GoToPose', 'aborted': 'GoToFail',
                                                    'no_connection': 'GoToFail', 'data_error': 'GoToFail'},
                                       autonomy={'received': Autonomy.Off, 'aborted': Autonomy.Off,
                                                 'no_connection': Autonomy.Off, 'data_error': Autonomy.Off},
                                       remapping={'data': 'pose'})

            # x:585 y:258
            OperatableStateMachine.add('GoToFail',
                                       LogState(text='Failed to go to pose', severity=Logger.REPORT_WARN),
                                       transitions={'done': 'failed'},
                                       autonomy={'done': Autonomy.Off})

            # x:319 y:101
            OperatableStateMachine.add('GoToPose',
                                       TeleportAbsoluteState(turtle_name='turtle1', x=0.0, y=0.0, theta=0.0,
                                                             call_timeout=3.0, wait_timeout=3.0,
                                                             service_name='teleport_absolute'),
                                       transitions={'done': 'finished', 'failed': 'GoToFail',
                                                    'call_timeout': 'GoToFail', 'unavailable': 'GoToFail'},
                                       autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off,
                                                 'call_timeout': Autonomy.Off, 'unavailable': Autonomy.Off},
                                       remapping={'pose': 'pose'})

        # x:975 y:134, x:130 y:365
        _sm_eightmove_1 = OperatableStateMachine(outcomes=['finished', 'failed'])

        with _sm_eightmove_1:
            # x:130 y:43
            OperatableStateMachine.add('Forward0',
                                       TimedCmdVelState(target_time=3.99, velocity=0.5, rotation_rate=0.0,
                                                        cmd_topic=cmd_vel, desired_rate=50),
                                       transitions={'done': 'LeftTurn'},
                                       autonomy={'done': Autonomy.Off})

            # x:414 y:314
            OperatableStateMachine.add('Forward1',
                                       TimedCmdVelState(target_time=7.99, velocity=0.5, rotation_rate=0.0,
                                                        cmd_topic=cmd_vel, desired_rate=50),
                                       transitions={'done': 'RightTurn'},
                                       autonomy={'done': Autonomy.Off})

            # x:663 y:38
            OperatableStateMachine.add('Forward2',
                                       TimedCmdVelState(target_time=3.99, velocity=0.5, rotation_rate=0.0,
                                                        cmd_topic=cmd_vel, desired_rate=50),
                                       transitions={'done': 'finished'},
                                       autonomy={'done': Autonomy.Off})

            # x:179 y:211
            OperatableStateMachine.add('LeftTurn',
                                       TimedCmdVelState(target_time=5.77, velocity=0.5, rotation_rate=0.667,
                                                        cmd_topic=cmd_vel, desired_rate=50),
                                       transitions={'done': 'Forward1'},
                                       autonomy={'done': Autonomy.Off})

            # x:625 y:189
            OperatableStateMachine.add('RightTurn',
                                       TimedCmdVelState(target_time=5.77, velocity=0.5, rotation_rate=-0.667,
                                                        cmd_topic=cmd_vel, desired_rate=50),
                                       transitions={'done': 'Forward2'},
                                       autonomy={'done': Autonomy.Off})

        with _state_machine:
            # x:57 y:316
            OperatableStateMachine.add('ClearEntry',
                                       ClearTurtlesimState(service_name='/clear', wait_timeout=3.0),
                                       transitions={'done': 'Home', 'failed': 'Home', 'unavailable': 'Unavailable'},
                                       autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off, 'unavailable': Autonomy.Off})

            # x:911 y:133
            OperatableStateMachine.add('ClearFailed',
                                       LogState(text='Failed to clear Turtlesim window!', severity=Logger.REPORT_HINT),
                                       transitions={'done': 'Operator'},
                                       autonomy={'done': Autonomy.Off})

            # x:694 y:20
            OperatableStateMachine.add('ClearLog',
                                       LogState(text='Clear turtlesim window ...', severity=Logger.REPORT_HINT),
                                       transitions={'done': 'ClearWindow'},
                                       autonomy={'done': Autonomy.Off})

            # x:893 y:15
            OperatableStateMachine.add('ClearWindow',
                                       ClearTurtlesimState(service_name='/clear', wait_timeout=3.0),
                                       transitions={'done': 'Operator', 'failed': 'ClearFailed', 'unavailable': 'ClearFailed'},
                                       autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off, 'unavailable': Autonomy.Off})

            # x:654 y:490
            OperatableStateMachine.add('EightMove',
                                       _sm_eightmove_1,
                                       transitions={'finished': 'StopCmd', 'failed': 'FailedEight'},
                                       autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

            # x:297 y:419
            OperatableStateMachine.add('FailedEight',
                                       LogState(text='Failed Eight pattern', severity=Logger.REPORT_HINT),
                                       transitions={'done': 'Operator'},
                                       autonomy={'done': Autonomy.Off})

            # x:550 y:287
            OperatableStateMachine.add('Finished Eight-pattern',
                                       LogState(text='Finished 8 pattern', severity=Logger.REPORT_HINT),
                                       transitions={'done': 'Operator'},
                                       autonomy={'done': Autonomy.Off})

            # x:459 y:4
            OperatableStateMachine.add('GoHome',
                                       LogState(text='Go to home position', severity=Logger.REPORT_HINT),
                                       transitions={'done': 'Home'},
                                       autonomy={'done': Autonomy.Off})

            # x:731 y:564
            OperatableStateMachine.add('GoTo',
                                       _sm_goto_0,
                                       transitions={'finished': 'PoseDone', 'failed': 'PoseDone'},
                                       autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

            # x:178 y:77
            OperatableStateMachine.add('Home',
                                       TeleportAbsoluteState(turtle_name='turtle1', x=5.544, y=5.544, theta=0.0,
                                                             call_timeout=3.0, wait_timeout=3.0,
                                                             service_name='teleport_absolute'),
                                       transitions={'done': 'AtHome', 'failed': 'ServiceCallFailed',
                                                    'call_timeout': 'ServiceCallFailed', 'unavailable': 'ServiceCallFailed'},
                                       autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off, 'call_timeout': Autonomy.Off,
                                                 'unavailable': Autonomy.Off},
                                       remapping={'pose': 'home'})

            # x:651 y:133
            OperatableStateMachine.add('Operator',
                                       OperatorDecisionState(outcomes=['Home', 'Eight', 'Quit', 'Clear', 'Rotate', 'Pose'],
                                                             hint="Suggest 'Eight' for pattern move", suggestion='Eight'),
                                       transitions={'Home': 'GoHome', 'Eight': 'EightMove', 'Quit': 'finished',
                                                    'Clear': 'ClearLog', 'Rotate': 'Turtlesim Input State Behavior',
                                                    'Pose': 'GoTo'},
                                       autonomy={'Home': Autonomy.Full, 'Eight': Autonomy.High, 'Quit': Autonomy.Full,
                                                 'Clear': Autonomy.Full, 'Rotate': Autonomy.Full, 'Pose': Autonomy.Full})

            # x:934 y:534
            OperatableStateMachine.add('PoseDone',
                                       LogState(text='Updated pose', severity=Logger.REPORT_HINT),
                                       transitions={'done': 'Operator'},
                                       autonomy={'done': Autonomy.Off})

            # x:967 y:330
            OperatableStateMachine.add('RotateFailed',
                                       LogState(text='Rotate failed', severity=Logger.REPORT_HINT),
                                       transitions={'done': 'Operator'},
                                       autonomy={'done': Autonomy.Off})

            # x:1072 y:281
            OperatableStateMachine.add('RotateLog',
                                       LogState(text='Rotation complete', severity=Logger.REPORT_HINT),
                                       transitions={'done': 'Operator'},
                                       autonomy={'done': Autonomy.Off})

            # x:417 y:159
            OperatableStateMachine.add('ServiceCallFailed',
                                       LogState(text='Failed during TeleportAbsolute service for turtlesim',
                                                severity=Logger.REPORT_HINT),
                                       transitions={'done': 'Operator'},
                                       autonomy={'done': Autonomy.Off})

            # x:471 y:391
            OperatableStateMachine.add('StopCmd',
                                       TimedCmdVelState(target_time=0.01, velocity=0.0, rotation_rate=0.0,
                                                        cmd_topic=cmd_vel, desired_rate=50),
                                       transitions={'done': 'Finished Eight-pattern'},
                                       autonomy={'done': Autonomy.Off})

            # x:957 y:437
            OperatableStateMachine.add('Turtlesim Input State Behavior',
                                       self.use_behavior(TurtlesimInputStateBehaviorSM, 'Turtlesim Input State Behavior'),
                                       transitions={'finished': 'RotateLog', 'failed': 'RotateFailed'},
                                       autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

            # x:345 y:299
            OperatableStateMachine.add('Unavailable',
                                       LogState(text='Service is unavailable - Start turtlesim?', severity=Logger.REPORT_HINT),
                                       transitions={'done': 'Operator'},
                                       autonomy={'done': Autonomy.Off})

            # x:461 y:80
            OperatableStateMachine.add('AtHome',
                                       LogState(text='Turtle is home!', severity=Logger.REPORT_HINT),
                                       transitions={'done': 'Operator'},
                                       autonomy={'done': Autonomy.Off})

        return _state_machine

    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]

    # [/MANUAL_FUNC]
