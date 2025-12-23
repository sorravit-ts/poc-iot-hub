from azure.iot.hub import IoTHubRegistryManager

CONNECTION_STR = 'HostName=zeep-iot-hub.azure-devices.net;DeviceId=devTestDevice;SharedAccessKey=SX+KXFsFLilmgdvI/QDQkK1pLfmq3xt81ZA+GXxYOMI='
DEVICE_ID = "devTestDevice"

registry_manager = IoTHubRegistryManager(CONNECTION_STR)
device = registry_manager.get_device(DEVICE_ID)

app = FastAPI()

print(device)
