from dotenv import load_dotenv
from sensor import RealMagnetSensor
from mqtt import Mqtt
from config import env_or_raise, env_or
from device import Device

if __name__ == "__main__":
    load_dotenv()

    endpoint = env_or_raise("IOT_CORE_ENDPOINT")
    client_id = env_or_raise("MQTT_CLIENT_ID")

    SAMPLES_PER_SECOND = int(env_or("SAMPLES_PER_SECOND", "1"))
    publish_magnet_data_raw = env_or("PUBLISH_MAGNET_DATA", "false")
    PUBLISH_MAGNET_DATA = publish_magnet_data_raw.lower() == "true"

    print(
        f"[PUBLISH_MAGNET_DATA] will publish raw magnet data: {PUBLISH_MAGNET_DATA}")

    client = Mqtt(endpoint, client_id)
    sensor = RealMagnetSensor()
    device = Device(sensor, client, SAMPLES_PER_SECOND, PUBLISH_MAGNET_DATA)
    device.start()
