from cryptography.fernet import Fernet

# Your encrypted message
encrypted_message = # your message that you got via email

# Your key (it should be the same key that was used to encrypt the message)
key = # key goes here <-------  # Replace with your actual key

# Initialize the Fernet class
cipher_suite = Fernet(key)

# Decrypt the message
decrypted_message = cipher_suite.decrypt(encrypted_message)

print(decrypted_message.decode())