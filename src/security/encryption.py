import os

from cryptography.fernet import Fernet

from src.utils.config_loader import load_config


class EncryptionKeyMissingError(Exception):
    pass


def generate_key():
    return Fernet.generate_key().decode()


def _get_key():
    config = load_config()
    env_var = config["security"]["encryption_key_env_var"]
    key = os.environ.get(env_var)
    if not key:
        raise EncryptionKeyMissingError(
            f"Set environment variable {env_var} with a Fernet key to enable encryption. "
            f"Generate one with generate_key()."
        )
    return key.encode()


def encrypt_file(input_path, output_path):
    fernet = Fernet(_get_key())
    with open(input_path, "rb") as f:
        data = f.read()
    encrypted = fernet.encrypt(data)
    with open(output_path, "wb") as f:
        f.write(encrypted)
    return output_path


def decrypt_file(input_path, output_path):
    fernet = Fernet(_get_key())
    with open(input_path, "rb") as f:
        data = f.read()
    decrypted = fernet.decrypt(data)
    with open(output_path, "wb") as f:
        f.write(decrypted)
    return output_path
