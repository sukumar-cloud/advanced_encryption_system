# import numpy as np
# from PIL import Image
# from Crypto.Cipher import AES
# from base64 import b64decode
# import itertools
# import traceback
# import os

# def get_list_from_key(image_path):
#     """Load pixel data from an image and return it as a list of RGBA tuples."""
#     if not os.path.exists(image_path):
#         print(f"Error: Image file {image_path} not found.")
#         return []
#     try:
#         im = Image.open(image_path)
#         return list(im.getdata())
#     except Exception as e:
#         print(f"Error loading image {image_path}: {e}")
#         return []

# def extract_bytes_from_tuple(list_of_tuples, start, length):
#     """Extract bytes from a list of tuples starting from 'start' index up to 'length' bytes."""
#     bytelist = list(itertools.chain(*list_of_tuples))
#     extracted_bytes = bytes(bytelist[start:start+length])
#     return extracted_bytes if len(extracted_bytes) == length else None

# def decrypt_with_user_key(user_key_path, encrypted_image_path):
#     """Decrypt the message from an encrypted image using the provided user key image."""
#     try:
#         # Load encrypted image pixels
#         encrypted_pixels = get_list_from_key(encrypted_image_path)
#         if not encrypted_pixels:
#             return False, "Error: Could not load encrypted image."

#         # Extract NONCE and MAC from the first few pixels
#         NONCE = extract_bytes_from_tuple(encrypted_pixels, 0, 15)
#         MAC = extract_bytes_from_tuple(encrypted_pixels, 16, 16)
#         if not NONCE or not MAC:
#             return False, "Error: Encrypted image is corrupted or incorrect."

#         # Load user key pixels
#         user_key_pixels = get_list_from_key(user_key_path)
#         if not user_key_pixels:
#             return False, "Error: Could not load user key image."

#         # Extract AES key from the first few user key pixels
#         AES_key = extract_bytes_from_tuple(user_key_pixels, 0, 16)
#         if not AES_key:
#             return False, "Error: User key image is invalid."

#         # Extract encrypted string from image pixels
#         str_list = []
#         skip = 8  # Skip NONCE and MAC pixels
#         error_count = 0  # Counter for invalid pixels
#         max_errors = 100  # Stop after 100 failures to prevent infinite loop

#         for i in encrypted_pixels[skip:]:
#             if i == (0, 0, 0, 0):  # Ignore padding pixels
#                 continue

#             try:
#                 index = user_key_pixels.index(i)
#                 str_list.append(chr(index))
#             except ValueError:
#                 error_count += 1
#                 if error_count > max_errors:
#                     return False, "Error: Too many invalid pixels in the encrypted image."
#                 continue  # Skip values not found in user key

#         # Convert extracted characters back to encrypted string
#         encrypted_string = "".join(str_list)
#         if not encrypted_string:
#             return False, "Error: Encrypted string extraction failed."

#         # Decode base64 encrypted text
#         try:
#             ciphertxt = b64decode(encrypted_string)
#         except Exception:
#             return False, "Error: Invalid base64 encoding."

#         # Decrypt the message using AES-OCB
#         try:
#             cipher = AES.new(AES_key, AES.MODE_OCB, NONCE)
#             decrypted_text = cipher.decrypt_and_verify(ciphertxt, MAC).decode()
#         except (ValueError, KeyError):
#             return False, "Error: Decryption failed. Possible incorrect key."

#         return True, decrypted_text
#     except Exception as e:
#         traceback.print_exc()
#         return False, f"Decryption failed: {e}"

# if __name__ == "__main__":
#     # User inputs encrypted image file path
#     encrypted_image_path = input("Enter the path of the encrypted image: ").strip()

#     # Ensure user key exists
#     user_key_path = "user_key.png"
#     if not os.path.exists(user_key_path):
#         print("Error: User key image not found.")
#     elif not os.path.exists(encrypted_image_path):
#         print("Error: Encrypted image not found.")
#     else:
#         # Attempt decryption
#         print("\nDecrypting...")
#         success, message = decrypt_with_user_key(user_key_path, encrypted_image_path)
#         if success:
#             print(f"Decrypted Message: {message}")
#         else:
#             print(f"Decryption failed: {message}")
