from email.mime.application import MIMEApplication
import os
import sys
from cryptography.fernet import Fernet
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart 

# Check if required modules are installed, this will run a printed statment on the terminal to see if you are missing a pip install for the from/import above.
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
        sender_email = # your email will go here
        app_password = # you app password would go here

        # Set up the server (usually automatically happen dont touch before first run.)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, app_password)

        # Create the email, you can edit the bellow to show diffrent messages when sending.
        msg = MIMEMultipart()
        msg['Subject'] = 'Emrald says hi :)'
        msg['From'] = sender_email
        msg['To'] = recipient_email

        # Add a text part to the message
        text_part = MIMEText("Encrypted message attached.") # paragraph for the message abov the encrypted attachment
        msg.attach(text_part)

        # Attach the encrypted message as a file, this will happen automatically, don't touch. 
        attachment = MIMEApplication(encrypted_message)
        attachment['Content-Disposition'] = 'attachment; filename="encrypted_message.txt"'
        msg.attach(attachment)

        # Send the email, will do automatically. 
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

    # Optionally, decrypt the message to verify, leave this alone unless you don't want a confirmation of the ecrypted message. 
    loaded_encrypted_message = load_encrypted_message()
    if loaded_encrypted_message:
        decrypted_message = decrypt_message(loaded_encrypted_message, key)
        if decrypted_message:
            print("Decrypted message to verify: ", decrypted_message)

if __name__ == "__main__":
    main()
