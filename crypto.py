from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


def genKey():
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    return key


def saveKey(key, filename):
    with open(filename, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))


def keyBytes(key):
    return key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )


def loadKey(filename):
    with open(filename, 'rb') as f:
        key = serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())
    return key


def savePubkey(pubkey, filename):
    with open(filename, "wb") as f:
        f.write(pubkey.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))


def pubkeyBytes(pubkey):
    return pubkey.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


def loadPubkey(filename):
    with open(filename, 'rb') as f:
        pubkey = serialization.load_pem_public_key(f.read(), backend=default_backend())
    return pubkey


def signing(key, msg):
    signature = key.sign(
        msg,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature


def verification(pubkey, msg, signature):
    try:
        pubkey.verify(
            signature,
            msg,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    except:
        return False
    return True


def sha256(msg):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(msg)
    return digest.finalize()    # Encoding 'ISO-8859-1' or 'latin_1'


def dhash(msg):
    return sha256(sha256(msg))


def genAddr(pubkey):
    msg = pubkeyBytes(pubkey)
    return dhash(msg)
