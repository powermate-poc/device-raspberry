import time
import paho.mqtt.client as mqtt


class Mqtt:
    client: mqtt.Client
    client_id: str

    def __init__(
            self,
            endpoint: str,
            client_id: str,
            port: int = 8883) -> None:
        self.client_id = client_id

        print(f"connecting to mqtt://{endpoint}:{port} as '{client_id}'...")

        self.client = mqtt.Client(protocol=mqtt.MQTTv5, client_id=client_id)
        self.client.tls_set(
            ca_certs="./certs/RootCA.pem",
            certfile="./certs/certificate.pem.crt",
            keyfile="./certs/private.pem.key")
        self.client.connect(endpoint, port, 30)
        self.client.loop_start()

        while not self.client.is_connected():
            time.sleep(0.1)

        print("MQTT Connected!")
