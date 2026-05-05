# WinTweaks

A Windows system tweaking tool inspired by GNOME Tweaks, designed to customize and optimize Windows settings through an intuitive graphical interface.

## Features

- **Taskbar**: Position, transparency, multi-display, tray, alignment and corners
- **Explorer**: Hidden files, desktop icons, jump lists, navigation pane and ribbon
- **System**: Dark mode, accent colors, snap, shake, sticky keys and crash control
- **Network**: IPv6, LLMNR, SMB1, RDP, Wi-Fi Sense, Teredo and APIPA controls
- **Power & Battery**: Hibernation, fast startup, throttling and power-flyout entries
- **Gaming**: Game Bar, Game Mode, HW GPU scheduling, FSO, mouse accel, VBS, GPU priority
- **Performance**: Visual effects, menu delays, drag windows, hung-app timeouts
- **Security & Defender**: UAC, SmartScreen, Defender real-time/cloud/samples, AutoPlay
- **Privacy**: Telemetry, advertising ID, Cortana, recent files
- **Apps & Services**: OneDrive, Cortana, Store, Search/SysMain/Spooler/DiagTrack
- **Context Menu**: Classic Win10 menu, Open with Notepad, PowerShell here, Take Ownership
- **Personalization**: Wallpaper, desktop icons, custom fonts, lock screen, fonts, borders
- **Accessibility**: Cursors, keys, mouse trails, double-click speed, keyboard repeat

## Requirements

- Windows 10/11
- Python 3.8+
- Administrator privileges (for registry modifications)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

Or run the compiled executable (requires administrator privileges).

## Building

To create a standalone executable:
```bash
python build.py
```

## Update Log

### v2.0.0
- Added **75 new tweaks** spanning 5 brand-new tabs and expansions of existing ones
- New tabs: **Network**, **Power & Battery**, **Gaming**, **Security & Defender**, **Apps & Services**
- Taskbar: multi-display, tray chevron, hover-preview delay and notification-icon hide
- Explorer: This PC / User folder / Network / Recycle Bin / Control Panel desktop icons, jump-list privacy, full-folder navigation pane
- Performance: drag-window outline, configurable hung-app + wait-to-kill timeouts
- Context menu: PowerShell-here-as-admin, Cmd-here-as-admin, Take Ownership
- Personalization: lock screen tips/Spotlight, window border widths, ClearType toggle, translucent selection
- Accessibility: double-click speed, hover time, keyboard repeat delay/rate
- Generalized REG_SZ spinbox conversion in `tweak_manager.py` so future string-typed numeric tweaks need no special handler
- Bumped to `v2.0.0`


## Important!
-Most features will need pc restart to work, Dont forget to say any bugs you encounter!

## License

MIT
