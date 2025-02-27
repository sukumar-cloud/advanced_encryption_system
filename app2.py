import streamlit as st
import os
from encrypt import create_user_key, get_list_from_key, encrypt_w_user_key
from uuid import uuid4
from decrypt import decrypt_with_user_key
from PIL import Image

st.title("🔐 Text Encryption to Image using AES")

# Input text box
text_input = st.text_area("Enter text to encrypt:")

# Encrypt button
if st.button("Encrypt"):
    if text_input.strip():
        if os.path.exists('user_key.png'):
            key_list = get_list_from_key('user_key.png')
        else:
            create_user_key(str(uuid4()))
            st.error("User key created. Run the program again to encrypt/decrypt the message.")
            st.stop()

        result, encrypted_image_path = encrypt_w_user_key(key_list, text_input)

        if result:
            st.success("✅ Encryption Successful!")
            st.image(encrypted_image_path, caption="Encrypted Image", use_column_width=True)

            with open(encrypted_image_path, "rb") as file:
                st.download_button("📥 Download Encrypted Image", file, "encrypted_image.png", "image/png")
        else:
            st.error("Encryption failed!")
    else:
        st.warning("⚠️ Please enter some text to encrypt.")

# Upload encrypted image
uploaded_file = st.file_uploader("Upload the encrypted image", type=["png"])

if st.button("Decrypt"):
    if uploaded_file:
        user_key_path = "user_key.png"

        if not os.path.exists(user_key_path):
            st.error("Error: User key image not found.")
        else:
            # Save uploaded file as a temporary image
            temp_path = "temp_encrypted_image.png"
            image = Image.open(uploaded_file)
            image.save(temp_path)

            # Attempt decryption
            success, message = decrypt_with_user_key(user_key_path, temp_path)
            if success:
                st.success(f"🔓 Decrypted Message: {message}")
            else:
                st.error(f"❌ Decryption failed: {message}")

            # Cleanup temporary file
            os.remove(temp_path)
    else:
        st.warning("⚠️ Please upload an encrypted image.")
