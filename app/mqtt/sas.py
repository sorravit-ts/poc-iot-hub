import base64
import hmac
import hashlib
import time
import urllib.parse


def generate_sas_token(uri: str, key: str, expiry: int = 3600) -> str:
    ttl = int(time.time()) + expiry
    sign_key = f"{urllib.parse.quote(uri, safe='')}\n{ttl}"

    signature = base64.b64encode(
        hmac.new(
            base64.b64decode(key),
            sign_key.encode("utf-8"),
            hashlib.sha256,
        ).digest()
    )

    return (
        "SharedAccessSignature "
        f"sr={urllib.parse.quote(uri, safe='')}"
        f"&sig={urllib.parse.quote(signature.decode())}"
        f"&se={ttl}"
    )
