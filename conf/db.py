import os
import platform

SQL_USER = "api"
SQL_PASS = "7RWprblOldzfhu9lIlegrA"  # FIX: credential
DB_NAME = "defaultdb"
DB_PORT = 26257
SQL_HOST = "quantum-trader-3674.g8z.cockroachlabs.cloud"
DATABASE_URL = f"cockroachdb://{SQL_USER}:{SQL_PASS}@{SQL_HOST}:{DB_PORT}/{DB_NAME}?sslmode=verify-full"


def download_tls_certificate():
    _cert_url = 'https://cockroachlabs.cloud/clusters/d941e2cf-f8bf-4eb0-a015-f9cba09d25e5/cert'

    _cert_file = "root.crt"

    if platform.system() == "Windows":
        _postgresql_dir = os.path.join(os.getenv('APPDATA'), 'postgresql')

    else:
        _postgresql_dir = os.path.join(os.getenv("HOME"), ".postgresql")

    os.makedirs(_postgresql_dir, exist_ok=True)

    if os.path.exists(os.path.join(_postgresql_dir, _cert_file)):
        print("Certificate already exists")
    else:
        import requests

        cert_path = os.path.join(_postgresql_dir, _cert_file)
        response = requests.get(_cert_url)
        with open(cert_path, 'wb') as f:
            f.write(response.content)

    # Download the certificate and save it to the directory


download_tls_certificate()
