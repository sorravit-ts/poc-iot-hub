import ssl
import threading
from paho.mqtt import client as mqtt

from .settings import settings
from .sas import get_cached_sas_token


class IoTHubMQTTClient:
    def __init__(self):
        # -------------------------
        # เตรียมข้อมูลสำหรับสร้าง SAS Token
        # -------------------------
        # resource uri ของ device ตาม format ของ Azure IoT Hub
        uri = f"{settings.IOTHUB_HOSTNAME.lower()}/devices/{settings.DEVICE_ID}"
        
        # สร้าง SAS Token สำหรับ authenticate device
        sas_token = get_cached_sas_token(uri, settings.DEVICE_KEY)

        # -------------------------
        # สร้าง MQTT client
        # -------------------------
        self.client = mqtt.Client(
            client_id=settings.DEVICE_ID,     # client_id ต้องเป็น device_id
            protocol=mqtt.MQTTv311,            # IoT Hub รองรับ MQTT v3.1.1
        )

        # -------------------------
        # ตั้งค่า username / password (SAS Token)
        # -------------------------
        self.client.username_pw_set(
            username=(
                f"{settings.IOTHUB_HOSTNAME}/"
                f"{settings.DEVICE_ID}/"
                f"?api-version={settings.API_VERSION}"
            ),
            password=sas_token,
        )

        # -------------------------
        # ตั้งค่า TLS
        # -------------------------
        self.client.tls_set(
            ca_certs=str(settings.ca_cert_path),
            tls_version=ssl.PROTOCOL_TLS_CLIENT,
        )

        # -------------------------
        # ผูก callback function
        # -------------------------
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish

    # ---------- Lifecycle ----------

    def start(self):
        """
        เริ่ม MQTT client ใน background thread
        เพื่อไม่ block main thread ของแอป
        """
        thread = threading.Thread(
            target=self._loop,
            daemon=True,   # ปิดอัตโนมัติเมื่อ service shutdown
        )
        thread.start()

    def _loop(self):
        """
        เชื่อมต่อ IoT Hub และเริ่ม loop รับ/ส่ง message
        """
        self.client.connect(
            settings.IOTHUB_HOSTNAME,
            settings.MQTT_PORT,
        )
        self.client.loop_forever()

    # ---------- Public API ----------

    def publish(self, payload: str, qos: int = 0):
        """
        ส่ง message จาก device → IoT Hub (D2C)

        payload : ข้อมูลที่ต้องการส่ง (string)
        qos     : MQTT QoS level
        """
        topic = f"devices/{settings.DEVICE_ID}/messages/events/"
        
        # ใส่ query string เพิ่ม metadata ให้ message เป็น optional properties
        # (IoT Hub จะ map เป็น application properties)
        return self.client.publish(
            topic + "?type=alert&level=critical", payload, qos=qos)

    # ---------- Callbacks ----------

    def on_connect(self, client, userdata, flags, rc):
        """
        ถูกเรียกเมื่อเชื่อมต่อ IoT Hub
        """
        if rc == 0:
            print("✅ Connected to IoT Hub")
            
            # subscribe รับ Cloud-to-Device (C2D) message
            client.subscribe(
                f"devices/{settings.DEVICE_ID}/messages/devicebound/#",
                qos=1,
            )
        else:
            print("❌ Connect failed:", rc)

    def on_disconnect(self, client, userdata, rc):
        """
        ถูกเรียกเมื่อ connection หลุด
        """
        print("⚠️ Disconnected, rc =", rc)

    def on_message(self, client, userdata, msg):
        """
        ถูกเรียกเมื่อได้รับ C2D message จาก IoT Hub
        """
        print(f"📩 C2D {msg.topic}: {msg.payload.decode()}")

    def on_publish(self, client, userdata, mid):
        """
        ถูกเรียกเมื่อ publish message สำเร็จ
        """
        print("✅ Published mid =", mid)
