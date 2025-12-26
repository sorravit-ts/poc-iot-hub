
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