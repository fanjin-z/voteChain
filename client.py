import requests
import crypto

SERVER_URL = 'localhost:5000'

def certReq(country, state, city, commonName, info='I;m a Legit voter'):
    subject = crypto.genNameForm(country, state, city, 'voter', commonName)
    key = crypto.genKey()
    csr = crypto.genCSR(subject, key)
    csr_pem = crypto.CSRtoBytes(csr)

    payload = {'csr':csr_pem, 'info':info}
    r = requests.post(SERVER_URL + '/certReq', data=payload)
    print(r.status_code)
