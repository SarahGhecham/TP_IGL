import qrcode
import cv2
from PIL import Image
import os

def generate_qr_code(nss):
    # Créer un QR Code avec le NSS
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(nss)
    qr.make(fit=True)

    # Créer une image du QR Code
    img = qr.make_image(fill='black', back_color='white')
    img.save(fr"api\qr_imgs\{nss}_qr.png")

# Décodage du QR Code
def scan_qr_code(image_path):
    # Charger l'image
    if not os.path.exists(image_path):
      print("Erreur: Le fichier  n'existe pas.")
    else:
      print("Le fichier existe.")
    img = cv2.imread(image_path)

    # Vérifier si l'image a été chargée correctement
    if img is None:
        print(f"Erreur: Impossible de charger l'image à partir de {image_path}")
        return None

    detector = cv2.QRCodeDetector()

    # Utilisation de la méthode detectAndDecode pour détecter et décoder le QR Code
    value, pts, qr_code = detector.detectAndDecode(img)

    if value:
        print(f"QR Code trouvé: {value}")
        return value
    else:
        print("Aucun QR Code trouvé.")
        return None


if __name__ == "__main__":
    nss = "12345678901234567890"
    generate_qr_code(nss)
    print(f"QR Code généré pour le NSS: {nss}")