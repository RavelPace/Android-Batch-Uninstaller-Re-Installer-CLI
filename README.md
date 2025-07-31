---

# 🔧 Android Batch Uninstaller / Re-Installer CLI

A Python CLI tool to batch uninstall or reinstall system (or user) apps on Android devices via ADB, using a list of package names stored in a `packages.txt` file. It uses `adbutils` for Python-based device interaction.

---

## Features

* Automatically installs **`adbutils`** if missing on runtime.
* Prompts a **USB debugging warning**, ensuring the device is trusted.
* Reads `packages.txt`—ignoring blank lines and comments (`#`).
* Lists connected devices and allows selecting one.
* Supports two actions:

  * **Uninstall**, optionally retaining data (`-k`)
  * **Install‑existing** of previously removed system apps
* Executes commands concurrently with `ThreadPoolExecutor` (up to 8 threads).
* Optionally reboots the device after operations.

---

## Requirements

* Python 3.8 or newer
* ADB command-line tools installed and accessible (`adb`)
* Android device with **USB Debugging enabled** and trusted on the host computer
* `adbutils` Python module (automatically installed if missing)

---

## Installation & Setup

1. Clone or place the script in your working directory.
2. Ensure **ADB** is installed (e.g. from Android SDK platform-tools).
- **Do a proper backup of your data! You can never be too careful!**
- Enable _Developer Options_ on your smartphone.
- Turn on _USB Debugging_ from the developer panel.
- From the settings, disconnect from any OEM accounts (when you delete an OEM
  account package it could lock you on the lockscreen because the phone can't
  associate your identity anymore)
- Install ADB (see the intructions by clicking on your OS below):<p>
  <details>
  <summary>WINDOWS</summary>

  - Download [android platform tools](https://dl.google.com/android/repository/platform-tools-latest-windows.zip)
    and unzip it somewhere.
  - [Add the android platform tools to your PATH](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/)
    **OR** make sure to launch UAD from the same directory.

  - [Install USB drivers for your device](https://developer.android.com/studio/run/oem-usb#Drivers)
  - Check your device is detected:

    ```bash
     adb devices
    ```

    </details>
    </p>
3. Open the script.

---

## Usage

1. Create a `packages.txt` in the script’s directory:

   ```
   # System packages to process
   com.android.chrome
   com.example.app
   ```

2. Run the script:

   ```bash
   python main.py
   ```

3. Follow the interactive steps:

   * Confirm USB debugging warning.
   * Select device from the list.
   * Choose the action:

     * **Uninstall** (`u`) — optionally **keep data/cache**
     * **Install-existing** (`i`) — reinstalls removed system apps
   * Script runs each package concurrently, printing ✅ or ❌ status.

4. Opt to **reboot** device when prompted at the end.

---

## Package Operations

* **Uninstall with data retention:**

  ```
  adb shell pm uninstall -k --user 0 <package>
  ```

  This removes the app but retains user-generated data and cache.

* **Reinstall system app:**

  ```
  adb shell cmd package install-existing --user 0 <package>
  ```

  Useful when reinstalling system apps that were previously uninstalled.

---

## Safety & Best Practices

* **Caution:** Uninstalling critical system apps can cause boot loops or instability, particularly on MIUI, HyperOS, or OEM ROMs. Always research each package before removal.
* Start by testing on a non-essential app and consider keeping user data if unsure.
* If necessary, reboot often between operations to detect issues early.
**NOTE:** Chinese phones users may need to use the AOSP list for removing some stock
apps because those Chinese manufacturers (especially Xiaomi and Huawei) have been
using the name of AOSP packages for their own (modified & closed-source) apps.
* The `packages.txt` file I provided has been tested and works without issues on the TECNO KJ7.

---

## Example `packages.txt`

```text
com.android.egg
com.android.traceur
com.debug.loggerui
```

---

## Troubleshooting

| Symptom                                   | Suggested Fix                                                                                                             |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `adbutils` install prompt keeps rerunning | Rerun the script after installation or install `adbutils` manually via pip                                                |
| No devices found                          | Reconnect device, accept device trust prompt, restart ADB server (`adb kill-server && adb start-server`)                  |
| Permission errors or "Failure \[-1000]"   | Some system apps may require root or unlocked bootloader to uninstall.                                                    |

---

## References

* `adbutils`: A pure Python library to interface with ADB, install/uninstall apps, list devices, push/pull files, and more.
* Real-world bloatware removal scripts and examples using shell commands in Python.

---

## 🔑 Summary

This script offers a simple yet powerful way to batch remove or reinstall Android packages using Python and ADB. It’s ideal for debloating devices or restoring system apps. Just prepare your `packages.txt`, run the script, and follow the prompts—just use caution when removing system-critical components.

---
