from uuid import uuid4
import os
from encrypt import create_user_key, get_list_from_key, encrypt_w_user_key
from decrypt import decrypt_with_user_key

if __name__ == "__main__":
    src_str = input("Enter the text to encrypt: ")

    # Generate or load user key
    if os.path.exists('user_key.png'):
        key_list = get_list_from_key('user_key.png')
    else:
        create_user_key(str(uuid4()))
        print("Run the program again to encrypt/decrypt the message.")
        exit(1)

    # Encrypt the message and store it in static folder
    result, encrypted_image_path = encrypt_w_user_key(key_list, src_str)
    if result:
        print(f'Encrypted message saved as: {encrypted_image_path}')
    else:
        print(f"Encryption failed: {encrypted_image_path}")
        exit(1)
