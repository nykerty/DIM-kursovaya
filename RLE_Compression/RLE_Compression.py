from PIL import Image
import numpy as np
import argparse
import os

DIR_INPUT = "RLE_Compression/INPUT/"
DIR_OUT = "RLE_Compression/OUTPUT/"


def get_size_format(b, factor=1024, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


def rle_encode(image_array):
    """Кодирует изображение с помощью RLE."""
    pixels = image_array.flatten()
    if len(pixels) == 0:
      return []
    encoded_data = []
    count = 1
    current_pixel = pixels[0]
    
    for i in range(1, len(pixels)):
        if pixels[i] == current_pixel:
            count += 1
        else:
            encoded_data.append((current_pixel, count))
            current_pixel = pixels[i]
            count = 1
    encoded_data.append((current_pixel, count))
    print("[*]", get_size_format(np.array(encoded_data).size))
    return encoded_data


def rle_decode(encoded_data, original_shape):
    """Декодирует данные, закодированные с помощью RLE."""
    decoded_pixels = []
    for pixel, count in encoded_data:
        decoded_pixels.extend([pixel] * count)
    
    decoded_array = np.array(decoded_pixels)
    decoded_array = decoded_array.reshape(original_shape)
    return decoded_array


def compress_image_rle(image_path):
  try:
    img = Image.open(image_path)
    image_array = np.array(img)
    original_shape = image_array.shape

  except Exception as e:
    print(f"Error loading image: {e}")
    return None, None, None
    
  if len(original_shape) == 3: # Если это цветное изображение
    print("="*50)
    print("[!] Encoding color image")
    encoded_channels = []
    for channel in range(original_shape[2]): # проход по каналам rgb
      encoded_channels.append(rle_encode(image_array[:,:,channel]))
      
    return encoded_channels, original_shape, "color"
  else:
    print("[!] Unknown image format.")
    return None, None, None


def decompress_image_rle(encoded_data, original_shape, image_type):
    """Декодирует RLE-сжатое изображение."""
    if image_type == "color":
      decoded_channels = []
      for channel in encoded_data:
        decoded_channels.append(rle_decode(channel, original_shape[:2]))
      decoded_image = np.stack(decoded_channels, axis=2)
    elif image_type == "grayscale":
      decoded_image = rle_decode(encoded_data, original_shape)
    else:
      print("[!] Unknown image format during decompression")
      return None
    
    return Image.fromarray(decoded_image.astype(np.uint8))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Python script for compressing and resizing images")
    parser.add_argument("image", help="Target image to compress and/or resize")
    args = parser.parse_args()

    encoded_image, original_shape, image_type = compress_image_rle(args.image)

    print("[*] Image:", args.image)
    image_size = os.path.getsize(args.image)
    print("[*] Size before compression:", get_size_format(image_size))

    decoded_image = decompress_image_rle(encoded_image, original_shape, image_type)
    if decoded_image:
      decoded_image.save(DIR_OUT + "decompressed_image.png") # Сохранение декодированного изображения

      print("[+] New file saved: .\RLE_Compression\OUTPUT\decompressed_image.png")
      new_image_size = os.path.getsize(DIR_OUT + "decompressed_image.png")
      saving_diff = new_image_size - image_size
      print("[+] Size after compression:", get_size_format(new_image_size))
      print(f"[+] Image size change: {saving_diff/image_size*100:.2f}% of the original image size.")  

    print("="*50)
#python .\RLE_Compression\RLE_Compression.py .\RLE_Compression\INPUT\kotik_Sema.png