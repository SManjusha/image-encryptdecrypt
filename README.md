A Fast Image Encryption Scheme Based on AES
This repository contains the implementation of the paper "A Fast Image Encryption Scheme Based on AES" by Yong Zhang, Xueqian Li, and Wengang Hou. The system implements an efficient image encryption scheme using the Advanced Encryption Standard (AES) in Cipher Block Chaining (CBC) mode to ensure secure and fast encryption of images.

Abstract
This project demonstrates an image encryption system where the plain image is divided into 128-bit data blocks, with the first block permuted by an initial vector (IV). AES encryption is then applied in CBC mode. The initial vector and the ciphered image are transmitted to the decryption party over a public channel. Simulation results show that the proposed cryptosystem is both secure and high-speed, suitable for secure image transmission.

Features
AES Encryption in CBC Mode: Ensures security by chaining blocks, with each block's encryption depending on the previous one.
Fast Encryption: Achieves speeds superior to some chaotic encryption systems.
Resistance to Attacks: The use of IV ensures that different images encrypted with the same key will yield different cipher images, making it resistant to known-plaintext and chosen-plaintext attacks.
Secure Decryption: The secret key and initial vector (IV) are used by the decryption party to recover the original image.

![Screenshot 2024-09-17 140011](https://github.com/user-attachments/assets/2643ad4b-defd-4370-aeb9-9bc8f541603e)

![Screenshot 2024-09-17 141042](https://github.com/user-attachments/assets/3b1a6cc0-a2ff-4088-9a2a-a4926576322b)
python decrypt.py --image path/to/encrypted_image.png --key "your-secret-key" --iv "initial-vector"

![Screenshot 2024-09-17 141058](https://github.com/user-attachments/assets/b8b38d32-4b7c-4711-af3b-bb17fa654558)
python decrypt.py --image encrypted_sample_image.png --key "my128bitSecret" --iv "22,244,55,176,191,..."

![Screenshot 2024-09-17 141539](https://github.com/user-attachments/assets/7dbb60a4-5f7b-4e40-b2c2-f4f47bcdd3d5)
