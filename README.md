# TOTP Authentication System

This project implements a Time-based One-Time Password (TOTP) authentication system using Python. The system handles generating, encrypting, storing, and verifying TOTP and includes functionality to send OTPs via email.

## Features

- **Generate TOTP Secret**: Create a new TOTP secret key.
- **Encrypt and Store Secret**: Securely encrypt and save the TOTP secret key.
- **Send OTP via Email**: Send the generated OTP to a user via email.
- **Verify OTP**: Validate the OTP entered by the user.

## Steps Involved

1. **Generate Encryption Key**:
   - Generate a new encryption key for encrypting the TOTP secret.
   - Save this key to a file for future use.

2. **Load Encryption Key**:
   - Load the encryption key from the saved file if it exists.
   - Generate a new key if none is found.

3. **Generate and Save TOTP Secret**:
   - Generate a new TOTP secret key if one does not already exist.
   - Encrypt the secret using the encryption key.
   - Save the encrypted secret to a file.

4. **Send OTP via Email**:
   - Generate a TOTP based on the secret key.
   - Send the OTP to the user's email address.

5. **Validate OTP**:
   - Prompt the user to enter the OTP received via email.
   - Verify the entered OTP against the generated one using a tolerance window.

## Configuration

### Email Configuration

Update the following variables in the script to match your email server details and credentials:

- `SMTP_SERVER`: The address of the SMTP server (e.g., `smtp.gmail.com`).
- `SMTP_PORT`: The port used by the SMTP server (e.g., `587` for TLS).
- `SENDER_EMAIL`: The email address used to send OTPs.
- `SENDER_PASSWORD`: The application-specific password for the email account.
- `RECIPIENT_EMAIL`: The email address to which the OTP will be sent.

### Environment Variables

For security reasons, sensitive information such as email server details and credentials should be managed using environment variables. Create a .env file in the root directory of the project with the following content:

- SMTP_SERVER=smtp.gmail.com         # Address of the SMTP server
- SMTP_PORT=587                      # Port used by the SMTP server
- SENDER_EMAIL=your_email@gmail.com  # Email address used to send OTPs
- SENDER_PASSWORD=your_password      # Application-specific password for the email account
- RECIPIENT_EMAIL=recipient_email@gmail.com  # Email address to which the OTP will be sent

Ensure that the .env file is included in your .gitignore to prevent it from being committed to version control.

The script uses the python-dotenv package to load environment variables from the .env file. Ensure this package is installed, and add the following code to your script to load the variables:


load_dotenv()

SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT'))
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

## Security Considerations

- **Encryption Key**: Ensure the encryption key is stored securely and not exposed in your code or repository.
- **Email Credentials**: Use application-specific passwords for email and manage credentials securely.
- **Time Synchronization**: Ensure that your system clock is accurate to avoid OTP validation issues.