import numpy as np
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

def generate_initial_vector(tent_map_length=128):
    # Tent map based IV generation
    X0 = np.random.rand()  # Random initial value for Tent map
    IV = []
    for _ in range(tent_map_length // 8):
        X0 = 2 * X0 if X0 < 0.5 else 2 * (1 - X0)
        IV.append(int(X0 * 255))
    return bytes(IV)

def pad_image(image_data):
    # Pad the image dimensions to be a multiple of 16
    h, w = image_data.shape
    new_h = h if h % 16 == 0 else (h // 16 + 1) * 16
    new_w = w if w % 16 == 0 else (w // 16 + 1) * 16
    padded_image = np.zeros((new_h, new_w), dtype=np.uint8)
    padded_image[:h, :w] = image_data
    return padded_image, (h, w)

def encrypt_image(image_path, key):
    # Load image and convert to grayscale
    image = Image.open(image_path).convert('L')
    image_data = np.array(image)

    # Pad the image so its dimensions are multiples of 16
    padded_image, original_shape = pad_image(image_data)

    # Prepare AES cipher in CBC mode
    iv = generate_initial_vector()
    key_hash = hashlib.sha256(key.encode()).digest()[:16]
    cipher = AES.new(key_hash, AES.MODE_CBC, iv)

    # Flatten the padded image and convert to bytes
    image_data_bytes = padded_image.tobytes()

    # Pad the byte data to a multiple of 16 bytes
    padded_image_data = pad(image_data_bytes, AES.block_size)

    # Encrypt the padded byte data
    encrypted_image_data = cipher.encrypt(padded_image_data)

    # Return the encrypted data, IV, and image shapes
    return encrypted_image_data, iv, padded_image.shape, original_shape

def decrypt_image(encrypted_image_data, iv, key, padded_shape, original_shape):
    # Prepare AES cipher in CBC mode
    key_hash = hashlib.sha256(key.encode()).digest()[:16]
    cipher = AES.new(key_hash, AES.MODE_CBC, iv)

    # Decrypt the byte data
    decrypted_image_data = cipher.decrypt(encrypted_image_data)

    # Unpad the decrypted byte data
    unpadded_image_data = unpad(decrypted_image_data, AES.block_size)

    # Convert the decrypted byte data back to a numpy array
    decrypted_image_array = np.frombuffer(unpadded_image_data, dtype=np.uint8)

    # Reshape the numpy array to match the padded image shape
    decrypted_image = np.reshape(decrypted_image_array, padded_shape)

    # Crop the image back to the original size
    h, w = original_shape
    decrypted_image_cropped = decrypted_image[:h, :w]

    return decrypted_image_cropped

# Example usage:
image_path = r"C:\Users\Manjusha\Desktop\mini\input_image.jpg.jpeg"  # Replace with your image path
key = "your_secret_key"

try:
    encrypted_image_data, iv, padded_shape, original_shape = encrypt_image(image_path, key)
    print("Encrypted image data size:", len(encrypted_image_data))

# Encrypt the image
    encrypted_image_data, iv, padded_shape, original_shape = encrypt_image(image_path, key)

# Save encrypted image data to a binary file for inspection
    encrypted_image_path = r"C:\Users\Manjusha\Desktop\mini\encrypted_image.bin"
    with open(encrypted_image_path, 'wb') as f:
       f.write(encrypted_image_data)
    print(f"Encrypted image data saved as {encrypted_image_path}")

# Decrypt the image
    decrypted_image = decrypt_image(encrypted_image_data, iv, key, padded_shape, original_shape)

# Save the decrypted image
    decrypted_image_pil = Image.fromarray(decrypted_image)
    output_path = r"C:\Users\Manjusha\Desktop\mini\decrypted_image.jpg"
    decrypted_image_pil.save(output_path)
    print(f"Decrypted image saved as {output_path}")
except Exception as e:
    print(f"Error saving image: {e}")

