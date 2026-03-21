#! /usr/bin/env python3

# Copyright 2026 Christopher Newport University
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

"""Demo script for calculating twist parameters for given turns."""
import math


def turn_rate():
    """
    Calcuate parameters for FlexBE TurtleSim demo figure eight pattern.

    Manually enter these into the FlexBE parameters for figure eight

    Note: FlexBE attempts to execute at a fixed rate, so times will only be approximate
    within resolution of update rate. Adjust the times downward to generate approximate
    desired transitions

    """
    desired_velocity = 0.5  # m/s
    fwd_distance_traveled = 2.0  # m
    desired_radius_of_curvature = 0.75  # meters

    print(f'Desired velocity = {desired_velocity:.3f} m/s')
    print(f'Desired Forward travel  = {fwd_distance_traveled:.3f} m/s')
    print(f'Desired radius of curvature  = {desired_radius_of_curvature:.3f} m')

    fwd_travel_time = fwd_distance_traveled / desired_velocity
    rate_of_turn = desired_velocity / desired_radius_of_curvature

    print(f'Required Forward travel time  = {fwd_travel_time:.3f} seconds')
    print(f'Required Rate of turn    = {rate_of_turn:.3f} radians/s')

    # Angle between lines connecting the center of rotation to starting point and initial tangent point at start of turn
    bisecting_angle = math.pi / 2 - math.atan2(desired_radius_of_curvature, fwd_distance_traveled)

    # Total turning angle
    turning_angle = 2 * math.pi - 2 * bisecting_angle
    turning_travel_time = turning_angle / rate_of_turn
    print(f'Required turning time   = {turning_travel_time:.3f} seconds')


if __name__ == '__main__':
    turn_rate()
