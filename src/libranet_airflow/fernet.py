"""libranet_airflow.fernet."""
import cryptography.fernet


def generate_key():
    """Generate a fernet-key."""
    fernet_key = cryptography.fernet.Fernet.generate_key()
    print(fernet_key.decode())  # your fernet_key, keep it in secured place!
