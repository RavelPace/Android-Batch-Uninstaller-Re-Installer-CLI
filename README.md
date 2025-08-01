# 🔧 Android Batch Uninstaller / Re-Installer CLI

A Python CLI tool to batch uninstall or reinstall system (or user) apps on Android devices via ADB, using a list of package names stored in a `packages.txt` file. It uses `adbutils` for Python-based device interaction.

---

## ✨ Features

- ✅ Automatically installs `adbutils` if missing at runtime.
- 🔐 Warns about USB debugging requirements for device safety.
- 📦 Reads `packages.txt`, skipping comments and blank lines.
- 🔌 Lists connected Android devices and lets you select one.
- ⚙️ Supports two main actions:
  - **Uninstall** apps (optionally retaining data)
  - **Install‑existing** for previously removed system apps
- 🧵 Runs operations concurrently using Python threads (max 8).
- 🔄 Optionally reboots the device after finishing.

---

## 🧰 Requirements

- Python 3.8 or newer
- ADB command-line tools installed and accessible
- Android device with **USB Debugging enabled**
- Internet access (to auto-install Python modules if missing)

---

## 📦 Installation & Setup

### 1. Prerequisites

- Backup your device—**just in case**.
- Enable **Developer Options** and **USB Debugging** on your Android.
- Disconnect from any OEM accounts (important for some devices).
- Download and install **ADB platform-tools**:

<details>
<summary>📥 Setup for Windows</summary>

1. Download [platform-tools](https://dl.google.com/android/repository/platform-tools-latest-windows.zip) and unzip it.
2. Add the folder to your system `PATH` or run the script from that directory.
3. [Install USB drivers for your device](https://developer.android.com/studio/run/oem-usb#Drivers).
4. Check device connection:

   ```bash
   adb devices

</details>

---

### 2. Project Structure

```
android-batch-cli/
├── main.py
├── packages.txt
└── README.md
```

Create `packages.txt` with a list of app package names, one per line.

---

## ▶️ Usage

1. **Prepare `packages.txt`:**

```text
# Packages to uninstall or reinstall
com.android.chrome
com.example.myapp
```

2. **Run the script:**

```bash
python main.py
```

3. **Interactive Prompts:**

* Confirm USB debugging warning.
* Select a connected device.
* Choose action:

  * `[u]` uninstall
  * `[i]` install-existing
* Decide whether to keep app data (for uninstall only).
* Packages will be processed in parallel.
* You’ll be asked whether to reboot the device.

---

## 🧪 What the Script Does

### Uninstall with optional data retention

```bash
adb shell pm uninstall -k --user 0 <package>
```

### Reinstall removed system app

```bash
adb shell cmd package install-existing --user 0 <package>
```

---

## ⚠️ Safety Tips

* Removing system apps may cause device instability or boot loops.
* On some OEMs (e.g., Xiaomi, Huawei), stock apps use AOSP package names.
* When unsure, use the **`-k`** flag to retain data.
* Always test on non-essential apps first.

---

## 📁 Example `packages.txt`

```text
com.android.egg
com.android.traceur
com.miui.analytics
```

---

## ❓ Troubleshooting

| Issue                                   | Solution                                                                              |
| --------------------------------------- | ------------------------------------------------------------------------------------- |
| `adbutils` keeps reinstalling           | Exit script and rerun, or install manually with `pip install adbutils`                |
| No devices detected                     | Reconnect via USB, enable debugging, approve authorization popup on the device        |
| Uninstall fails with `[INSTALL_FAILED]` | Some system apps require root access or bootloader unlock                             |
| Script exits unexpectedly               | Ensure all package files are valid and `adb` is accessible in terminal/command prompt |

---

## 🔍 References

* [`adbutils`](https://github.com/openatx/adbutils): Python ADB interaction library
* Android shell commands: `pm`, `cmd package`, `reboot`
* Tested on multiple OEMs including TECNO KJ7 and Pixel devices

---

## 🧾 Summary

This CLI tool provides a safe, fast, and flexible way to uninstall or reinstall Android apps in bulk using Python and ADB.
**Perfect for debloating devices or restoring core apps.**

Just prep a `packages.txt`, connect your device, and follow the interactive prompts.
Use it responsibly—and enjoy your cleaner Android experience!

---

**Made with ❤️ by RavelPace**
