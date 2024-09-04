import pyotp
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import logging
from datetime import datetime, timedelta

# Load environment variables
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

# Setup logging
logging.basicConfig(filename='otp_auth.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Rate limiting configuration
RATE_LIMIT_WINDOW = timedelta(minutes=5)  # Time window for rate limiting
MAX_ATTEMPTS = 5  # Maximum attempts within the window
attempts = {}

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

    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Upgrade to secure connection
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = message.as_string()
        server.sendmail(SENDER_EMAIL, recipient_email, text)
        server.quit()
        logging.info(f"Email sent to {recipient_email}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

# Function to check rate limit
def is_rate_limited(user_id):
    now = datetime.now()
    if user_id in attempts:
        attempt_times = attempts[user_id]
        # Remove attempts outside the rate limit window
        attempt_times = [t for t in attempt_times if now - t <= RATE_LIMIT_WINDOW]
        attempts[user_id] = attempt_times

        if len(attempt_times) >= MAX_ATTEMPTS:
            return True

    return False

# Function to log an attempt
def log_attempt(user_id):
    now = datetime.now()
    if user_id not in attempts:
        attempts[user_id] = []
    attempts[user_id].append(now)
    logging.info(f"Attempt logged for user ID: {user_id}")

# Step 1: Load or generate encryption key
encryption_key = load_encryption_key()
if not encryption_key:
    encryption_key = generate_encryption_key()
    logging.info("A new encryption key has been generated and saved.")
else:
    logging.info("Loaded existing encryption key.")

# Step 2: Load or generate TOTP secret
secret = load_encrypted_secret(encryption_key)

if not secret:
    secret = pyotp.random_base32()
    save_encrypted_secret(secret, encryption_key)
    logging.info("A new secret key has been generated, encrypted, and saved.")
else:
    logging.info("Loaded existing encrypted secret key.")

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
user_id = "unique_user_id"  # Replace with actual user ID or session identifier
user_otp = input("Enter the OTP you received via email: ")

# Log the attempt
log_attempt(user_id)

# Step 7: Validate the entered OTP with a window tolerance and check rate limit
if is_rate_limited(user_id):
    print("Too many attempts. Please try again later.")
    logging.warning(f"Rate limit exceeded for user ID: {user_id}")
else:
    if totp.verify(user_otp, valid_window=1):  # 1 interval before or after
        print("The OTP is valid!")
        logging.info("The OTP is valid.")
    else:
        print("The OTP is invalid!")
        logging.warning("The OTP is invalid.")
