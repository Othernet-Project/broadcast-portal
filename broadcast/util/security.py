import hashlib
import hmac


def sign(data, secret_key):
    return hmac.new(secret_key, data, hashlib.sha256).hexdigest()

