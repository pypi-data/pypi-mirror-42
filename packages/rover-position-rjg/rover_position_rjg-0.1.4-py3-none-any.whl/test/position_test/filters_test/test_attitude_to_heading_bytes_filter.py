import time
import unittest
from unittest.mock import patch, MagicMock

import struct

from rover_position_rjg.data.quaternion import Quaternion

from rover_position_rjg.data.vector import Vector

from rover_position_rjg.position.filters.attitude_filter import AttitudeOutput

from rover_position_rjg.position.filters.attitude_to_heading_bytes_filter import AttitudeToHeadingBytesFilter
from rover_position_rjg.position.filters.fan_out_filter import *


class AttitudeToHeadingBytesFilterTest(unittest.TestCase):
    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_passes_data_to_filters(self, receiver: DataFilter[bytes, bytes]):
        receiver.receive = MagicMock()
        the_filter = AttitudeToHeadingBytesFilter()
        the_filter.add(receiver)
        # Act
        heading = Quaternion.from_tait_bryan_radians(Vector([10, 20, 30]))
        attitude_output = AttitudeOutput(Vector.zero(), heading)
        timestamp = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
        data = Data(attitude_output, timestamp)
        the_filter.receive(data)
        # Assert
        tb = heading.to_tait_bryan()
        expected = struct.pack('>ffff', tb.x, tb.y, tb.z, float(timestamp) / 1e9)
        receiver.receive.assert_called_once_with(Data(expected, timestamp))
