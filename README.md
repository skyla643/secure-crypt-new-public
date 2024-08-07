# Secure-Crypt-New-Public

## Overview
This repository contains a set of scripts for encrypting and decrypting messages, as well as sending encrypted messages via email. The main functionality includes generating encryption keys, encrypting messages, decrypting messages, and sending encrypted messages as email attachments.

## Files
- `LICENSE`
- `README.md`
- `What your terminal would look like`
- `decryptyourmessage.py`
- `emailencryptsender.py`
- `encrypted_message.txt`
- `encryption_key.txt`

## How to Use

### Setup and Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/skyla643/secure-crypt-new-public.git
   cd secure-crypt-new-public
   ```

2. **Install Required Modules:**
   Make sure you have the required modules installed. If not, install them using pip.
   ```bash
   pip install cryptography
   pip install smtplib
   pip install email
   ```

### File Descriptions and Usage

#### `emailencryptsender.py`
This script handles the encryption of messages and sends the encrypted message via email.

**Steps to Use:**
1. **Generate or Load Encryption Key:**
   - The script will generate a new encryption key if one doesn't exist and save it to `encryption_key.txt`.
   - If `encryption_key.txt` already exists, it will load the existing key, in other words will also generate automatically. 

2. **Encrypt Message:**
   - Input your message to be encrypted.
   - The message will be encrypted using the generated or loaded key.

3. **Save Encrypted Message:**
   - The encrypted message will be saved to `encrypted_message.txt`.

4. **Send Encrypted Message via Email:**
   - Enter the recipient's email address.
   - The script will send the encrypted message as an email attachment.

**Running the Script:**
```bash
python emailencryptsender.py
```

**Script Structure:**
```python
from email.mime.application import MIMEApplication
import os
import sys
from cryptography.fernet import Fernet
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Check if required modules are installed
required_modules = ['cryptography', 'smtplib', 'email']
for module in required_modules:
    if module not in sys.modules:
        print(f"Module '{module}' is not installed. Please run 'pip install {module}' to install it.")
        sys.exit(1)

def generate_key(key_file):
    """Generate a new encryption key and save it to a file."""
    key = Fernet.generate_key()
    with open(key_file, "wb") as key_file:
        key_file.write(key)
    return key

def load_key(key_file):
    """Load an encryption key from a file."""
    try:
        with open(key_file, "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        print(f"Encryption key file '{key_file}' not found.")
        return None

def encrypt_message(message, key):
    """Encrypt a message using the provided key."""
    try:
        fernet = Fernet(key)
        return fernet.encrypt(message.encode())
    except Exception as e:
        print(f"Failed to encrypt message: {e}")
        return None

def decrypt_message(encrypted_message, key):
    """Decrypt an encrypted message using the provided key."""
    try:
        fernet = Fernet(key)
        return fernet.decrypt(encrypted_message).decode()
    except Exception as e:
        print(f"Failed to decrypt message: {e}")
        return None

def send_email(recipient_email, encrypted_message):
    try:
        # Set email credentials
        sender_email = "your_email@example.com"
        app_password = "your_app_password"

        # Set up the server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, app_password)

        # Create the email
        msg = MIMEMultipart()
        msg['Subject'] = 'Emrald says hi :)'
        msg['From'] = sender_email
        msg['To'] = recipient_email

        # Add a text part to the message
        text_part = MIMEText("Encrypted message attached.")
        msg.attach(text_part)

        # Attach the encrypted message as a file
        attachment = MIMEApplication(encrypted_message)
        attachment['Content-Disposition'] = 'attachment; filename="encrypted_message.txt"'
        msg.attach(attachment)

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def save_encrypted_message(encrypted_message, filename="encrypted_message.txt"):
    """Save an encrypted message to a file."""
    try:
        with open(filename, "wb") as encrypted_file:
            encrypted_file.write(encrypted_message)
        print(f"Encrypted message saved to '{filename}'.")
    except Exception as e:
        print(f"Failed to save encrypted message: {e}")

def load_encrypted_message(filename="encrypted_message.txt"):
    """Load an encrypted message from a file."""
    try:
        with open(filename, "rb") as encrypted_file:
            return encrypted_file.read()
    except FileNotFoundError:
        print(f"Encrypted message file '{filename}' not found.")
        return None

def main():
    key_file = "encryption_key.txt"
    if not os.path.exists(key_file):
        key = generate_key(key_file)
    else:
        key = load_key(key_file)

    if not key:
        print("Failed to load or generate key.")
        return

    recipient_email = input("Enter recipient email: ")
    message = input("Enter your message: ")

    encrypted_message = encrypt_message(message, key)

    if not encrypted_message:
        print("Failed to encrypt message.")
        return

    save_encrypted_message(encrypted_message)

    send_email(recipient_email, encrypted_message)

    # Optionally, decrypt the message to verify
    loaded_encrypted_message = load_encrypted_message()
    if loaded_encrypted_message:
        decrypted_message = decrypt_message(loaded_encrypted_message, key)
        if decrypted_message:
            print("Decrypted message to verify: ", decrypted_message)

if __name__ == "__main__":
    main()
```

### `decryptyourmessage.py`
This script decrypts the encrypted message using the provided key.

**Steps to Use:**
1. **Load Encrypted Message:**
   - Ensure you have the encrypted message and the key used for encryption.

2. **Decrypt Message:**
   - Input the encrypted message and key into the script to decrypt the message.

**Running the Script:**
```bash
python decryptyourmessage.py
```

**Script Structure:**
```python
from cryptography.fernet import Fernet

# Your encrypted message
encrypted_message = b'your_encrypted_message_here'

# Your key (it should be the same key that was used to encrypt the message)
key = b'your_key_here'

# Initialize the Fernet class
cipher_suite = Fernet(key)

# Decrypt the message
decrypted_message = cipher_suite.decrypt(encrypted_message)

print(decrypted_message.decode())
```

### Terminal View
"Your terminal file path and log":
```plaintext
Enter recipient email: your email <--- you would type it in here!
Enter your message: hello this is a test. <----- you would write your message here
Encrypted message saved to 'encrypted_message.txt'. <----will automatically make this after you write your message.
Email sent successfully! <-------- check the confirmation if the email you messaged received the email.
Decrypted message to verify:  hello this is a test. <------ will tell you what your message is again, basically will tell you what the message will look like after decrypted.
```

"Your terminal file path and log":
```plaintext
hello this is a test. <---------This is what the decryptyourmessage.py file will put out when you enter the encrypted message and key in the decryptyourmessage.py code!
```

# How to set up the "back machine" 

## Setting Email Credentials

You might have questions regarding this small piece of code that could throw you off if you're not familiar with it:

```python
# Set email credentials
sender_email = # your email will go here
app_password = # your app password would go here
```

### Inputting Your Email

- **Sender Email:** 
  - `sender_email = "your_email@gmail.com"`
  - Simply replace `"your_email@gmail.com"` with your actual Gmail address.
  - Note: This script is currently set up for Gmail. If you want to use another email service, you'll need to modify the SMTP server settings accordingly.

### Avoiding Spam Folder

- **Spam Warning:**
  - The email might go to the spam folder initially. 
  - Check your spam folder and mark the email as "Not Spam" or "Allow." 
  - This should ensure that future emails go to the main inbox.

### Setting the App Password

Here's where it gets tricky:

```python
app_password = # your app password would go here
```

- **App Password:**
  - An App Password is a 16-digit code generated by Google for accessing your account from less secure apps or devices.
  - This is not your regular Google account password.

### What is an App Password in Google Services?

An App Password is a 16-digit code generated by Google that allows less secure apps or devices to access your Google account. It is used when an app or device doesn't support two-factor authentication (2FA).

### Why Use an App Password?

When you enable 2FA for your Google account, you add an extra layer of security. However, some apps and devices might not be compatible with 2FA. In such cases, instead of your regular password, you use an App Password to log in securely.

### How to Generate an App Password

1. **Log in to your Google Account:**
   - Go to [myaccount.google.com](https://myaccount.google.com) and sign in with your Google credentials.

2. **Navigate to Security Settings:**
   - Click on "Security" in the left-hand menu.

3. **Set Up 2-Step Verification:**
   - Ensure 2-Step Verification is turned on. If not, follow the instructions to set it up.

4. **Generate an App Password:**
   - Under "Signing in to Google," click on "App Passwords."
   - You may need to sign in again.
   - Select the app and device you want to generate the password for from the dropdown menus.
   - Click "Generate."

5. **Use the App Password:**
   - A 16-digit code will appear. Use this code in place of your regular password for the app or device.

### Example Usage

Let's say you're setting up an email client that doesn't support 2FA:
- During the account setup, when prompted for your Google password, enter the 16-digit App Password instead.
- This allows the email client to access your Google account securely.

### Important Notes

- **Single Use:** An App Password is typically used once per app or device. You don't need to remember it.
- **Security:** Keep your App Passwords secure and only generate them for trusted apps or devices.
- **Revocation:** You can revoke App Passwords anytime from your Google Account's security settings.

By using App Passwords, you maintain your account's security while allowing access to apps and devices that might not fully support advanced security features.

This should make the code snippet a bit clearer and more manageable.

---

### Personal Note

This explanation is meant to make the concept of App Passwords as clear as possible. Sometimes, setting up secure communication can feel more complicated than a tough relationship, but with the right steps, it becomes straightforward and secure.

- With love SMRCCC3301
