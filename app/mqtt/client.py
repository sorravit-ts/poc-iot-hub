import ssl
import threading
from paho.mqtt import client as mqtt

from .settings import settings
from .sas import generate_sas_token


class IoTHubMQTTClient:
    def __init__(self):
        uri = f"{settings.IOTHUB_HOSTNAME.lower()}/devices/{settings.DEVICE_ID}"
        sas_token = generate_sas_token(uri, settings.DEVICE_KEY)

        self.client = mqtt.Client(
            client_id=settings.DEVICE_ID,
            protocol=mqtt.MQTTv311,
        )

        self.client.username_pw_set(
            username=(
                f"{settings.IOTHUB_HOSTNAME}/"
                f"{settings.DEVICE_ID}/"
                f"?api-version={settings.API_VERSION}"
            ),
            password=sas_token,
        )

        self.client.tls_set(
            ca_certs=str(settings.ca_cert_path),
            tls_version=ssl.PROTOCOL_TLS_CLIENT,
        )

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish

    # ---------- Lifecycle ----------

    def start(self):
        thread = threading.Thread(
            target=self._loop,
            daemon=True,
        )
        thread.start()

    def _loop(self):
        self.client.connect(
            settings.IOTHUB_HOSTNAME,
            settings.MQTT_PORT,
        )
        self.client.loop_forever()

    # ---------- Public API ----------

    def publish(self, payload: str, qos: int = 0):
        topic = f"devices/{settings.DEVICE_ID}/messages/events/"
        return self.client.publish(topic, payload, qos=qos)

    # ---------- Callbacks ----------

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("✅ Connected to IoT Hub")
            client.subscribe(
                f"devices/{settings.DEVICE_ID}/messages/devicebound/#",
                qos=1,
            )
        else:
            print("❌ Connect failed:", rc)

    def on_disconnect(self, client, userdata, rc):
        print("⚠️ Disconnected, rc =", rc)

    def on_message(self, client, userdata, msg):
        print(f"📩 C2D {msg.topic}: {msg.payload.decode()}")

    def on_publish(self, client, userdata, mid):
        print("✅ Published mid =", mid)
