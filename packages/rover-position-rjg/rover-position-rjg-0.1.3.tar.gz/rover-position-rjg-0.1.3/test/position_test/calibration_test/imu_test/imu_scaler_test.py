import inspect
import os
import unittest

from rover_position_rjg.data.data import Data
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.calibration.imu.imu_scaler import ImuScaler
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData


class ImuScalerTest(unittest.TestCase):
    def setUp(self):
        dir_name = os.path.dirname(inspect.getfile(ImuScalerTest))
        self.filename = os.path.join(dir_name, 'calibration.json')
        self.bias = Vector([1, 2, 3])
        offset = self.build(self.bias)
        self.scaler = ImuScaler(offset=offset,
                                gyro_zero_band_height=Vector([2, 4, 6]),
                                gyro_zero_band_num_samples=10,
                                cross_axis_sensitivities=(Vector.zero(), Vector.zero(), Vector.zero()))

    def test_default_scale(self):
        scaler = ImuScaler()
        data = self.build(Vector([123, 456, 999]))
        # Act
        result = scaler.scale(Data(data, 100))
        # Assert
        self.assertEqual(Vector([123, 456, 999]), result.value.angular_velocity.value)

    def test_does_not_adjust_gyro_bias_with_zero_value(self):
        data = self.build(self.bias)
        # Act
        result = self.scaler.scale(Data(data, 100))
        # Assert
        self.assertEqual(Vector.zero(), result.value.angular_velocity.value)
        self.assertEqual(self.bias, self.scaler.offset.angular_velocity.value)

    def test_does_not_adjust_gyro_bias_with_large_value(self):
        angular_velocity = Vector([-100, 55, 33])
        data = self.build(angular_velocity)
        # Act
        result = self.scaler.scale(Data(data, 100))
        # Assert
        self.assertEqual(self.bias, self.scaler.offset.angular_velocity.value)

    def test_adjusts_gyro_bias(self):
        data = self.build(Vector([2, 0, 6]))
        # Act
        self.scaler.scale(Data(data, 100))
        # Assert
        self.assertEqual(Vector([1.1, 1.8, 3.3]), self.scaler.offset.angular_velocity.value)

    def test_uses_adjusted_gyro_bias_to_scale_result(self):
        data = self.build(Vector([2, 0, 6]))
        # Act
        result = self.scaler.scale(Data(data, 100))
        # Assert
        self.assertEqual(Vector([0.9, -1.8, 2.7]), result.value.angular_velocity.value)

    def test_gyro_bias_uses_loaded_offset(self):
        data = self.build(Vector([11, 6, 2]))
        # Act
        self.scaler.load(self.filename)
        result = self.scaler.scale(Data(data, 100))
        # Assert
        self.assertEqual(Vector([0.9, 0.9, 1.8]), result.value.angular_velocity.value)
        self.assertEqual(Vector([10.1, 5.1, 0.2]), self.scaler.offset.angular_velocity.value)

    def test_calibrate_angular_velocity_offset(self):
        # Act
        self.scaler.calibrate()
        self.assertTrue(self.scaler.calibrating)
        self.receive_calibration_samples()
        # Assert
        self.assertFalse(self.scaler.calibrating)
        self.assertEqual(Vector([100, 200, 300]), self.scaler.offset.angular_velocity.value)

    def test_calibrate_sets_zero_band(self):
        # Act
        self.scaler.calibrate()
        self.assertTrue(self.scaler.calibrating)
        self.receive_calibration_samples()
        # Assert
        self.assertFalse(self.scaler.calibrating)
        self.assertEqual(Vector([4.898980, 4.898980, 10.954451]), self.scaler.gyro_zero_band_height)
        gyro_offset = self.scaler.offset.angular_velocity.value
        self.assertEqual(gyro_offset + self.scaler.gyro_zero_band_height, self.scaler.gyro_zero_upper_limit)
        self.assertEqual(gyro_offset - self.scaler.gyro_zero_band_height, self.scaler.gyro_zero_lower_limit)

    def test_acceleration_cross_axis_sensitivities(self):
        scaler = ImuScaler(gyro_zero_band_height=Vector.zero(),
                           gyro_zero_band_num_samples=10,
                           cross_axis_sensitivities=(Vector([0, 1, -1]), Vector([1, 0, -1]), Vector([1, -1, 0])))
        # Act/Assert
        self.assert_acceleration(scaler, Vector([2, -2, 2]), Vector([2, 0, 0]))
        self.assert_acceleration(scaler, Vector([-1, 1, 1]), Vector([0, 1, 0]))
        self.assert_acceleration(scaler, Vector([-3, 3, 3]), Vector([0, 0, 3]))
        self.assert_acceleration(scaler, Vector([-2, 2, 6]), Vector([2, 1, 3]))

    def assert_acceleration(self, scaler: ImuScaler, expected: Vector, initial_acceleration: Vector):
        result = scaler.scale(Data(self.build(acceleration=initial_acceleration), 100))
        acc = result.value.acceleration.value
        self.assertEqual(expected, acc)

    @staticmethod
    def build(angular_velocity: Vector = Vector.zero(), acceleration: Vector = Vector.zero()) -> NineDoFData:
        result = NineDoFData.zero()
        result.angular_velocity.value = angular_velocity
        result.acceleration.value = acceleration
        return result

    def receive_calibration_samples(self):
        data = self.build(Vector([92, 192, 282]))
        self.scaler.scale(Data(data, 100))
        data = self.build(Vector([94, 194, 284]))
        self.scaler.scale(Data(data, 100))
        data = self.build(Vector([96, 196, 296]))
        self.scaler.scale(Data(data, 100))
        data = self.build(Vector([98, 198, 298]))
        self.scaler.scale(Data(data, 100))
        data = self.build(Vector([100, 200, 300]))
        self.scaler.scale(Data(data, 100))
        data = self.build(Vector([100, 200, 300]))
        self.scaler.scale(Data(data, 100))
        data = self.build(Vector([102, 202, 302]))
        self.scaler.scale(Data(data, 100))
        data = self.build(Vector([104, 204, 304]))
        self.scaler.scale(Data(data, 100))
        data = self.build(Vector([106, 206, 316]))
        self.scaler.scale(Data(data, 100))
        data = self.build(Vector([108, 208, 318]))
        self.scaler.scale(Data(data, 100))
