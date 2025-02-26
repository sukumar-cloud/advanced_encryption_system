import numpy as np
from PIL import Image
from uuid import uuid4
from math import sqrt, floor
from Cryptodome.Cipher import AES
from Cryptodome import Random
from base64 import b64encode
import itertools
import random
import os

# Ensure the static folder exists
STATIC_FOLDER = "static"
os.makedirs(STATIC_FOLDER, exist_ok=True)

def byte_to_tuples(tuple_size, byte_string, fill_value=None):
    return list(itertools.zip_longest(*[iter(byte_string)] * tuple_size, fillvalue=fill_value))

def generate_random_pixelTuple(backlog):
    upper_limit = 256 ** 4
    index = random.randint(1, upper_limit)
    while index in backlog:
        index = random.randint(1, upper_limit)

    red = floor(index / 256 ** 3)
    green = floor(index % 256 ** 3 / 256 ** 2)
    blue = floor(index % 256 ** 2 / 256)
    alpha = index % 256 ** 2 % 256
    return (red, green, blue, alpha), index

def create_user_key(uuid):
    print('Generating User Key...')
    random.seed(uuid)
    AES_key = Random.get_random_bytes(AES.key_size[0])
    AESls = byte_to_tuples(4, AES_key, 0)

    max_it = 1114112
    w = int(sqrt(max_it)) + 1
    pixels = []
    backlog = set()
    fresh = [None] * w
    count = 0
    total = 0

    for i in AESls:
        fresh[count] = i
        count += 1
        total += 1

    while total < max_it:
        if count == w:
            pixels.append(fresh)
            fresh = [None] * w
            count = 0
        fresh[count], index = generate_random_pixelTuple(backlog)
        backlog.add(index)
        count += 1
        total += 1

    array = np.array(pixels, dtype=np.uint8)
    new_image = Image.fromarray(array, 'RGBA')
    
    user_key_path = os.path.join(STATIC_FOLDER, 'user_key.png')
    new_image.save(user_key_path)
    
    print(f'User Key Generated Successfully! Saved at: {user_key_path}')

def get_list_from_key(image_path):
    im = Image.open(image_path)
    return list(im.getdata())

def encrypt_w_user_key(key_list, source_string):
    source_string = source_string.encode()
    try:
        NONCE = Random.get_random_bytes(15)
        NONCEls = byte_to_tuples(4, NONCE, 0)
        AES_key = bytes(itertools.chain.from_iterable(key_list[:4]))[:16]
        cipher = AES.new(AES_key, AES.MODE_OCB, NONCE)
        ciphertxt, MAC = cipher.encrypt_and_digest(source_string)
        MACls = byte_to_tuples(4, MAC, 0)
        encrypted_string = b64encode(ciphertxt).decode()
    except Exception as e:
        return False, str(e)

    try:
        w = int(sqrt(len(encrypted_string))) + 1
        pixels = []
        fresh = [None] * w
        count = 0

        for i in NONCEls + MACls:
            if count == w:
                pixels.append(fresh)
                fresh = [None] * w
                count = 0
            fresh[count] = i
            count += 1

        for i in encrypted_string:
            if count == w:
                pixels.append(fresh)
                fresh = [None] * w
                count = 0
            fresh[count] = key_list[ord(i)]
            count += 1

        pixels.append(fresh)

        while count < w:
            pixels[-1][count] = (0, 0, 0, 0)
            count += 1

        array = np.array(pixels, dtype=np.uint8)
        img = Image.fromarray(array, 'RGBA')

        encrypted_image_path = os.path.join(STATIC_FOLDER, "encrypted_image.png")
        img.save(encrypted_image_path)

        return True, encrypted_image_path
    except Exception as e:
        return False, str(e)