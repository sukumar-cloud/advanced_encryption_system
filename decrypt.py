import numpy as np
from PIL import Image
from Cryptodome.Cipher import AES
from base64 import b64decode
import itertools
import traceback

def get_list_from_key(image_path):
    im = Image.open(image_path)
    return list(im.getdata())

def extract_bytes_from_tuple(list_of_tuples, start, length):
    bytelist = list(itertools.chain(*list_of_tuples))
    return bytes(bytelist[start:start+length])

def decrypt_with_user_key(user_key, image_path):
    try:
        # Get pixels from the encrypted image
        str_pixels = get_list_from_key(image_path)
        NONCE = extract_bytes_from_tuple(str_pixels, 0, 15)
        MAC = extract_bytes_from_tuple(str_pixels, 16, 16)

        # Get pixels from the user key image
        user_key_pixels = get_list_from_key(user_key)
        AES_key = extract_bytes_from_tuple(user_key_pixels, 0, 16)

        str_list = []
        skip = 0

        for i in str_pixels:
            if skip < 8:  # Skipping NONCE and MAC values
                skip += 1
                continue
            if i != (0, 0, 0, 0):
                str_list.append(chr(user_key_pixels.index(i)))

        # Convert extracted characters back to a string
        encrypted_string = "".join(str_list)
        ciphertxt = b64decode(encrypted_string)

        # Decrypt the message
        cipher = AES.new(AES_key, AES.MODE_OCB, NONCE)
        source_string = cipher.decrypt_and_verify(ciphertxt, MAC).decode()

        return True, source_string
    except Exception as e:
        traceback.print_exc()
        return False, ""
