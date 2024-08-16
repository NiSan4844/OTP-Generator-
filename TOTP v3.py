import pyotp
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from cryptography.fernet import Fernet
from dotenv import load_dotenv


load_dotenv()

# Email configuration (loaded from environment variables)
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT'))
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

# File paths to store the encrypted secret key and encryption key
secret_file = "totp_secret.enc"
encryption_key_file = "encryption.key"

# Function to generate and save the encryption key
def generate_encryption_key():
    key = Fernet.generate_key()
    with open(encryption_key_file, "wb") as f:
        f.write(key)
    return key

# Function to load the encryption key
def load_encryption_key():
    if os.path.exists(encryption_key_file):
        with open(encryption_key_file, "rb") as f:
            return f.read()
    return None

# Function to encrypt and save the secret key to a file
def save_encrypted_secret(secret, key):
    fernet = Fernet(key)
    encrypted_secret = fernet.encrypt(secret.encode())
    with open(secret_file, "wb") as f:
        f.write(encrypted_secret)

# Function to load and decrypt the secret key from a file
def load_encrypted_secret(key):
    if os.path.exists(secret_file):
        with open(secret_file, "rb") as f:
            encrypted_secret = f.read()
        fernet = Fernet(key)
        return fernet.decrypt(encrypted_secret).decode()
    return None

# Function to send an email with the TOTP
def send_email(subject, body, recipient_email):
    message = MIMEMultipart()
    message['From'] = SENDER_EMAIL
    message['To'] = recipient_email
    message['Subject'] = subject

    # Add the body to the email
    message.attach(MIMEText(body, 'plain'))

    try:
        # Create a secure connection with the SMTP server and send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Upgrade to secure connection
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = message.as_string()
        server.sendmail(SENDER_EMAIL, recipient_email, text)
        server.quit()
        print(f"Email sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Step 1: Load or generate encryption key
encryption_key = load_encryption_key()
if not encryption_key:
    encryption_key = generate_encryption_key()
    print("A new encryption key has been generated and saved.")
else:
    print("Loaded existing encryption key.")

# Step 2: Load or generate TOTP secret
secret = load_encrypted_secret(encryption_key)

if not secret:
    secret = pyotp.random_base32()
    save_encrypted_secret(secret, encryption_key)
    print("A new secret key has been generated, encrypted, and saved.")
else:
    print("Loaded existing encrypted secret key.")

# Step 3: Create a TOTP object using the secret key
totp = pyotp.TOTP(secret)

# Step 4: Generate a TOTP and send it via email
current_otp = totp.now()
email_subject = "OTP code"
email_body = f"Your OTP code is: {current_otp}"
send_email(email_subject, email_body, RECIPIENT_EMAIL)

# Step 5: Simulate a delay (e.g., user taking time to input the OTP)
time.sleep(5)

# Step 6: User enters the OTP (in a real-world scenario, this would come from the user's input)
user_otp = input("Enter the OTP you received via email: ")

# Step 7: Validate the entered OTP with a window tolerance
if totp.verify(user_otp, valid_window=1):  # 1 interval before or after
    print("The OTP is valid!")
else:
    print("The OTP is invalid!")