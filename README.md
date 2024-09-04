# OTP Authentication System

This project implements a Time-based One-Time Password (TOTP) authentication system. The system generates a TOTP, sends it to the user's email, and then validates the user input against the generated OTP. It includes rate limiting and logging functionalities to enhance security and monitor usage.

## Features

- **TOTP Generation**: Uses the `pyotp` library to generate a time-based OTP.
- **Email Sending**: Sends OTP via email using SMTP.
- **Encryption**: Stores and retrieves the TOTP secret key securely.
- **Rate Limiting**: Limits the number of attempts a user can make within a specified time window.
- **Logging**: Logs key actions and events for monitoring and debugging.

## Setup

1. **Install Required Libraries**: Ensure you have the required libraries installed. You can install them using pip:

    ```bash
    pip install pyotp python-dotenv cryptography
    ```

2. **Environment Variables**: Create a `.env` file in the project directory with the following variables:

    ```dotenv
    SMTP_SERVER=smtp.example.com
    SMTP_PORT=587
    SENDER_EMAIL=your_email@example.com
    SENDER_PASSWORD=your_password
    RECIPIENT_EMAIL=recipient_email@example.com
    ```

## Code Overview

### 1. Load Environment Variables

The `load_dotenv()` function loads environment variables from the `.env` file.

### 2. Email Configuration

Email settings are loaded from environment variables and used for sending OTP emails.

### 3. File Paths

- `secret_file`: Path to store the encrypted TOTP secret key.
- `encryption_key_file`: Path to store the encryption key.

### 4. Logging Setup

Logging is configured to record events and errors to `otp_auth.log`.

### 5. Rate Limiting Configuration

- `RATE_LIMIT_WINDOW`: Defines the time window for rate limiting.
- `MAX_ATTEMPTS`: Maximum number of allowed attempts within the window.

### 6. Functions

#### `generate_encryption_key()`

Generates and saves an encryption key for encrypting the TOTP secret.

#### `load_encryption_key()`

Loads the encryption key from a file.

#### `save_encrypted_secret(secret, key)`

Encrypts and saves the TOTP secret using the provided key.

#### `load_encrypted_secret(key)`

Loads and decrypts the TOTP secret using the provided key.

#### `send_email(subject, body, recipient_email)`

Sends an email with the given subject and body to the specified recipient using SMTP.

#### `is_rate_limited(user_id)`

Checks if the user has exceeded the maximum number of attempts within the rate limit window.

#### `log_attempt(user_id)`

Logs an attempt with the current timestamp for the given user ID.

### 7. Main Steps

1. **Load or Generate Encryption Key**: Checks if an encryption key exists; if not, generates a new one.
2. **Load or Generate TOTP Secret**: Loads the encrypted TOTP secret or generates a new one if not available.
3. **Create TOTP Object**: Uses the TOTP secret to create a TOTP object.
4. **Generate and Send OTP**: Generates the current OTP and sends it via email.
5. **Simulate Delay**: Waits to simulate user input time.
6. **User Input**: Prompts the user to enter the received OTP.
7. **Log Attempt and Validate OTP**: Logs the attempt, checks the rate limit, and validates the OTP.

## Security Considerations

- **Encryption**: The TOTP secret is encrypted before being saved to ensure confidentiality.
- **Rate Limiting**: Helps to prevent brute-force attacks by limiting the number of attempts.
- **Logging**: Records significant events and errors for troubleshooting and monitoring.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

