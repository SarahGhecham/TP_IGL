from django.test import TestCase

# Create your tests here.
# Importer la fonction depuis votre fichier utilitaire (qr_utils.py)
from qr_utils import scan_qr_code,generate_qr_code

import os

nss = "124-45-6789"
generate_qr_code(nss)
image_path = fr"api\qr_imgs\{nss}_qr.png"
nss2=scan_qr_code(image_path)


print(f"QR Code decode pour NSS: {nss2}")

