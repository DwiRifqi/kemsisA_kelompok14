from PIL import Image

def encode_image(image_path, message, output_path):
    img = Image.open(image_path)
    binary_msg = ''.join(format(ord(c), '08b') for c in message) + '1111111111111110'
    pixels = list(img.getdata())

    new_pixels = []
    msg_index = 0
    for pixel in pixels:
        r, g, b = pixel[:3]
        if msg_index < len(binary_msg):
            r = (r & ~1) | int(binary_msg[msg_index])
            msg_index += 1
        if msg_index < len(binary_msg):
            g = (g & ~1) | int(binary_msg[msg_index])
            msg_index += 1
        if msg_index < len(binary_msg):
            b = (b & ~1) | int(binary_msg[msg_index])
            msg_index += 1
        new_pixels.append((r, g, b))
        if len(pixel) == 4:
            new_pixels[-1] += (pixel[3],)

    img.putdata(new_pixels)
    img.save(output_path)

def decode_image(image_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    binary = ''

    for pixel in pixels:
        for color in pixel[:3]:
            binary += str(color & 1)

    bytes_list = [binary[i:i+8] for i in range(0, len(binary), 8)]
    message = ''
    for byte in bytes_list:
        if byte == '11111110':
            break
        message += chr(int(byte, 2))
    return message
