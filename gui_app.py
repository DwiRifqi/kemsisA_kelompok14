import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from crypto.caesar import encrypt, decrypt
from stegano_custom.lsb_local import encode_image, decode_image
import os
import threading

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 SteganoKripto GUI")
        self.root.geometry("700x550")
        self.root.configure(bg="#e0f7fa")  # Soft blue background

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", padding=10, font=("Segoe UI", 10, "bold"), background="#00796b", foreground="white")
        style.configure("TLabel", font=("Segoe UI", 10), background="#e0f7fa")
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#004d40", background="#e0f7fa")

        ttk.Label(root, text="🔒 Steganografi + Kriptografi", style="Header.TLabel").pack(pady=15)

        # Pesan input
        self.input_text = tk.Text(root, height=5, font=("Consolas", 11), bg="#ffffff", fg="#004d40", insertbackground="#004d40")
        self.input_text.pack(padx=30, pady=(0, 10), fill="x")

        # Shift input
        shift_frame = ttk.Frame(root)
        shift_frame.pack(pady=5)
        ttk.Label(shift_frame, text="Shift Caesar Cipher:").pack(side="left", padx=(0, 5))
        self.shift_entry = ttk.Entry(shift_frame, width=5)
        self.shift_entry.insert(0, "3")
        self.shift_entry.pack(side="left")

        # Tombol aksi
        ttk.Button(root, text="🔏 Enkripsi & Sembunyikan", command=self.encrypt_and_embed).pack(pady=12)
        ttk.Button(root, text="📥 Ambil & Dekripsi", command=self.decode_and_decrypt).pack(pady=5)

        # Hasil
        self.result_label = tk.Label(root, text="", bg="#e0f7fa", fg="#004d40",
                                     font=("Segoe UI", 11), wraplength=600, justify="left")
        self.result_label.pack(padx=30, pady=20)

    def encrypt_and_embed(self):
        threading.Thread(target=self._encrypt_and_embed_thread).start()

    def _encrypt_and_embed_thread(self):
        msg = self.input_text.get("1.0", "end-1c").strip()
        shift_text = self.shift_entry.get().strip()

        if not msg:
            self._show_error("Pesan tidak boleh kosong.")
            return

        if not shift_text.isdigit():
            self._show_error("Shift harus berupa angka.")
            return

        shift = int(shift_text)
        path = filedialog.askopenfilename(title="Pilih gambar PNG", filetypes=[("PNG Images", "*.png")])
        if not path:
            return

        out_path = filedialog.asksaveasfilename(defaultextension=".png", title="Simpan gambar hasil", filetypes=[("PNG Images", "*.png")])
        if not out_path:
            return

        encrypted = encrypt(msg, shift)
        encode_image(path, encrypted, out_path)
        self.result_label.after(0, lambda: self.result_label.config(text=f"✅ Pesan berhasil disisipkan ke: {os.path.basename(out_path)}"))

    def decode_and_decrypt(self):
        threading.Thread(target=self._decode_and_decrypt_thread).start()

    def _decode_and_decrypt_thread(self):
        shift_text = self.shift_entry.get().strip()
        if not shift_text.isdigit():
            self._show_error("Shift harus berupa angka.")
            return

        shift = int(shift_text)
        path = filedialog.askopenfilename(title="Pilih gambar tersembunyi", filetypes=[("PNG Images", "*.png")])
        if not path:
            return

        try:
            decoded = decode_image(path)
            print(">> Decoded message:", decoded)  # debug log

            if not decoded:
                self._show_error("Gagal membaca pesan dari gambar. Mungkin gambar tidak mengandung pesan.")
                return

            decrypted = decrypt(decoded, shift)
            print(">> Decrypted message:", decrypted)  # debug log

            if not decrypted:
                self._show_error("Pesan berhasil ditemukan tapi gagal didekripsi. Cek nilai shift.")
                return

            self.result_label.after(0, lambda: self.result_label.config(text=f"📩 Pesan tersembunyi:\n{decrypted}"))

        except Exception as e:
            print(">> ERROR:", e)
            self._show_error(f"Terjadi kesalahan saat proses decode: {e}")

    def _show_error(self, message):
        self.root.after(0, lambda: messagebox.showerror("Error", message))

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
