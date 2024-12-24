import os
from PIL import Image
import argparse

def get_size_format(b, factor=1024, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


def compress_img(image_name, new_size_ratio=1.0, quality=90, width=None, height=None, to_webp=False):
    if not os.path.exists(image_name):
        print(f"[!] Error: File not found: {image_name}")
        return
    try:
        img = Image.open(image_name)
    except Exception as e:
        print(f"[!] Error: Could not open image {image_name}: {e}")
        return
    print("[*] Image shape:", img.size)
    image_size = os.path.getsize(image_name)
    print("[*] Size before compression:", get_size_format(image_size))

    if new_size_ratio < 1.0:
        img = img.resize((int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)), Image.LANCZOS)
        print("[+] New Image shape:", img.size)
    elif width and height:
        img = img.resize((width, height), Image.LANCZOS)
        print("[+] New Image shape:", img.size)

    filename, ext = os.path.splitext(image_name)

    if to_webp:
        new_filename = f"{filename}_compressed.webp"
    else:
        new_filename = f"{filename}_compressed{ext}"

    try:
        if to_webp:
            img.save(new_filename, quality=quality, method=6)
        else:
           img.save(new_filename, quality=quality, optimize=True)
    except OSError:
        img = img.convert("RGB")
        if to_webp:
           img.save(new_filename, quality=quality, method=6)
        else:
           img.save(new_filename, quality=quality, optimize=True)

    print("[+] New file saved:", new_filename)
    new_image_size = os.path.getsize(new_filename)
    print("[+] Size after compression:", get_size_format(new_image_size))
    saving_diff = new_image_size - image_size
    print(f"[+] Image size change: {saving_diff/image_size*100:.2f}% of the original image size.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Python script for compressing and resizing images")
    parser.add_argument("image", help="Target image to compress and/or resize")
    parser.add_argument("-w", "--to-webp", action="store_true", help="Convert the image to the WebP format")
    parser.add_argument("-q", "--quality", type=int, help="Quality ranging from a minimum of 0 (worst) to a maximum of 95 (best). Default is 90", default=90)
    parser.add_argument("-r", "--resize-ratio", type=float, help="Resizing ratio from 0 to 1, setting to 0.5 will multiply width & height of the image by 0.5. Default is 1.0", default=1.0)
    parser.add_argument("-W", "--width", type=int, help="The new width image, make sure to set it with the height parameter")
    parser.add_argument("-H", "--height", type=int, help="The new height for the image, make sure to set it with the width parameter")
    args = parser.parse_args()

    print("="*50)
    print("[*] Image:", args.image)
    print("[*] To WebP:", args.to_webp)
    print("[*] Quality:", args.quality)
    print("[*] Resizing ratio:", args.resize_ratio)
    if args.width and args.height:
        print("[*] Width:", args.width)
        print("[*] Height:", args.height)
    print("="*50)
    compress_img(args.image,
                new_size_ratio=args.resize_ratio,
                quality=args.quality,
                width=args.width,
                height=args.height,
                to_webp=args.to_webp
                )
    print("="*50)
#python .\WEBP_Compression\WEBP_Compression.py .\WEBP_Compression\kotik_Sema.png -w -q 1