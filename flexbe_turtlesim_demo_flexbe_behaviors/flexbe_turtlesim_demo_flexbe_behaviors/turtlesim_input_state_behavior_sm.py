#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2023 Collin Stone
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
Define Turtlesim Input State Behavior.

A simple behavior demonstrating the Turtlesim RotateAbsolute action interface,
and
the FlexBE input state with a simple generic user interface.

Created on Mon Jul 17 2023
@author: Collin Stone
"""


from flexbe_core import Autonomy
from flexbe_core import Behavior
from flexbe_core import ConcurrencyContainer
from flexbe_core import Logger
from flexbe_core import OperatableStateMachine
from flexbe_core import PriorityContainer
from flexbe_core import initialize_flexbe_core
from flexbe_states.input_state import InputState
from flexbe_states.log_state import LogState
from flexbe_turtlesim_demo_flexbe_states.rotate_turtle_state import RotateTurtleState

# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]


# [/MANUAL_IMPORT]


class TurtlesimInputStateBehaviorSM(Behavior):
    """
    Define Turtlesim Input State Behavior.

    A simple behavior demonstrating the Turtlesim RotateAbsolute action interface,
    and
    the FlexBE input state with a simple generic user interface.
    """

    def __init__(self, node):
        super().__init__()
        self.name = 'Turtlesim Input State Behavior'

        # parameters of this behavior

        # Initialize ROS node information
        initialize_flexbe_core(node)

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]


        # [/MANUAL_INIT]

        # Behavior comments:

    def create(self):
        """Create state machine."""
        # Root state machine
        # x:1021 y:289, x:1259 y:249
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]


        # [/MANUAL_CREATE]

        with _state_machine:
            # x:202 y:136
            OperatableStateMachine.add('InputState',
                                       InputState(request=1,
                                                  message='Enter an angle (degrees): ',
                                                  timeout=1.0,
                                                  action_topic='flexbe/behavior_input'),
                                       transitions={'received': 'RotateTurtleState',
                                                    'aborted': 'Aborted',
                                                    'no_connection': 'No Connection',
                                                    'data_error': 'Data Error'},
                                       autonomy={'received': Autonomy.Low,
                                                 'aborted': Autonomy.Off,
                                                 'no_connection': Autonomy.Off,
                                                 'data_error': Autonomy.Off},
                                       remapping={'data': 'angle_degrees'})

            # x:457 y:10
            OperatableStateMachine.add('Aborted',
                                       LogState(text='Aborted',
                                                severity=Logger.REPORT_WARN),
                                       transitions={'done': 'failed'},
                                       autonomy={'done': Autonomy.Low})

            # x:760 y:531
            OperatableStateMachine.add('Canceled',
                                       LogState(text='Canceled',
                                                severity=Logger.REPORT_WARN),
                                       transitions={'done': 'failed'},
                                       autonomy={'done': Autonomy.Low})

            # x:452 y:243
            OperatableStateMachine.add('Data Error',
                                       LogState(text='Data Error',
                                                severity=Logger.REPORT_WARN),
                                       transitions={'done': 'failed'},
                                       autonomy={'done': Autonomy.Low})

            # x:761 y:434
            OperatableStateMachine.add('Failed',
                                       LogState(text='Failed',
                                                severity=Logger.REPORT_WARN),
                                       transitions={'done': 'failed'},
                                       autonomy={'done': Autonomy.Low})

            # x:453 y:137
            OperatableStateMachine.add('No Connection',
                                       LogState(text='No Connection',
                                                severity=Logger.REPORT_WARN),
                                       transitions={'done': 'failed'},
                                       autonomy={'done': Autonomy.Low})

            # x:453 y:336
            OperatableStateMachine.add('RotateTurtleState',
                                       RotateTurtleState(timeout=10,
                                                         action_topic='/turtle1/rotate_absolute'),
                                       transitions={'rotation_complete': 'Rotation Complete',
                                                    'failed': 'Failed',
                                                    'canceled': 'Canceled',
                                                    'timeout': 'Timeout'},
                                       autonomy={'rotation_complete': Autonomy.Off,
                                                 'failed': Autonomy.Off,
                                                 'canceled': Autonomy.Off,
                                                 'timeout': Autonomy.Off},
                                       remapping={'angle': 'angle_degrees', 'duration': 'duration'})

            # x:760 y:335
            OperatableStateMachine.add('Rotation Complete',
                                       LogState(text='Rotation Successful',
                                                severity=Logger.REPORT_HINT),
                                       transitions={'done': 'finished'},
                                       autonomy={'done': Autonomy.Off})

            # x:758 y:627
            OperatableStateMachine.add('Timeout',
                                       LogState(text='Timeout',
                                                severity=Logger.REPORT_WARN),
                                       transitions={'done': 'failed'},
                                       autonomy={'done': Autonomy.Low})

        return _state_machine

    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]


    # [/MANUAL_FUNC]
