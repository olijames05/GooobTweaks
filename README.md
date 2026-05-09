# WinTweaks v2.2.5

A Windows system tweaking tool inspired by GNOME Tweaks, designed to customize and optimize Windows settings through an intuitive graphical interface. **255 tweaks across 13 categories.**

## Features

### Taskbar (19 tweaks)
- Small icons, never-combine, transparency & transparency level
- Search box mode, Cortana button, Task View button
- Widgets, Chat/Teams, Chat Meet Now buttons
- Left-align, last-active click, no grouping, show seconds in clock
- Rounded corners, taskbar position (top/bottom/left/right)
- **NEW:** Auto-hide taskbar, always show all tray icons, End Task context menu (Win11), hide Meet Now button

### Explorer (29 tweaks)
- Show file extensions, hidden files, protected system files
- Compact view, launch to This PC / Quick Access / Downloads
- Full path in title bar & address bar, disable thumbnails
- Details pane, preview pane, item checkboxes, ribbon
- Quick Access, desktop icons (This PC, User, Network, Recycle Bin, Control Panel)
- Recent jump lists, nav pane all folders, sync provider ads, expand nav to current folder
- Recycle Bin no-confirm, show encrypted/compressed color
- **NEW:** Status bar, folder size in tooltips, disable simplified sharing wizard, separate process per window, icon cache size

### System (23 tweaks)
- Dark mode, accent color, Snap Assist, Aero Shake, edge swipe
- Sticky keys, filter keys, Caps Lock, NumLock at startup
- Auto-restart on crash, error reporting, Win+L disable, long paths
- Verbose status messages, remote UAC, Print Screen snipping, seconds in clock
- **NEW:** Delivery Optimization P2P mode, disable consumer experience/cloud features, disable startup sound, hardware clock UTC (dual-boot), disable automatic maintenance, max HTTP connections per server

### Network (19 tweaks)
- Disable IPv6, LLMNR, SMB1 client, Wi-Fi Sense, Remote Assistance, RDP
- Disable Teredo, NetBIOS WINS release on shutdown, link-local multicast, metered network updates
- **NEW:** Disable Nagle algorithm, QoS bandwidth reserve, DNS cache max TTL, WPAD (web proxy auto-discovery), RFC 1323 TCP extensions, SMB bandwidth throttling, NetBIOS broadcast name resolution, TCP task offloading, DNS name devolution

### Power & Battery (16 tweaks)
- Disable hibernate, fast startup, show hibernate/sleep/lock in power menu
- Disable CPU throttling, Modern Standby, unlock CPU minimum state
- **NEW:** Disable USB selective suspend, screen saver, Away Mode, Windows Power Throttling (EcoQoS), NDU network data usage service, SleepStudy, disk write-back cache, energy estimation sampling

### Gaming (21 tweaks)
- Disable Game Bar, Game Mode, Hardware-Accelerated GPU Scheduling (HAGS)
- Disable Fullscreen Optimizations (FSO), mouse acceleration, network throttling
- MMCSS responsiveness, disable Game DVR, disable VBS/Memory Integrity
- GPU priority boost, disable Multi-Plane Overlay (MPO), FSE behaviour, shader cache
- Raw input, High Performance power plan
- **NEW:** MMCSS NoLazyMode timer, disable Xbox Live Auth Manager, disable Xbox Live Game Save, disable Spectre/Meltdown mitigations ⚠, Games task SFIO priority, disable Xbox Game Monitoring service

### Performance (26 tweaks)
- Visual effects, menu delay, thumbnail cache, drag full windows
- Hung app / kill / service kill timeouts, startup delay, animate minimize
- Auto-end tasks, low disk space check, paging executive, NTFS last-access timestamp
- 8.3 short filenames, prefetcher, foreground app timeout, clear page file on shutdown
- Games CPU priority, Win32 priority separation
- **NEW:** Enable SSD TRIM, optimize memory for programs (not throughput), disable SFC boot scan ⚠, heap decommit threshold, disable WMI performance adapter, crash dump type, max HTTP connections per server

### Security & Defender (16 tweaks)
- UAC level, SmartScreen for apps & Edge, Defender real-time/cloud/sample submission
- Disable AutoRun, disable AutoPlay
- **NEW:** Disable LM password hash (NoLMHash), force NTLMv2 only, disable Windows Error Reporting service, disable default admin shares (C$/ADMIN$), disable Windows Script Host (.vbs/.js), require SMB packet signing, require NLA for Remote Desktop, disable Remote Registry service

### Privacy (19 tweaks)
- Telemetry level, advertising ID, Cortana, recent files, frequent folders
- Feedback frequency, activity history, inking & typing, app suggestions in Start
- Windows tips, welcome experience, map updates, lock screen ads
- **NEW:** Disable location services (global), disable camera access (global), disable microphone access (global), disable app launch tracking, disable ads in Settings, disable voice activation

### Apps & Services (19 tweaks)
- Disable OneDrive auto-start, Cortana auto-start, Store auto-update
- Disable Search indexing, SysMain/Superfetch, Print Spooler, DiagTrack
- Disable background apps, tips & suggestions, update auto-restart, silent app installs
- **NEW:** Disable Bing search in Start Menu, Edge startup preload, People Bar, News & Interests widget, Feedback Hub sampling, Shared Experiences (cross-device), Windows Ink Workspace button, Meet Now taskbar button

### Context Menu (8 tweaks)
- Classic Windows 10 context menu (Win11), Open with Notepad
- PowerShell Admin here, CMD Admin here, Take Ownership
- **NEW:** Add "Copy as Path", remove Share entry, remove Cast to Device entry

### Personalization (18 tweaks)
- Disable lock screen, blur, colorize Start, transparency, animations, shadows
- Rounded corners, boot animation, boot logo, cursor shadow, system beep, error beeps
- Lock screen tips, Spotlight, window border width, padded border, font smoothing, listview alpha

### Accessibility (22 tweaks)
- High contrast, large cursors, mouse trails, snap to default button
- Toggle keys, mouse keys, SoundSentry, ShowSounds, caret width
- Cursor blink, scroll lines, icon size, underline shortcuts
- Double-click speed, mouse hover time, keyboard delay & repeat rate
- **NEW:** Mouse pointer speed, scroll inactive windows on hover, touchpad natural scrolling, cursor size, ClickLock

## Requirements

- Windows 10 / 11
- Python 3.8+
- Administrator privileges (for registry modifications)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Or run the compiled executable (requires administrator privileges).

## Building

```bash
python build.py
```

## Update Log

### v2.2.5
- Added **75 new tweaks** across all 13 categories (255 total)
- New categories expanded: Network +9, Power +8, Security +8, Apps & Services +8, Performance +7, Gaming +6, Privacy +6, System +6, Accessibility +5, Explorer +5, Taskbar +4, Context Menu +3
- New special handlers: taskbar auto-hide (StuckRects3 binary), Copy as Path, blocked shell extensions (Share, Cast to Device)

### v2.0.0
- Initial release with 180 tweaks across 13 categories
- Added Network, Power, Gaming, Security, Apps & Services tabs
- Custom panels: video wallpaper, icon manager, wallpaper icons, custom fonts

## Important!

Most tweaks marked with ⚠ (Spectre mitigations, SFC scan disable) involve a security vs. performance trade-off — read the description before enabling. Most other tweaks require an Explorer restart or a full PC restart to take effect. Report any bugs you find!

## License

MIT
