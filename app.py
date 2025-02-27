# # from flask import Flask, request, render_template
# # app = Flask(__name__)

# # @app.route('/')
# # def index():
# #     return render_template('index.html')

# # @app.route('/d')
# # def decrypt():
# #     return render_template('d.html')

# # if __name__ == '__main__':
# #     app.run(debug=True)

# from flask import Flask, render_template, request, send_from_directory, jsonify, url_for
# import os
# import numpy as np
# from PIL import Image
# from Crypto.Cipher import AES
# from Crypto import Random
# import itertools
# import base64

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'static'

# def byte_to_tuples(tuple_size, byte_string, fill_value=None):
#     return list(itertools.zip_longest(*[iter(byte_string)] * tuple_size, fillvalue=fill_value))

# def generate_encrypted_image(text):
#     try:
#         key = Random.get_random_bytes(16)  # AES key (128-bit)
#         cipher = AES.new(key, AES.MODE_EAX)
#         ciphertext, tag = cipher.encrypt_and_digest(text.encode())

#         encrypted_data = key + cipher.nonce + tag + ciphertext
#         pixel_data = byte_to_tuples(4, encrypted_data, 0)

#         img_size = int(np.ceil(np.sqrt(len(pixel_data))))
#         img_array = np.zeros((img_size, img_size, 4), dtype=np.uint8)

#         index = 0
#         for i in range(img_size):
#             for j in range(img_size):
#                 if index < len(pixel_data):
#                     img_array[i, j] = pixel_data[index]
#                     index += 1

#         img = Image.fromarray(img_array, 'RGBA')
#         img_path = os.path.join(app.config['UPLOAD_FOLDER'], 'encrypted_image.png')
#         img.save(img_path)

#         return img_path
#     except Exception as e:
#         print(f"Error: {e}")
#         return None

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/d')
# def decrypte():
#     return render_template('d.html')

# @app.route('/encrypt', methods=['POST'])
# def encrypt_text():
#     data = request.json
#     text = data.get('text', '')

#     if not text:
#         return jsonify({'error': 'No text provided'}), 400

#     img_path = generate_encrypted_image(text)
#     if img_path:
#         return jsonify({'image_url': url_for('static', filename='encrypted_image.png')})
#     else:
#         return jsonify({'error': 'Encryption failed'}), 500

# @app.route('/static/<path:filename>')
# def serve_static(filename):
#     return send_from_directory('static', filename)



# if __name__ == '__main__':
#     app.run(debug=True)
