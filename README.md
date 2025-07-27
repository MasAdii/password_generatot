# Masadi Password Generator (v1.2.4)

![Masadi Password Generator Banner](https://img.shields.io/badge/Masadi%20Password%20Generator-v1.2.4-blueviolet?style=for-the-badge&logo=python&logoColor=white)
![Python Version](https://img.shields.io/badge/Python-3.6+-green?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)
[![Made with Rich](https://img.shields.io/badge/Made%20with-Rich-purple?style=for-the-badge)](https://github.com/Textualize/rich)

Masadi Password Generator adalah alat berbasis Command Line Interface (CLI) yang canggih dan aman, dirancang untuk membantu Anda membuat kata sandi yang kuat dan unik dengan mudah. Dengan antarmuka yang intuitif dan visual yang menarik berkat pustaka `rich`, alat ini memastikan keamanan digital Anda.

## ✨ Fitur Utama

*   **Generasi Password Aman**: Menggunakan modul `secrets` Python untuk menghasilkan password kriptografis yang kuat dan acak, cocok untuk aplikasi keamanan tinggi.
*   **Antarmuka Pengguna Premium (Rich UI)**: Menampilkan banner animasi, progress bar interaktif, tabel ringkasan, dan output yang diwarnai untuk pengalaman pengguna yang menyenangkan.
*   **Kustomisasi Fleksibel**:
    *   Tentukan panjang password (`-l`/`--length`).
    *   Sertakan atau kecualikan huruf besar (`-U`/`--uppercase`), huruf kecil (`-L`/`--lowercase`), angka (`-N`/`--numbers`), dan simbol (`-S`/`--symbols`).
*   **Mode Aman (`-s`/`--secure`)**: Secara otomatis menghasilkan password yang sangat kuat (minimal 20 karakter, semua jenis karakter aktif) dengan satu perintah.
*   **Penilai Kekuatan Password**: Secara instan menganalisis dan menampilkan kekuatan password yang dihasilkan (Lemah, Sedang, Kuat, Sangat Kuat).
*   **Salin ke Clipboard (`-c`/`--copy`)**: Salin password yang dihasilkan langsung ke clipboard Anda untuk penempelan yang mudah.
*   **Ekspor ke File (`-e`/`--export`)**: Simpan password yang dihasilkan ke file `passwords.txt` untuk referensi di masa mendatang.
*   **Generasi Loop (`--loop`)**: Hasilkan banyak password dalam satu eksekusi dengan progress bar visual.
*   **Mode Senyap (`--silent`)**: Cetak password mentah langsung ke konsol tanpa UI atau animasi untuk skrip atau otomatisasi.

## 🚀 Instalasi

1.  **Pastikan Anda memiliki Python 3.6+ terinstal.**
    Anda dapat mengunduhnya dari [python.org](https://www.python.org/downloads/).

2.  **Kloning repositori ini (atau unduh file `masadi_passgen.py`):**

    ```bash
    git clone https://github.com/MasAdii/password_generatot.git
    cd password_generatot
    ```

3.  **Instal dependensi yang diperlukan:**
    Alat ini sangat bergantung pada pustaka `rich` dan `pyperclip`.

    ```bash
    pip install rich pyperclip
    ```
    *Catatan: Untuk fungsi salin ke clipboard di Linux, Anda mungkin perlu menginstal `xclip` atau `xsel` secara terpisah. Contoh: `sudo apt-get install xclip` (Ubuntu/Debian) atau `sudo yum install xsel` (Fedora/CentOS).*

## 💡 Penggunaan

Jalankan skrip dari terminal Anda untuk melihat semua opsi yang tersedia:


```bash
python masadi_passgen.py --help

Ini akan menampilkan output bantuan seperti di bawah ini:

usage: masadi_passgen.py [-h] [-l LENGTH] [-U] [-L] [-N] [-S] [-s] [-c] [-e] [--silent] [--loop LOOP]

Masadi Password Generator - Buat password yang kuat dan aman dengan antarmuka CLI yang premium.

options:
  -h, --help            show this help message and exit
  -l LENGTH, --length LENGTH
                        Panjang password yang dihasilkan (default: 16).
  -U, --uppercase       Sertakan huruf besar (A-Z).
  -L, --lowercase       Sertakan huruf kecil (a-z).
  -N, --numbers         Sertakan angka (0-9).
  -S, --symbols         Sertakan simbol khusus (!@#$%^&* dll.).
  -s, --secure          Mode Aman: Menghasilkan password yang sangat kuat (minimal 20 karakter, semua jenis karakter aktif).
  -c, --copy            Salin password yang dihasilkan ke clipboard.
  -e, --export          Ekspor password yang dihasilkan ke file 'passwords.txt'.
  --silent              Mode Senyap: Langsung mencetak password tanpa banner dan animasi UI.
  --loop LOOP           Jumlah password yang akan dihasilkan (misalnya, --loop 5 untuk 5 password).

Contoh Penggunaan:
Hasilkan password default (panjang 16, semua jenis karakter):
Generated bash
python masadi_passgen.py
Use code with caution.
Bash
Hasilkan password panjang 12 dengan huruf kecil dan angka saja:
Generated bash
python masadi_passgen.py -l 12 -L -N
Use code with caution.
Bash
Hasilkan password yang sangat kuat dalam mode aman dan salin ke clipboard:
Generated bash
python masadi_passgen.py -s -c
Use code with caution.
Bash
Hasilkan 3 password, lalu ekspor ke file:
Generated bash
python masadi_passgen.py --loop 3 -e
Use code with caution.
Bash
Hasilkan password dalam mode senyap (berguna untuk scripting):
Generated bash
python masadi_passgen.py --silent -l 24 -U -L -N -S
Use code with caution.
Bash
Output:
Generated code
XyZ1@bC2!dE3$fG4%hI5^jK6*
Use code with caution.
Hasilkan password dengan semua jenis karakter (opsi default jika tidak ada yang dipilih):
Generated bash
python masadi_passgen.py -l 20
Use code with caution.
Bash
(Ini setara dengan python masadi_passgen.py -l 20 -U -L -N -S jika Anda tidak menentukan jenis karakter apa pun.)
💖 Kontribusi
Kontribusi disambut baik! Jika Anda memiliki ide untuk fitur baru, laporan bug, atau peningkatan, jangan ragu untuk membuka issue atau mengajukan pull request.
