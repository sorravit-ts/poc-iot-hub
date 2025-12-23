
from fastapi import FastAPI, HTTPException

from app.mqtt.client import IoTHubMQTTClient
from app.models.telemetry import Telemetry

app = FastAPI()

mqtt_client = IoTHubMQTTClient()
mqtt_client.start()


@app.post("/send")
async def send_telemetry(data: Telemetry):
    result = mqtt_client.publish(data.json(), qos=0)

    if result.rc != 0:
        raise HTTPException(
            status_code=500,
            detail="Failed to publish telemetry",
        )

    return {
        "status": "sent",
        "payload": data.dict(),
    }


# import os
# import ssl
# import base64
# import hmac
# import hashlib
# import time
# import urllib.parse
# from fastapi import FastAPI, HTTPException
# from paho.mqtt import client as mqtt
# from pydantic import BaseModel
# import threading

# # SAS Token
# def generate_sas_token(uri, key, expiry=3600):
#     ttl = int(time.time()) + expiry
#     sign_key = f"{urllib.parse.quote(uri, safe='')}\n{ttl}"
#     signature = base64.b64encode(
#         hmac.new(base64.b64decode(key), sign_key.encode("utf-8"), hashlib.sha256).digest()
#     )
#     sas = f"SharedAccessSignature sr={urllib.parse.quote(uri, safe='')}&sig={urllib.parse.quote(signature.decode())}&se={ttl}"
#     return sas


# IOTHUB_HOSTNAME = "zeep-iot-hub.azure-devices.net"
# DEVICE_ID = "devTestDevice"
# API_VERSION = "2021-04-12"

# # Private key for device 'devTestDevice'
# # DEVICE_KEY = "SX+KXFsFLilmgdvI/QDQkK1pLfmq3xt81ZA+GXxYOMI=" 

# # Second device 'devTestDevice2' key
# DEVICE_KEY = "jNidTC4KBr9OhmN+8+mU81aiUtunJQ48wdzwNomtAUs="

# uri = f"{IOTHUB_HOSTNAME.lower()}/devices/{DEVICE_ID}"
# SAS_TOKEN = generate_sas_token(uri, DEVICE_KEY, 3600)

# MQTT_BROKER = IOTHUB_HOSTNAME
# MQTT_PORT = 8883

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# CA_CERT_PATH = os.path.join(BASE_DIR, "certs", "DigiCert Global Root G2.crt.pem")
# CA_CERT_PATH = os.path.abspath(CA_CERT_PATH)

# app = FastAPI()

# class Telemetry(BaseModel):
#     temperature: float
#     humidity: float

# # MQTT Client
# mqtt_client = mqtt.Client(client_id=DEVICE_ID, protocol=mqtt.MQTTv311)


# mqtt_client.username_pw_set(
#     username=f"{IOTHUB_HOSTNAME}/{DEVICE_ID}/?api-version=2021-04-12",
#     password=SAS_TOKEN
# )


# mqtt_client.tls_set(
#     ca_certs=CA_CERT_PATH,
#     tls_version=ssl.PROTOCOL_TLS
# )

# def on_connect(client, userdata, flags, rc):
#     if rc == 0:
#         print("✅ Connected to IoT Hub successfully")
#         # subscribe cloud-to-device messages
#         topic = f"devices/{DEVICE_ID}/messages/devicebound/#"
#         client.subscribe(topic, qos=1)
#     else:
#         print("❌ Failed to connect, return code:", rc)

# def on_disconnect(client, userdata, rc):
#     print("⚠️ Disconnected, rc =", rc)

# def on_message(client, userdata, msg):
#     print(f"📩 Received C2D message on topic {msg.topic}: {msg.payload.decode()}")

# def on_publish(client, userdata, mid):
#     print("✅ Message published, mid = ", mid, ", userdata =", userdata," client =", client)

# mqtt_client.on_connect = on_connect
# mqtt_client.on_disconnect = on_disconnect
# mqtt_client.on_message = on_message
# mqtt_client.on_publish = on_publish

# def mqtt_loop():
#     mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
#     mqtt_client.loop_forever()

# threading.Thread(target=mqtt_loop, daemon=True).start()

# @app.post("/send")
# async def send_telemetry(data: Telemetry):
#     topic = f"devices/{DEVICE_ID}/messages/events/"
#     payload = data.json()

#     print("Connected:", mqtt_client.is_connected())
#     # result = mqtt_client.publish(topic, payload, qos=1)
#     result = mqtt_client.publish("devices/" + DEVICE_ID + "/messages/events/", payload, qos=0)

#     print("Publish result:", result)
#     if result.rc != mqtt.MQTT_ERR_SUCCESS:
#         raise HTTPException(status_code=500, detail="Failed to publish")

#     return {"status": "sent", "payload": payload}

