from flask import Flask, render_template, request, redirect, send_file, flash
from werkzeug.utils import secure_filename
import os
from stegano.lsb import hide, reveal
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'rahasia_banget'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Fungsi Caesar Cipher
def encrypt(text, shift):
    result = ''
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def decrypt(text, shift):
    result = ''
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base - shift) % 26 + base)
        else:
            result += char
    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt_route():
    if 'image' not in request.files:
        flash('Gambar tidak ditemukan.')
        return redirect('/')

    image = request.files['image']
    message = request.form.get('message')
    shift = request.form.get('shift')

    if not image or not message or not shift:
        flash('Semua field harus diisi.')
        return redirect('/')

    try:
        shift = int(shift)
    except ValueError:
        flash('Shift harus berupa angka.')
        return redirect('/')

    encrypted_msg = encrypt(message, shift)
    filename = secure_filename(image.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(path)

    output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"steg_{filename}")
    secret = hide(path, encrypted_msg)
    secret.save(output_path)

    return render_template('index.html', encrypted_image=output_path)

@app.route('/decrypt', methods=['POST'])
def decrypt_route():
    if 'image' not in request.files:
        flash('Gambar tidak ditemukan.')
        return redirect('/')

    image = request.files['image']
    shift = request.form.get('shift')

    if not image or not shift:
        flash('Semua field harus diisi.')
        return redirect('/')

    try:
        shift = int(shift)
    except ValueError:
        flash('Shift harus berupa angka.')
        return redirect('/')

    filename = secure_filename(image.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(path)

    try:
        hidden_msg = reveal(path)
        if hidden_msg:
            decrypted_msg = decrypt(hidden_msg, shift)
        else:
            decrypted_msg = "Tidak ada pesan ditemukan."
    except Exception as e:
        decrypted_msg = f"Terjadi kesalahan: {str(e)}"

    return render_template('index.html', decrypted_message=decrypted_msg)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
