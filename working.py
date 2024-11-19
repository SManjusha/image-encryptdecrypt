import numpy as np
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import matplotlib.pyplot as plt
import time

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
image_path = r"C:\Users\Manjusha\Desktop\mini\input_image.jpg.jpeg"  # Replace with your image path
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







