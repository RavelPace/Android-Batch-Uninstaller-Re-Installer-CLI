import importlib
import subprocess
import sys
import os

from concurrent.futures import ThreadPoolExecutor, as_completed

def set_console_title(title: str):
    if os.name == 'nt':  # Windows
        os.system(f"title {title}")
    else:  # POSIX: Linux / macOS (xterm-compatible)
        sys.stdout.write(f"\033]0;{title}\a")
        sys.stdout.flush()

def print_title():
    title_text = "Android Batch Uninstaller / Re-Installer CLI (By RavelPace)"
    set_console_title(title_text)
    width = max(len(title_text) + 4, 60)
    border = "=" * width
    print(f"\n{border}")
    print(f"  {title_text}  ")

def ensure_adbutils():
    try:
        import adbutils
    except ImportError:
        print("❌ 'adbutils' not found. Installing now...")
        subprocess.run([sys.executable, "-m", "pip", "install", "adbutils"], check=True)
        print("✅ 'adbutils' installed successfully.")
        input("Press Enter to exit and run the script again.")
        sys.exit(1)
    return adbutils

def print_warning():
    print("\nWARNING:")
    print("BEFORE USING THIS TOOL, MAKE SURE YOU ENABLE USB DEBUGGING")
    print("AND CHECKMARK 'ALWAYS ALLOW DEBUGGING FROM THIS COMPUTER' ON YOUR DEVICE.")
    print("="*60)
    print()

adbutils = ensure_adbutils()

def ensure_packages_file(fname="packages.txt"):
    if not os.path.exists(fname):
        print(f"❌ '{fname}' not found.")
        print(f"Please create a file named '{fname}' with the package names you want to process.")
        print("Each line should contain a package name, e.g., 'com.example.app'.")
        input("Press Enter to exit and create the file.")
        sys.exit(1)

def read_packages(fname="packages.txt"):
    with open(fname, encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip() and not l.startswith("#")]

def choose_device():
    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
    devices = adb.device_list()
    if not devices:
        print("❌ No devices found. Enable USB debugging and reconnect.")
        input("Press Enter to exit...")
        sys.exit(1)
    print("Connected devices:")
    for idx, d in enumerate(devices):
        model = d.shell("getprop ro.product.model").strip()
        print(f" [{idx}] {d.serial} — {model}")
    sel = int(input(f"Select device [0-{len(devices)-1}]: ") or "0")
    return devices[sel]

def run_shell(d, args, retries=2):
    last_err = ""
    for _ in range(retries):
        try:
            out = d.shell(" ".join(args))
            return True, out.strip()
        except Exception as e:
            last_err = str(e)
    return False, last_err

def uninstall_pkg(d, pkg, keep=False):
    args = ["pm", "uninstall"] + (["-k"] if keep else []) + ["--user", "0", pkg]
    return run_shell(d, args)

def install_pkg(d, pkg):
    args = ["cmd", "package", "install-existing", "--user", "0", pkg]
    return run_shell(d, args)

def process_pkg(d, pkg, action, keep):
    if action == "uninstall":
        return pkg, *uninstall_pkg(d, pkg, keep)
    else:
        return pkg, *install_pkg(d, pkg)

def reboot_device(d):
    try:
        d.reboot()
        print("✅ Device is restarting...")
    except Exception as e:
        print(f"❌ Failed to reboot device: {e}")

def main():
    print_title()
    print_warning()
    ensure_packages_file()
    device = choose_device()
    pkgs = read_packages()
    print(f"\nLoaded {len(pkgs)} packages from file.\n")

    choice = input("Choose action: [u]ninstall or [i]nstall-existing: ").strip().lower()
    if choice in ("u", "uninstall"):
        action = "uninstall"
        keep = input("Keep data/cache? [y/N]: ").strip().lower() == "y"
    elif choice in ("i", "install"):
        action = "install"
        keep = False
    else:
        print("Invalid action. Exiting.")
        input("Press Enter to exit...")
        return

    print(f"\nPerforming '{action}' on {len(pkgs)} packages for device {device.serial}...\n")
    with ThreadPoolExecutor(max_workers=8) as exec:
        futures = {exec.submit(process_pkg, device, pkg, action, keep): pkg for pkg in pkgs}
        for future in as_completed(futures):
            pkg, ok, out = future.result()
            print(f"{'✅' if ok else '❌'} {pkg}: {out}")

    # Prompt to reboot device
    if input("\nDo you want to restart the device? [y/N]: ").strip().lower() == "y":
        reboot_device(device)
    else:
        print("Device will not be restarted.")

    input("\nDone. Press Enter to exit...")

if __name__ == "__main__":
    main()
    
    
# made with <3 by RavelPace    
