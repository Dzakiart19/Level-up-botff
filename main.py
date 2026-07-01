import os
import sys
import time
import json
import threading
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

ACCOUNTS_FILE = "accounts.json"

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""
{Colors.RED}{Colors.BOLD}
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║    ██████╗ ███████╗██╗  ██╗                                ║
║    ██╔══██╗██╔════╝╚██╗██╔╝                                ║
║    ██████╔╝█████╗   ╚███╔╝                                 ║
║    ██╔══██╗██╔══╝   ██╔██╗                                 ║
║    ██║  ██║███████╗██╔╝ ██╗                                ║
║    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝                                ║
║                                                            ║
║        ╔═╗╔═╗╦═╗╔═╗╔═╗╦═╗╔═╗╔╦╗╦╔═╗╔╗╔                     ║
║        ║  ║ ║╠╦╝╠═╝║ ║╠╦╝╠═╣ ║ ║║ ║║║║                     ║
║        ╚═╝╚═╝╩╚═╩  ╚═╝╩╚═╩ ╩ ╩ ╩╚═╝╝╚╝                     ║
║                                                            ║
║             {Colors.CYAN}Free Fire Gaming Bot v2.0{Colors.RED}                      ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
{Colors.END}
    {Colors.YELLOW}⚡ Auto Start | Team Code | UID Invite ⚡{Colors.END}
{Colors.CYAN}════════════════════════════════════════════════════════════{Colors.END}
"""
    print(banner)

def print_status(message, status_type="info"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    if status_type == "success":
        icon = "✓"
        color = Colors.GREEN
    elif status_type == "error":
        icon = "✗"
        color = Colors.RED
    elif status_type == "warning":
        icon = "⚠"
        color = Colors.YELLOW
    else:
        icon = "ℹ"
        color = Colors.CYAN
    print(f"{Colors.BOLD}[{timestamp}]{Colors.END} {color}{icon} {message}{Colors.END}")

def print_menu():
    menu = f"""
{Colors.CYAN}╔════════════════════════════════════════════════════════════╗
║                    {Colors.BOLD}MAIN MENU{Colors.END}{Colors.CYAN}                               ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  {Colors.GREEN}1.{Colors.END} {Colors.WHITE}Start Bot (1 Akun - Pilih dari daftar){Colors.CYAN}                ║
║  {Colors.GREEN}2.{Colors.END} {Colors.WHITE}Auto Start with Team Code{Colors.CYAN}                              ║
║  {Colors.GREEN}3.{Colors.END} {Colors.WHITE}Jalankan SEMUA Bot Sekaligus{Colors.CYAN}                           ║
║  {Colors.GREEN}4.{Colors.END} {Colors.WHITE}Stop Current Operation{Colors.CYAN}                                 ║
║  {Colors.GREEN}5.{Colors.END} {Colors.WHITE}View Bot Status{Colors.CYAN}                                        ║
║  {Colors.GREEN}6.{Colors.END} {Colors.WHITE}Lihat Daftar Akun{Colors.CYAN}                                      ║
║  {Colors.GREEN}7.{Colors.END} {Colors.WHITE}View Logs{Colors.CYAN}                                              ║
║  {Colors.RED}0.{Colors.END} {Colors.WHITE}Exit{Colors.CYAN}                                                   ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝{Colors.END}
"""
    print(menu)

def loading_animation(text, duration=2):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        frame = frames[i % len(frames)]
        print(f"\r{Colors.CYAN}{frame} {text}...{Colors.END}", end="", flush=True)
        time.sleep(0.1)
        i += 1
    print(f"\r{Colors.GREEN}✓ {text} Complete!{Colors.END}          ")

def get_user_input(prompt, input_type="text", color=Colors.CYAN):
    print(f"{color}┌─{Colors.END}")
    user_input = input(f"{color}└─> {Colors.WHITE}{prompt}: {Colors.END}")
    return user_input if input_type == "text" else int(user_input)

def load_accounts():
    try:
        if os.path.exists(ACCOUNTS_FILE):
            with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print_status(f"Gagal baca accounts.json: {e}", "error")
    return []

def display_bot_info():
    accounts = load_accounts()
    total = len(accounts)
    print(f"\n{Colors.CYAN}╔════════════════════════════════════════════════════════════╗")
    print(f"║               {Colors.BOLD}DAFTAR AKUN BOT ({total} akun){Colors.END}{Colors.CYAN}                  ║")
    print(f"╠════════════════════════════════════════════════════════════╣{Colors.END}")
    if not accounts:
        print_status("Tidak ada akun di accounts.json!", "error")
    else:
        for i, acc in enumerate(accounts[:5], 1):
            name = acc.get("name", "-")
            uid = acc.get("uid", "-")
            print(f"{Colors.WHITE}  [{i}] {Colors.GREEN}{name}{Colors.END} {Colors.CYAN}UID: {Colors.YELLOW}{uid}{Colors.END}")
        if total > 5:
            print(f"{Colors.CYAN}  ... dan {total - 5} akun lainnya{Colors.END}")
    print(f"{Colors.CYAN}╚════════════════════════════════════════════════════════════╝{Colors.END}\n")

def show_all_accounts():
    accounts = load_accounts()
    clear_screen()
    print_banner()
    print(f"\n{Colors.CYAN}╔════════════════════════════════════════════════════════════╗")
    print(f"║                 {Colors.BOLD}SEMUA AKUN BOT{Colors.END}{Colors.CYAN}                             ║")
    print(f"╠════════════════════════════════════════════════════════════╣{Colors.END}")
    for i, acc in enumerate(accounts, 1):
        name = acc.get("name", "-")
        uid = acc.get("uid", "-")
        region = acc.get("region", "-")
        print(f"{Colors.WHITE}  [{Colors.GREEN}{i:02d}{Colors.WHITE}] {Colors.CYAN}{name}{Colors.END} | UID: {Colors.YELLOW}{uid}{Colors.END} | Region: {region}")
    print(f"{Colors.CYAN}╚════════════════════════════════════════════════════════════╝{Colors.END}\n")
    input(f"{Colors.YELLOW}Press Enter untuk kembali...{Colors.END}")

class BotController:
    def __init__(self):
        self.is_running = False
        self.operation_type = None
        self.bot_threads = []
        self.active_accounts = []

    def pick_account(self):
        accounts = load_accounts()
        if not accounts:
            print_status("Tidak ada akun di accounts.json!", "error")
            return None
        print(f"\n{Colors.CYAN}Pilih akun:{Colors.END}")
        for i, acc in enumerate(accounts, 1):
            print(f"  {Colors.GREEN}[{i}]{Colors.END} {acc.get('name', '-')} | UID: {Colors.YELLOW}{acc.get('uid', '-')}{Colors.END}")
        choice = get_user_input("Masukkan nomor akun", "text", Colors.YELLOW)
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(accounts):
                return accounts[idx]
        except:
            pass
        print_status("Pilihan tidak valid!", "error")
        return None

    def start_bot(self):
        if self.is_running:
            print_status("Bot sudah berjalan!", "warning")
            return

        acc = self.pick_account()
        if not acc:
            return

        print_status(f"Menjalankan bot: {acc['name']}...", "info")
        loading_animation("Initializing connection")

        try:
            from app import FF_CLIENT
            uid = acc["uid"]
            pwd = acc["password"]

            t = threading.Thread(target=lambda: FF_CLIENT(uid, pwd), daemon=True)
            t.start()
            self.bot_threads.append(t)
            self.active_accounts.append(acc["name"])
            self.is_running = True
            self.operation_type = f"Connected ({acc['name']})"
            print_status(f"Bot {acc['name']} berhasil dijalankan!", "success")
        except Exception as e:
            print_status(f"Gagal menjalankan bot: {str(e)}", "error")

    def start_all_bots(self):
        accounts = load_accounts()
        if not accounts:
            print_status("Tidak ada akun di accounts.json!", "error")
            return

        print_status(f"Menjalankan {len(accounts)} bot sekaligus...", "info")
        loading_animation("Initializing all bots")

        try:
            from app import FF_CLIENT
            for acc in accounts:
                uid = acc["uid"]
                pwd = acc["password"]
                name = acc.get("name", uid)
                t = threading.Thread(target=lambda u=uid, p=pwd: FF_CLIENT(u, p), daemon=True)
                t.start()
                self.bot_threads.append(t)
                self.active_accounts.append(name)
                print_status(f"Bot {name} dimulai", "success")
                time.sleep(0.5)

            self.is_running = True
            self.operation_type = f"All Bots Running ({len(accounts)} akun)"
            print_status(f"Semua {len(accounts)} bot berhasil dijalankan!", "success")
        except Exception as e:
            print_status(f"Gagal menjalankan bot: {str(e)}", "error")

    def auto_start_teamcode(self):
        if not self.is_running:
            print_status("Jalankan bot dulu (Opsi 1 atau 3)", "warning")
            return

        team_code = get_user_input("Masukkan Team Code", "text", Colors.YELLOW)
        if not team_code.isdigit():
            print_status("Team code tidak valid! Gunakan angka saja.", "error")
            return

        print_status(f"Auto start diaktifkan untuk team: {team_code}", "success")
        print_status("Kirim /lw di dalam game untuk mengaktifkan", "info")
        self.operation_type = f"Auto Start (Team: {team_code})"

    def stop_operation(self):
        if not self.is_running:
            print_status("Tidak ada operasi yang berjalan", "warning")
            return

        print_status("Menghentikan semua operasi...", "warning")
        loading_animation("Disconnecting")
        self.is_running = False
        self.operation_type = None
        self.bot_threads = []
        self.active_accounts = []
        print_status("Semua bot dihentikan!", "success")

    def view_status(self):
        clear_screen()
        print_banner()

        status = "ONLINE" if self.is_running else "OFFLINE"
        status_color = Colors.GREEN if self.is_running else Colors.RED

        print(f"\n{Colors.CYAN}╔════════════════════════════════════════════════════════════╗")
        print(f"║                   {Colors.BOLD}SYSTEM STATUS{Colors.END}{Colors.CYAN}                           ║")
        print(f"╠════════════════════════════════════════════════════════════╣{Colors.END}")
        print(f"{Colors.WHITE}  Bot Status: {status_color}{status}{Colors.END}")
        print(f"{Colors.WHITE}  Operasi: {Colors.YELLOW}{self.operation_type or 'None'}{Colors.END}")
        print(f"{Colors.WHITE}  Akun Aktif: {Colors.GREEN}{len(self.active_accounts)}{Colors.END}")
        if self.active_accounts:
            for name in self.active_accounts:
                print(f"{Colors.CYAN}    - {name}{Colors.END}")
        print(f"{Colors.CYAN}╚════════════════════════════════════════════════════════════╝{Colors.END}\n")

        input(f"{Colors.YELLOW}Press Enter untuk kembali...{Colors.END}")


def main():
    controller = BotController()

    while True:
        clear_screen()
        print_banner()
        display_bot_info()
        print_menu()

        try:
            choice = get_user_input("Pilih opsi", "text", Colors.GREEN)

            if choice == "1":
                controller.start_bot()
                time.sleep(2)

            elif choice == "2":
                controller.auto_start_teamcode()
                time.sleep(2)

            elif choice == "3":
                controller.start_all_bots()
                time.sleep(2)

            elif choice == "4":
                controller.stop_operation()
                time.sleep(2)

            elif choice == "5":
                controller.view_status()

            elif choice == "6":
                show_all_accounts()

            elif choice == "7":
                print_status("Log viewer coming soon!", "info")
                time.sleep(2)

            elif choice == "0":
                print_status("Shutting down Bot...", "warning")
                loading_animation("Exiting")
                print(f"\n{Colors.RED}{Colors.BOLD}Thanks for using Rex Corporation!{Colors.END}\n")
                sys.exit(0)

            else:
                print_status("Opsi tidak valid! Coba lagi.", "error")
                time.sleep(1)

        except KeyboardInterrupt:
            print(f"\n\n{Colors.RED}Program dihentikan oleh user{Colors.END}")
            sys.exit(0)
        except Exception as e:
            print_status(f"Error: {str(e)}", "error")
            time.sleep(2)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{Colors.RED}Fatal Error: {str(e)}{Colors.END}")
        sys.exit(1)
