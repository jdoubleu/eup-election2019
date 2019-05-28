# provide crypto functions
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

# constants
cert_file = 'certificate.crt'
ca_file = 'certchain.crt'

# functions
def get_public_key():
    with open(cert_file, 'rb') as cf:
        cert = x509.load_pem_x509_certificate(cf.read(), default_backend())
        return cert.public_key()

def verify_file_sig(file, sig_file):
    public_key = get_public_key()
    
    with open(file, 'rb') as data, open(sig_file, 'rb') as sig:
        try:        
            public_key.verify(
                sig.read(), 
                data.read(),
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            return True
        except cryptography.exceptions.InvalidSignature as e:
            return False