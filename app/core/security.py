import secrets
import hashlib


def generate_api_key():
    """
    Docstring for generate_api_key

    generates an api key for each merchant and returns it
    """

    return f"sk_test_{secrets.token_urlsafe(32)}"


def hash_api_key(api_key: str):
    """
    Docstring for hash_api_key

    :param api_key: Description
    :type api_key: str
    returns a hashed version of the api key
    """

    return hashlib.sha256(api_key.encode()).hexdigest()
