
from __future__ import division, print_function, unicode_literals
import sys
import random
import argparse
import logging
from tkinter import *
from tkinter import filedialog as tkFileDialog
from tkinter import messagebox as tkMessageBox
import os
import PIL
from PIL import Image
import math
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import binascii
import matplotlib.pyplot as plt
import time
import numpy as np
def generate_initial_vector(tent_map_length=128):
    X0 = np.random.rand()  # Random initial value for Tent map
    IV = []
    for _ in range(tent_map_length // 8):
        X0 = 2 * X0 if X0 < 0.5 else 2 * (1 - X0)
        IV.append(int(X0 * 255))
    return bytes(IV)

def pad_image(image_data):
    h, w, c = image_data.shape
    new_h = h if h % 16 == 0 else (h // 16 + 1) * 16
    new_w = w if w % 16 == 0 else (w // 16 + 1) * 16
    padded_image = np.zeros((new_h, new_w, c), dtype=np.uint8)
    padded_image[:h, :w, :] = image_data
    return padded_image, (h, w, c)

def encrypt_image(image_path, key):
    image = Image.open(image_path).convert('RGB')
    image_data = np.array(image)
    padded_image, original_shape = pad_image(image_data)
    iv = generate_initial_vector()
    key_hash = hashlib.sha256(key.encode()).digest()[:16]
    cipher = AES.new(key_hash, AES.MODE_CBC, iv)
    image_data_bytes = padded_image.tobytes()
    padded_image_data = pad(image_data_bytes, AES.block_size)
    encrypted_image_data = cipher.encrypt(padded_image_data)
    encrypted_image_array = np.frombuffer(encrypted_image_data, dtype=np.uint8)
    encrypted_image_array = encrypted_image_array[:padded_image.size]
    encrypted_image_array = encrypted_image_array.reshape(padded_image.shape)
    return encrypted_image_data, iv, padded_image.shape, original_shape, encrypted_image_array

def decrypt_image(encrypted_image_data, iv, key, padded_shape, original_shape):
    key_hash = hashlib.sha256(key.encode()).digest()[:16]
    cipher = AES.new(key_hash, AES.MODE_CBC, iv)
    decrypted_image_data = cipher.decrypt(encrypted_image_data)
    unpadded_image_data = unpad(decrypted_image_data, AES.block_size)
    decrypted_image_array = np.frombuffer(unpadded_image_data, dtype=np.uint8)
    decrypted_image = np.reshape(decrypted_image_array, padded_shape)
    h, w, c = original_shape
    decrypted_image_cropped = decrypted_image[:h, :w, :]
    return decrypted_image_cropped

# Example usage:
image_path = r"image path"  # Replace with your image path
key = "your_secret_key"

try:
    # Encrypt the image and measure encryption time
    encrypt_times = []
    decrypt_times = []
    for _ in range(100):  # Loop for multiple samples to collect time data
        start = time.time()
        encrypted_image_data, iv, padded_shape, original_shape, encrypted_image_array = encrypt_image(image_path, key)
        encrypt_times.append(time.time() - start)

        # Decrypt the image and measure decryption time
        start = time.time()
        decrypted_image = decrypt_image(encrypted_image_data, iv, key, padded_shape, original_shape)
        decrypt_times.append(time.time() - start)

    # Save encrypted and decrypted images
    encrypted_image_pil = Image.fromarray(encrypted_image_array, 'RGB')
    encrypted_image_path = r"C:\Users\Manjusha\Desktop\mini\encrypted_image.png"
    encrypted_image_pil.save(encrypted_image_path)
    print(f"Encrypted image visual saved as {encrypted_image_path}")

    decrypted_image_pil = Image.fromarray(decrypted_image, 'RGB')
    output_path = r"C:\Users\Manjusha\Desktop\mini\decrypted_image.png"
    decrypted_image_pil.save(output_path)
    print(f"Decrypted image saved as {output_path}")

    # Display encrypted and decrypted images
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(encrypted_image_array)
    plt.title("Encrypted Image")
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(decrypted_image)
    plt.title("Decrypted Image")
    plt.axis('off')
    plt.show()  # Show image display

    # Separate graph for encryption and decryption times
    plt.figure()
    plt.plot(encrypt_times, label="Encryption Time", color='blue', marker='o')
    plt.plot(decrypt_times, label="Decryption Time", color='green', marker='x')
    plt.xlabel("Sample")
    plt.ylabel("Time (seconds)")
    plt.title("AES Image Encryption and Decryption Times")
    plt.legend()
    plt.show()  # Show timing graph separately

except Exception as e:
    print(f"Error: {e}")

# ---------------------
# GUI stuff starts here
# ---------------------

def pass_alert():
   tkMessageBox.showinfo("Password Alert","Please enter a password.")

def enc_success(imagename):
   tkMessageBox.showinfo("Success","Encrypted Image: " + imagename)

# image encrypt button event
def image_open():
    global file_path_e

    enc_pass = passg.get()
    if enc_pass == "":
        pass_alert()
    else:
        filename = tkFileDialog.askopenfilename()
        if not filename:
            return  # Handle case where no file is selected
        file_path_e = os.path.dirname(filename)
        encrypted_image_data, iv, padded_shape, original_shape, encrypted_image_array = encrypt_image(filename, enc_pass)
        encrypted_image_pil = Image.fromarray(encrypted_image_array, 'RGB')
        encrypted_image_path = os.path.join(file_path_e, "encrypted_image.png")
        encrypted_image_pil.save(encrypted_image_path)
        enc_success(encrypted_image_path)

        # Write metadata
        metadata_path = os.path.join(file_path_e, "encryption_metadata.txt")
        with open(metadata_path, "w") as metadata_file:
          metadata_file.write(f"{iv.hex()}\n")  # Write IV as a hex string
          metadata_file.write(f"{padded_shape}\n")
          metadata_file.write(f"{original_shape}\n")
        print(f"Encrypted Image Path: {encrypted_image_path}")
        print(f"Metadata Path: {metadata_path}")




# image decrypt button event
def cipher_open():
    global file_path_d

    dec_pass = passg.get()  # Get the decryption password from the input field
    if dec_pass == "":
        pass_alert()
    else:
        # Select encrypted image
        encrypted_image_path = tkFileDialog.askopenfilename(title="Select Encrypted Image")
        if not encrypted_image_path:
            return

        # Select metadata file
        metadata_path = tkFileDialog.askopenfilename(title="Select Metadata File")
        if not metadata_path:
            return

    try:
    # Load encrypted image data
      with open(encrypted_image_path, "rb") as f:
        encrypted_image_data = f.read()

    # Load metadata
      with open(metadata_path, "r") as metadata_file:
        iv_hex = metadata_file.readline().strip()
        padded_shape = eval(metadata_file.readline().strip())
        original_shape = eval(metadata_file.readline().strip())

      iv = bytes.fromhex(iv_hex)

    # Perform decryption
      decrypted_image = decrypt_image(encrypted_image_data, iv, dec_pass, padded_shape, original_shape)
      decrypted_image_pil = Image.fromarray(decrypted_image, 'RGB')

    # Save and display decrypted image
      decrypted_image_path = os.path.join(file_path_d, "decrypted_image.png")
      decrypted_image_pil.save(decrypted_image_path)
      tkMessageBox.showinfo("Success", f"Decrypted Image: {decrypted_image_path}")
    except Exception as e:
        print(f"Decryption error details: {e}")
        tkMessageBox.showerror("Error", f"Decryption failed: {e}")


class App:
  def __init__(self, master):
    global passg
    title = "Image Encryption and Decryption"
    author = "by AES in CBC mode"
    msgtitle = Message(master, text =title)
    msgtitle.config(font=('helvetica', 17, 'bold'), width=200)
    msgauthor = Message(master, text=author)
    msgauthor.config(font=('helvetica',10), width=200)

    canvas_width = 200
    canvas_height = 50
    w = Canvas(master,
           width=canvas_width,
           height=canvas_height)
    msgtitle.pack()
    msgauthor.pack()
    w.pack()

    passlabel = Label(master, text="Enter Encrypt/Decrypt Password:")
    passlabel.pack()
    passg = Entry(master, show="*", width=20)
    passg.pack()

    self.encrypt = Button(master,
                         text="Encrypt", fg="black",
                         command=image_open, width=25,height=5)
    self.encrypt.pack(side=LEFT)
    self.decrypt = Button(master,
                         text="Decrypt", fg="black",
                         command=cipher_open, width=25,height=5)
    self.decrypt.pack(side=RIGHT)


# ------------------ MAIN -------------#
root = Tk()
root.wm_title("Image Encryption and Decryption")
app = App(root)
root.mainloop()





