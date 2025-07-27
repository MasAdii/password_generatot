import argparse
import secrets
import string
import sys
import time
import os

# --- Import Libraries Eksternal ---
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.layout import Layout
    from rich.columns import Columns
    from rich.padding import Padding
    from rich import box
    from rich.live import Live
    from rich.spinner import Spinner
    from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn
    from rich.table import Table
    from rich.align import Align
    from rich.style import Style
    # from rich.highlighter import ReprHighlighter # Tidak diperlukan lagi untuk password langsung
except ImportError:
    print("Error: Library 'rich' tidak ditemukan. Silakan instal dengan: pip install rich", file=sys.stderr)
    sys.exit(1)

try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False

# --- Inisialisasi Konsol Rich dan Highlighter (jika masih diperlukan untuk tujuan lain) ---
console = Console(theme=None) # Kita akan definisikan style sendiri
# highlighter = ReprHighlighter() # Tidak digunakan lagi secara langsung untuk password display

# --- Definisi Warna Kustom untuk Konsistensi ---
COLOR_PRIMARY = "#8A2BE2"  # BlueViolet - Ungu Kebiruan (Main Brand)
COLOR_ACCENT = "#00FFFF"   # Cyan - Biru Cerah (Untuk password, informasi penting)
COLOR_SUCCESS = "#00FF00"  # Lime - Hijau Terang
COLOR_WARNING = "#FFD700"  # Gold - Emas
COLOR_ERROR = "#FF0000"    # Red - Merah Terang
COLOR_INFO = "#6A5ACD"     # SlateBlue - Biru Keunguan
COLOR_DIM = "#808080"      # Gray - Abu-abu

# --- Fungsi untuk Menampilkan Banner ASCII Art dengan Animasi ---
def display_banner_animated():
    """Menampilkan banner ASCII art 'Masadi Password Generator' dengan animasi."""
    banner_raw = """
███╗   ███╗ █████╗  ███████╗ █████╗ ██████╗ ██████╗  █████╗  ██████╗ ███████╗
████╗ ████║██╔══██╗ ██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗██════╝ ██╔════╝
██╔████╔██║███████║ █████╗  ███████║██████╔╝██████╔╝███████║██║  ███╗█████╗
██║╚██╔╝██║██╔══██║ ██╔══╝  ██╔══██║██╔══██╗██╔══██╗██╔══██║██║   ██║██╔══╝
██║ ╚═╝ ██║██║  ██║ ███████╗██║  ██║██║  ██║██║  ██║██║  ██║╚██████╔╝███████╗
╚═╝     ╚═╝╚═╝  ╚═╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
            Masadi Password Generator
    """
    
    console.print(Padding(Text("🚀 Memulai Masadi Secure Core...", style=f"bold dim {COLOR_INFO}", justify="center"), (1,0,1,0)))
    time.sleep(0.5)

    with Live(console=console, screen=False, refresh_per_second=60, transient=True) as live:
        full_banner_text = ""
        lines = banner_raw.strip().split('\n')
        max_line_length = max(len(line) for line in lines)
        
        # Calculate optimal width for the panel
        panel_width = min(console.width - 2, max_line_length + 6) # -2 for console padding
        
        for i, line in enumerate(lines):
            for j in range(len(line) + 1):
                revealed_line = line[:j]
                current_banner_display = full_banner_text + revealed_line
                
                panel_content = Panel(
                    Text(current_banner_display, justify="center", style=f"bold {COLOR_PRIMARY}"),
                    box=box.DOUBLE,
                    border_style=COLOR_PRIMARY,
                    title=f"[bold {COLOR_WARNING}]🔒 Memulai Protokol Keamanan 🔒[/bold {COLOR_WARNING}]",
                    title_align="center",
                    subtitle=f"[italic {COLOR_INFO}]Mitra Keamanan Utama Anda[/italic {COLOR_INFO}]",
                    subtitle_align="right",
                    width=panel_width
                )
                live.update(panel_content)
                time.sleep(0.002) # Kecepatan pengungkapan karakter

            full_banner_text += line + "\n"
            # Update panel dengan baris lengkap setelah selesai diungkap
            live.update(Panel(
                Text(full_banner_text.strip(), justify="center", style=f"bold {COLOR_PRIMARY}"),
                box=box.DOUBLE,
                border_style=COLOR_PRIMARY,
                title=f"[bold {COLOR_WARNING}]🔒 Memulai Protokol Keamanan 🔒[/bold {COLOR_WARNING}]",
                title_align="center",
                subtitle=f"[italic {COLOR_INFO}]Mitra Keamanan Utama Anda[/italic {COLOR_INFO}]",
                subtitle_align="right",
                width=panel_width
            ))
            time.sleep(0.03) # Kecepatan pengungkapan baris
    
    # Final message after banner animation
    console.print(
        Padding(
            Align(
                Text(f"🚀 Mari buat beberapa rahasia yang tak tertembus untukmu, Masadi! 🚀", 
                     style=f"{COLOR_ACCENT} italic", justify="center"),
                align="center",
                width=console.width
            ),
            (1, 0, 1, 0)
        )
    )

# --- Fungsi Generasi Password ---
def generate_password(length, use_uppercase, use_lowercase, use_numbers, use_symbols):
    """
    Menghasilkan password acak yang aman menggunakan modul 'secrets'.
    Memastikan setidaknya satu karakter dari setiap jenis yang dipilih jika memungkinkan.
    """
    char_pool = []
    
    if use_uppercase:
        char_pool.extend(string.ascii_uppercase)
    if use_lowercase:
        char_pool.extend(string.ascii_lowercase)
    if use_numbers:
        char_pool.extend(string.digits)
    if use_symbols:
        char_pool.extend("!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~")

    if not char_pool:
        raise ValueError("Setidaknya satu jenis karakter (huruf besar, huruf kecil, angka, simbol) harus dipilih.")

    password_list = []
    
    # Pastikan setidaknya satu karakter dari setiap kategori yang dipilih,
    # tetapi tidak melebihi panjang total yang diminta.
    required_chars = []
    if use_uppercase:
        required_chars.append(secrets.choice(string.ascii_uppercase))
    if use_lowercase:
        required_chars.append(secrets.choice(string.ascii_lowercase))
    if use_numbers:
        required_chars.append(secrets.choice(string.digits))
    if use_symbols:
        required_chars.append(secrets.choice("!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~"))

    # Tambahkan karakter wajib jika panjangnya tidak melebihi target
    # Jika karakter wajib lebih banyak dari panjang, ambil acak sejumlah panjang
    secrets.SystemRandom().shuffle(required_chars) # Acak dulu agar yang diambil acak
    password_list.extend(required_chars[:length]) # Ambil sebanyak 'length' atau semua jika kurang dari 'length'


    # Isi sisa panjang password dari pool karakter gabungan
    remaining_length = max(0, length - len(password_list))
    for _ in range(remaining_length):
        password_list.append(secrets.choice(char_pool))

    # Acak daftar password untuk memastikan pola tidak dapat diprediksi
    secrets.SystemRandom().shuffle(password_list)

    return "".join(password_list[:length]) # Pastikan panjang password tepat

# --- Fungsi Penilai Kekuatan Password ---
def assess_password_strength(password):
    """Menilai kekuatan password berdasarkan panjang dan variasi karakter."""
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in "!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~" for c in password)

    score = 0
    
    # Kriteria panjang
    if length >= 8: score += 1
    if length >= 12: score += 1
    if length >= 16: score += 1
    if length >= 20: score += 1 

    # Kriteria jenis karakter
    char_types_count = sum([has_upper, has_lower, has_digit, has_symbol])
    if char_types_count >= 2: score += 1
    if char_types_count >= 3: score += 1
    if char_types_count >= 4: score += 1

    # Menentukan level kekuatan dengan styling rich
    if score <= 2:
        return f"[bold {COLOR_ERROR}]Lemah 😞[/bold {COLOR_ERROR}]"
    elif score <= 4:
        return f"[bold {COLOR_WARNING}]Sedang 🤔[/bold {COLOR_WARNING}]"
    elif score <= 6:
        return f"[bold {COLOR_ACCENT}]Kuat 💪[/bold {COLOR_ACCENT}]"
    else:
        return f"[bold {COLOR_SUCCESS}]Sangat Kuat ⭐[/bold {COLOR_SUCCESS}]"

# --- Fungsi Utama CLI ---
def main():
    parser = argparse.ArgumentParser(
        # Mengubah deskripsi menjadi string biasa karena argparse tidak merender objek Rich Text
        description="Masadi Password Generator - Buat password yang kuat dan aman dengan antarmuka CLI yang premium.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "-l", "--length",
        type=int,
        default=16,
        help="Panjang password yang dihasilkan (default: 16)."
    )
    parser.add_argument(
        "-U", "--uppercase",
        action="store_true",
        help="Sertakan huruf besar (A-Z)."
    )
    parser.add_argument(
        "-L", "--lowercase",
        action="store_true",
        help="Sertakan huruf kecil (a-z)."
    )
    parser.add_argument(
        "-N", "--numbers",
        action="store_true",
        help="Sertakan angka (0-9)."
    )
    parser.add_argument(
        "-S", "--symbols",
        action="store_true",
        help="Sertakan simbol khusus (!@#$%^&* dll.)."
    )
    parser.add_argument(
        "-s", "--secure",
        action="store_true",
        help="Mode Aman: Menghasilkan password yang sangat kuat (minimal 20 karakter, semua jenis karakter aktif)."
    )
    parser.add_argument(
        "-c", "--copy",
        action="store_true",
        help="Salin password yang dihasilkan ke clipboard."
    )
    parser.add_argument(
        "-e", "--export",
        action="store_true",
        help="Ekspor password yang dihasilkan ke file 'passwords.txt'."
    )
    parser.add_argument(
        "--silent",
        action="store_true",
        help="Mode Senyap: Langsung mencetak password tanpa banner dan animasi UI."
    )
    parser.add_argument(
        "--loop",
        type=int,
        default=1,
        help="Jumlah password yang akan dihasilkan (misalnya, --loop 5 untuk 5 password)."
    )

    args = parser.parse_args()

    # --- Pengaturan Awal & Validasi ---
    if not args.silent:
        display_banner_animated()
        console.print("") # Tambahkan baris kosong untuk jarak

    char_sets_selected_by_user = any([args.uppercase, args.lowercase, args.numbers, args.symbols])

    if args.secure:
        if not args.silent:
            console.print(Panel(
                Text(f"🔒 [bold {COLOR_SUCCESS}]MODE AMAN AKTIF![/bold {COLOR_SUCCESS}] Membuat password yang sangat kuat (minimal 20 karakter, semua jenis).", 
                     justify="center", style=COLOR_SUCCESS),
                border_style=COLOR_SUCCESS,
                box=box.HEAVY,
                padding=(1, 2)
            ))
        args.length = max(args.length, 20)  # Pastikan minimal 20 karakter
        args.uppercase = args.lowercase = args.numbers = args.symbols = True
    elif not char_sets_selected_by_user:
        if not args.silent:
            console.print(Panel(
                Text(f"⚠️ [bold {COLOR_WARNING}]Tidak ada jenis karakter yang dipilih.[/bold {COLOR_WARNING}] Menggunakan semua jenis karakter untuk password yang kuat.", 
                     justify="center", style=COLOR_WARNING),
                border_style=COLOR_WARNING,
                box=box.ROUNDED,
                padding=(1, 2)
            ))
        args.uppercase = args.lowercase = args.numbers = args.symbols = True
    
    # Validasi akhir jika tidak ada set karakter yang diaktifkan (misalnya, jika semua argumen --U --L --N --S secara eksplisit diset false)
    if not any([args.uppercase, args.lowercase, args.numbers, args.symbols]):
        if not args.silent:
            console.print(Panel(
                Text(f"🚨 [bold {COLOR_ERROR}]KESALAHAN:[/bold {COLOR_ERROR}] Tidak dapat membuat password. Tidak ada jenis karakter (huruf besar, huruf kecil, angka, simbol) yang diaktifkan.", 
                     justify="center", style=f"bold {COLOR_ERROR}"),
                border_style=COLOR_ERROR,
                box=box.DOUBLE,
                padding=(1, 2)
            ))
        sys.exit(1)

    generated_passwords = []
    copy_success_count = 0
    export_success = False

    # --- Loop Generasi Password dengan Progress Bar atau Spinner ---
    if args.loop > 1 and not args.silent:
        console.print(f"\n[bold {COLOR_PRIMARY}]⚙️ Memulai generasi {args.loop} password...[/bold {COLOR_PRIMARY}]")
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeRemainingColumn(),
            TimeElapsedColumn(),
            console=console,
            transient=True # Sembunyikan progress bar saat selesai
        ) as progress:
            task = progress.add_task(f"[bold {COLOR_ACCENT}]Meramu kunci rahasia Masadi...", total=args.loop)
            for i in range(args.loop):
                start_time = time.perf_counter()
                try:
                    password = generate_password(
                        args.length,
                        args.uppercase, args.lowercase, args.numbers, args.symbols
                    )
                except ValueError as e:
                    progress.stop()
                    console.print(Panel(
                        Text(f"🚨 [bold {COLOR_ERROR}]Kesalahan saat generasi:[/bold {COLOR_ERROR}] {e}", justify="center", style=COLOR_ERROR),
                        border_style=COLOR_ERROR, padding=(1,2)
                    ))
                    sys.exit(1)
                end_time = time.perf_counter()
                generation_time = end_time - start_time
                generated_passwords.append(password)

                strength_markup_string = assess_password_strength(password) # Ini adalah string dengan markup rich
                
                # --- PERBAIKAN: Gunakan Text langsung untuk password display, hindari ReprHighlighter ---
                password_text_display = Text(password, style=f"bold {COLOR_ACCENT}") 
                label_password = Text("🔑 Password: ", style="white") 
                full_password_display = label_password + password_text_display

                label_strength = Text("💪 Kekuatan: ", style="white")
                strength_display = label_strength + Text.from_markup(strength_markup_string)

                inner_table = Table.grid(expand=True)
                inner_table.add_column(justify="left", ratio=1) # Password column takes most space
                inner_table.add_column(justify="right") # Strength column takes minimum space
                inner_table.add_row(
                    full_password_display, # Pass the pre-constructed Rich Text object directly
                    strength_display       # Pass the pre-constructed Rich Text object directly
                )

                console.print(
                    Panel(
                        inner_table, # Memasukkan Table langsung ke Panel
                        title=f"[bold {COLOR_PRIMARY}]✨ Password {i+1} dari {args.loop} ✨[/bold {COLOR_PRIMARY}]",
                        title_align="left",
                        border_style=COLOR_INFO,
                        box=box.ROUNDED,
                        padding=(0, 2) # Padding sedikit dikurangi karena table sudah punya padding internal
                    )
                )
                console.print(f"[dim {COLOR_DIM}]Waktu Generasi: {generation_time:.4f} detik[/dim {COLOR_DIM}] ⏱️")

                if args.copy:
                    if PYPERCLIP_AVAILABLE:
                        try:
                            pyperclip.copy(password)
                            console.print(f"[bold {COLOR_INFO}]📋 Password disalin ke clipboard! [bold {COLOR_SUCCESS}]✔[/bold {COLOR_SUCCESS}][/bold {COLOR_INFO}]")
                            copy_success_count += 1
                        except pyperclip.PyperclipException:
                            console.print(f"[bold {COLOR_ERROR}]🚨 Peringatan:[/bold {COLOR_ERROR}] Tidak dapat menyalin ke clipboard. Pastikan mekanisme copy/paste tersedia. [dim](Instal 'xclip'/'xsel' untuk Linux)[/dim]")
                    else:
                        console.print(f"[bold {COLOR_ERROR}]🚨 Peringatan:[/bold {COLOR_ERROR}] Library 'pyperclip' tidak terinstal. Tidak dapat menyalin ke clipboard. [dim](pip install pyperclip)[/dim]")
                
                progress.update(task, advance=1)
                time.sleep(0.1) # Penundaan kecil untuk efek visual
    else: # Generasi password tunggal atau mode senyap
        if not args.silent:
            with console.status(f"[bold {COLOR_ACCENT}]Meramu kunci rahasia Anda...", spinner="point", speed=1.5, spinner_style=COLOR_ACCENT) as status:
                start_time = time.perf_counter()
                try:
                    password = generate_password(
                        args.length,
                        args.uppercase, args.lowercase, args.numbers, args.symbols
                    )
                except ValueError as e:
                    status.stop()
                    console.print(Panel(
                        Text(f"🚨 [bold {COLOR_ERROR}]Kesalahan saat generasi:[/bold {COLOR_ERROR}] {e}", justify="center", style=COLOR_ERROR),
                        border_style=COLOR_ERROR, padding=(1,2)
                    ))
                    sys.exit(1)
                end_time = time.perf_counter()
                generation_time = end_time - start_time
                status.stop()
                console.print(f"[bold {COLOR_SUCCESS}]✅ Password berhasil dibuat![/bold {COLOR_SUCCESS}]\n")
        else:
            try:
                password = generate_password(
                    args.length,
                    args.uppercase, args.lowercase, args.numbers, args.symbols
                )
            except ValueError as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
            
        generated_passwords.append(password)

        if args.silent:
            console.print(password)
        else:
            strength_markup_string = assess_password_strength(password)
            
            # --- PERBAIKAN: Gunakan Text langsung untuk password display, hindari ReprHighlighter ---
            password_text_display = Text(password, style=f"bold {COLOR_ACCENT}") 
            label_password = Text("🔑 Password: ", style="white")
            full_password_display = label_password + password_text_display

            label_strength = Text("💪 Kekuatan: ", style="white")
            strength_display = label_strength + Text.from_markup(strength_markup_string)

            inner_table = Table.grid(expand=True)
            inner_table.add_column(justify="left", ratio=1)
            inner_table.add_column(justify="right")
            inner_table.add_row(
                full_password_display, # Pass the pre-constructed Rich Text object directly
                strength_display       # Pass the pre-constructed Rich Text object directly
            )

            console.print(
                Panel(
                    inner_table, # Memasukkan Table langsung ke Panel
                    title=f"[bold {COLOR_PRIMARY}]✨ Password yang Dihasilkan ✨[/bold {COLOR_PRIMARY}]",
                    title_align="left",
                    border_style=COLOR_INFO,
                    box=box.ROUNDED,
                    padding=(0, 2)
                )
            )
            console.print(f"[dim {COLOR_DIM}]Waktu Generasi: {generation_time:.4f} detik[/dim {COLOR_DIM}] ⏱️")

            if args.copy:
                if PYPERCLIP_AVAILABLE:
                    try:
                        pyperclip.copy(password)
                        console.print(f"[bold {COLOR_INFO}]📋 Password disalin ke clipboard! [bold {COLOR_SUCCESS}]✔[/bold {COLOR_SUCCESS}][/bold {COLOR_INFO}]")
                        copy_success_count += 1
                    except pyperclip.PyperclipException:
                        console.print(f"[bold {COLOR_ERROR}]🚨 Peringatan:[/bold {COLOR_ERROR}] Tidak dapat menyalin ke clipboard. Pastikan mekanisme copy/paste tersedia. [dim](Instal 'xclip'/'xsel' untuk Linux)[/dim]")
                else:
                    console.print(f"[bold {COLOR_ERROR}]🚨 Peringatan:[/bold {COLOR_ERROR}] Library 'pyperclip' tidak terinstal. Tidak dapat menyalin ke clipboard. [dim](pip install pyperclip)[/dim]")
    
    # --- Ekspor ke File ---
    if args.export and generated_passwords:
        export_file = "passwords.txt"
        mode = "a" if os.path.exists(export_file) else "w"
        try:
            with open(export_file, mode) as f:
                for pwd in generated_passwords:
                    f.write(f"{pwd}\n")
            export_success = True
            if not args.silent:
                console.print(f"[bold {COLOR_INFO}]💾 {len(generated_passwords)} password diekspor ke [bold {COLOR_SUCCESS}]{export_file}[/bold {COLOR_SUCCESS}]! [bold {COLOR_SUCCESS}]✔[/bold {COLOR_SUCCESS}][/bold {COLOR_INFO}]")
            else:
                console.print(f"Diekspor {len(generated_passwords)} password ke {export_file}")
        except IOError:
            if not args.silent:
                console.print(Panel(
                    Text(f"[bold {COLOR_ERROR}]🚨 Kesalahan:[/bold {COLOR_ERROR}] Tidak dapat menulis ke '{export_file}'. Periksa izin file.", 
                         justify="center", style=COLOR_ERROR),
                    border_style=COLOR_ERROR, padding=(1,2)
                ))
            else:
                print(f"Error: Tidak dapat menulis ke {export_file}", file=sys.stderr)
            sys.exit(1)

    # --- Summary Akhir ---
    if not args.silent:
        console.print("\n")
        summary_table = Table(
            title=f"[bold underline {COLOR_PRIMARY}]Ringkasan Generasi Masadi[/bold underline {COLOR_PRIMARY}]",
            box=box.HEAVY_HEAD, # Jenis kotak baru untuk tabel
            border_style=COLOR_PRIMARY,
            header_style=Style(color=COLOR_WARNING, bold=True),
            show_footer=False
        )
        summary_table.add_column("Statistik", justify="left", style=f"{COLOR_INFO}")
        summary_table.add_column("Nilai", justify="right", style=f"bold {COLOR_ACCENT}")

        summary_table.add_row("Total Password Dihasilkan:", f"{len(generated_passwords)}")
        if args.copy:
            copy_status_text = f"[bold {COLOR_SUCCESS}]{copy_success_count}[/bold {COLOR_SUCCESS}] [green]✅[/green]" if copy_success_count > 0 else f"[bold {COLOR_ERROR}]0[/bold {COLOR_ERROR}] [red]❌[/red]"
            summary_table.add_row("Password Disalin ke Clipboard:", copy_status_text)
        if args.export:
            export_status_text = f"[bold {COLOR_SUCCESS}]Ya[/bold {COLOR_SUCCESS}] [green]✅[/green]" if export_success else f"[bold {COLOR_ERROR}]Tidak[/bold {COLOR_ERROR}] [red]❌[/red]"
            summary_table.add_row("Password Diekspor ke File:", export_status_text)
        summary_table.add_row("Mode Aman Aktif:", f"[bold {COLOR_SUCCESS}]Ya[/bold {COLOR_SUCCESS}]" if args.secure else f"[bold {COLOR_DIM}]Tidak[/bold {COLOR_DIM}]")
        summary_table.add_row("Panjang yang Digunakan:", f"{args.length}")
        
        console.print(Align.center(summary_table, width=console.width))

        console.print(
            Padding(
                Align(
                    Text(f"\n✨ Terima kasih telah menggunakan Masadi Password Generator! ✨", 
                         style=f"bold {COLOR_PRIMARY}", justify="center"),
                    align="center",
                    width=console.width
                ),
                (1, 0, 1, 0), expand=True
            )
        )
        console.print(Align(Text(f"         Tetap aman. Tetap Masadi. 😎", style=f"dim italic {COLOR_DIM}", justify="center"), align="center"))
        console.print(f"[{COLOR_DIM}]v1.2.4 - Dibuat dengan [red]❤️[/red] oleh Masadi Security Labs[/][dim]")

# --- Titik Masuk Program ---
if __name__ == "__main__":
    main()
