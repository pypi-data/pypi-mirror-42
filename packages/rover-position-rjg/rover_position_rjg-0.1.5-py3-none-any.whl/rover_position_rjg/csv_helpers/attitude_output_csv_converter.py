from typing import Iterable

from rover_position_rjg.csv_helpers.csv_converter import CsvConverter, TCsvItem
from rover_position_rjg.csv_helpers.quaternion_csv_converter import QuaternionCsvConverter
from rover_position_rjg.csv_helpers.vector_csv_converter import VectorCsvConverter
from rover_position_rjg.position.filters.attitude_filter import AttitudeOutput


class AttitudeOutputCsvConverter(CsvConverter[AttitudeOutput]):
    def __init__(self):
        self.vector_converter = VectorCsvConverter()
        self.quaternion_converter = QuaternionCsvConverter()

    def to_row(self, value: AttitudeOutput) -> Iterable[TCsvItem]:
        result = list(self.vector_converter.to_row(value.acceleration))
        result.extend(self.quaternion_converter.to_row(value.attitude))
        return result

    def to_object(self, row: Iterable[TCsvItem]) -> AttitudeOutput:
        acceleration = self.vector_converter.to_object(row[0:3])
        attitude = self.quaternion_converter.to_object(row[3:7])
        return AttitudeOutput(acceleration, attitude)
