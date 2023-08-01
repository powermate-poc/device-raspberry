import time
import csv
import json
from sensor import MagnetSensor
from mqtt import Mqtt

FILENAME = "magnetometer_data.csv"

TIMESTAMP = "timestamp [ns]"
X = "x"
Y = "y"
Z = "z"
ABSOLUTE = "absolute"


def cubic_meters_per_hour(
        rotation_start: int,
        rotation_end: int,
        gas_per_rotation: float = 0.01) -> float:
    delta_t = rotation_end - rotation_start
    delta_t_sec = delta_t / 1e9
    rotation_rate = 1 / delta_t_sec
    gas_consumption_rate = rotation_rate * gas_per_rotation * 3600

    return gas_consumption_rate


class Device:
    sensor: MagnetSensor
    samples_per_second: int
    mqtt: Mqtt
    publish_magnet_data: bool

    def __init__(
            self,
            sensor: MagnetSensor,
            mqtt: Mqtt,
            samples_per_second: int = 1,
            publish_magnet_data: bool = False) -> None:
        self.sensor = sensor
        self.mqtt = mqtt
        self.samples_per_second = samples_per_second
        self.publish_magnet_data = publish_magnet_data

    def start(self) -> None:
        filename = f"{int(time.time())}_{FILENAME}"
        print(f"Writing magnet data to {filename}")
        with open(filename, mode='w', newline='', encoding="utf8") as csv_file:
            fieldnames = [TIMESTAMP, X, Y, Z, ABSOLUTE]
            writer = csv.writer(csv_file)

            if csv_file.tell() == 0:
                writer.writerow(fieldnames)

            sleeptime = 1 / self.samples_per_second
            data_topic = f"{self.mqtt.client_id}/data"

            last_value: float = 1
            last_rotation_ts: int = -1
            while True:
                try:
                    magnet_x, magnet_y, magnet_z, magnet_abs = self.sensor.read()
                    timestamp = time.time_ns()

                    # TODO: make the axis configurable
                    if last_value <= 0 and magnet_z > 0:
                        # we detected a crossing from - to + --> a rotation has
                        # happened
                        self.mqtt.client.publish(
                            data_topic, self.rotation_to_json(
                                timestamp, last_rotation_ts))
                        last_rotation_ts = timestamp

                    if self.publish_magnet_data:
                        message = self.magnet_data_to_json(
                            timestamp, magnet_x, magnet_y, magnet_z, magnet_abs)
                        self.mqtt.client.publish(data_topic, message)

                    writer.writerow(
                        [timestamp, magnet_x, magnet_y, magnet_z, magnet_abs])
                    last_value = magnet_z
                except OSError:
                    print("Failed to read sensor data")

                time.sleep(sleeptime)

    def rotation_to_json(
            self,
            timestamp: int,
            last_rotation_ts: int) -> str:
        data = {
            "measurements": [
                {
                    "name": "timestamp",
                    "unit": "ns",
                    "value": timestamp
                },
                {
                    "name": "rotation",
                    "value": 1.0
                },
            ]
        }

        if last_rotation_ts != -1 :
            data["measurements"].append({
                "name": "consumption_rate",
                "value": cubic_meters_per_hour(last_rotation_ts, timestamp)
            })

        return json.dumps(data)

    def magnet_data_to_json(
            self,
            timestamp: int,
            magnet_x: float,
            magnet_y: float,
            magnet_z: float,
            abs_value: float) -> str:
        data = {
            "measurements": [
                {
                    "name": "timestamp",
                    "unit": "ns",
                    "value": timestamp
                },
                {
                    "name": "x",
                    "value": magnet_x
                },
                {
                    "name": "y",
                    "value": magnet_y
                },
                {
                    "name": "z",
                    "value": magnet_z
                },
                {
                    "name": "abs",
                    "value": abs_value
                }
            ]
        }
        return json.dumps(data)
