from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography import x509
from cryptography.x509.oid import NameOID



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
    if isinstance(key, rsa.RSAPrivateKey):
        return key
    else:
        raise TypeError('Not a RSA private key.')


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
    if isinstance(pubkey, rsa.RSAPublicKey):
        return pubkey
    else:
        raise TypeError('Not a RSA public key.')


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


def genNameForm(country, state, city, orgName, commonName):

    nameForm = x509.Name([x509.NameAttribute(NameOID.COUNTRY_NAME, country),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
        x509.NameAttribute(NameOID.LOCALITY_NAME, city),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, orgName),
        x509.NameAttribute(NameOID.COMMON_NAME, commonName),
        ])
    return nameForm


def genCSR(subject, key):
    csr = x509.CertificateSigningRequestBuilder().\
        subject_name(subject).\
        sign(key, hashes.SHA256(), default_backend())
    return csr


# def saveCSR(csr, filename):
#     with open(filename, "wb") as f:
#         f.write(csr.public_bytes(serialization.Encoding.PEM))
#
#
# def loadCSR(filename):
#     with open(filename, "rb") as f:
#         csr = x509.load_pem_x509_csr(f.read, default_backend())
#     return csr


import datetime
def genCert(csr, issuer, key, expired_in):
    cert = x509.CertificateBuilder().\
        subject_name(csr.subject).\
        issuer_name(issuer).\
        public_key(csr.public_key()).\
        serial_number(x509.random_serial_number()).\
        not_valid_before(datetime.datetime.utcnow()).\
        not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=expired_in)).\
        sign(key, hashes.SHA256(), default_backend())
    return cert


def saveCert(cert, filename):
    with open(filename, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))


def loadCert(filename):
    with open(filename, 'rb') as f:
        cert = x509.load_pem_x509_certificate(f.read(), default_backend())
    return cert
