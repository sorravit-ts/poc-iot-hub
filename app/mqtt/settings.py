from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # IoT Hub
    IOTHUB_HOSTNAME: str
    DEVICE_ID: str
    API_VERSION: str = "2021-04-12"

    DEVICE_KEY: str

    # MQTT
    MQTT_PORT: int = 8883

    # Cert // Optional
    CA_CERT_FILENAME: str = "DigiCert Global Root G2.crt.pem"

    @property
    def ca_cert_path(self) -> Path:
        base_dir = Path(__file__).resolve().parents[1]
        return base_dir / "certs" / self.CA_CERT_FILENAME

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
