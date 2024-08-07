from cryptography.fernet import Fernet

# Your encrypted message
encrypted_message = b"gAAAAABmssKTL4DhS2H_bht9tCttDuvrefM4T8JoPIqa79mxRR2QTsatO2Jj4GFqxs3Y1r-WKiz2gs_zNCaHwbfoxrbIewi0P_kkviOUw-8ucodBdXeMAgE="

# Your key (it should be the same key that was used to encrypt the message)
key = b'B814DKUFKNYPGUMWXbOjLUoaxb782zHR3DnemblOYBE='  # Replace with your actual key

# Initialize the Fernet class
cipher_suite = Fernet(key)

# Decrypt the message
decrypted_message = cipher_suite.decrypt(encrypted_message)

print(decrypted_message.decode())