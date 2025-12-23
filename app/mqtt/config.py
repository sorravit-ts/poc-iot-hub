import os

IOTHUB_HOSTNAME = "zeep-iot-hub.azure-devices.net"
DEVICE_ID = "devTestDevice"
API_VERSION = "2021-04-12"

DEVICE_KEY = "jNidTC4KBr9OhmN+8+mU81aiUtunJQ48wdzwNomtAUs="

MQTT_PORT = 8883

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CA_CERT_PATH = os.path.join(
    BASE_DIR, "certs", "DigiCert Global Root G2.crt.pem"
)
