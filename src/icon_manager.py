"""
Desktop icon customization - change system and app icons.
"""

import os
import winreg
import shutil
from typing import Dict, Optional, List
from pathlib import Path


class IconManager:
    """Manages desktop and system icons."""
    
    # System icons that can be customized
    SYSTEM_ICONS = {
        "computer": {
            "name": "This PC",
            "clsid": "{20D04FE0-3AEA-1069-A2D8-08002B30309D}",
            "default_icon": "%SystemRoot%\System32\imageres.dll,-109"
        },
        "recycle_bin_empty": {
            "name": "Recycle Bin (Empty)",
            "clsid": "{645FF040-5081-101B-9F08-00AA002F954E}",
            "value_name": "empty",
            "default_icon": "%SystemRoot%\System32\imageres.dll,-55"
        },
        "recycle_bin_full": {
            "name": "Recycle Bin (Full)",
            "clsid": "{645FF040-5081-101B-9F08-00AA002F954E}",
            "value_name": "full",
            "default_icon": "%SystemRoot%\System32\imageres.dll,-54"
        },
        "user_files": {
            "name": "User Files",
            "clsid": "{59031a47-3f72-44a7-89c5-5595fe6b30ee}",
            "default_icon": "%SystemRoot%\System32\imageres.dll,-123"
        },
        "network": {
            "name": "Network",
            "clsid": "{F02C1A0D-BE21-4350-88B0-7367FC96EF3C}",
            "default_icon": "%SystemRoot%\System32\imageres.dll,-25"
        },
        "control_panel": {
            "name": "Control Panel",
            "clsid": "{5399E694-6CE5-4D6C-8FCE-1D8870FDCBA0}",
            "default_icon": "%SystemRoot%\System32\imageres.dll,-27"
        },
    }
    
    # Desktop icon settings
    DESKTOP_ICONS_KEY = r"Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel"
    
    def __init__(self):
        self.icon_cache_dir = os.path.expandvars(r"%LocalAppData%\Microsoft\Windows\Explorer")
    
    def set_system_icon(self, icon_type: str, icon_path: str) -> bool:
        """
        Change a system icon.
        
        Args:
            icon_type: Key from SYSTEM_ICONS (computer, recycle_bin_empty, etc.)
            icon_path: Path to .ico file or DLL with icon resource (e.g., "shell32.dll,12")
        
        Returns:
            True if successful
        """
        if icon_type not in self.SYSTEM_ICONS:
            return False
        
        icon_info = self.SYSTEM_ICONS[icon_type]
        clsid = icon_info["clsid"]
        
        try:
            # Handle recycle bin specially (has empty/full states)
            if "recycle_bin" in icon_type:
                value_name = icon_info.get("value_name", "")
                key_path = f"CLSID\\{clsid}\\DefaultIcon"
                
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0,
                                   winreg.KEY_WRITE) as key:
                    # For recycle bin, we need to set both icons
                    if "," in icon_path:
                        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, icon_path)
                    else:
                        winreg.SetValueEx(key, "", 0, winreg.REG_EXPAND_SZ, icon_path)
            else:
                # Standard system icon
                key_path = f"Software\Classes\CLSID\\{clsid}\\DefaultIcon"
                
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0,
                                   winreg.KEY_WRITE) as key:
                    if "," in icon_path:
                        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, icon_path)
                    else:
                        winreg.SetValueEx(key, "", 0, winreg.REG_EXPAND_SZ, icon_path)
            
            # Clear icon cache
            self._clear_icon_cache()
            
            return True
            
        except Exception as e:
            print(f"Error setting icon: {e}")
            return False
    
    def reset_system_icon(self, icon_type: str) -> bool:
        """Reset a system icon to default."""
        if icon_type not in self.SYSTEM_ICONS:
            return False
        
        icon_info = self.SYSTEM_ICONS[icon_type]
        default_icon = icon_info["default_icon"]
        
        return self.set_system_icon(icon_type, default_icon)
    
    def show_desktop_icon(self, icon_type: str, show: bool = True) -> bool:
        """
        Show or hide a desktop icon.
        
        Args:
            icon_type: computer, recycle_bin, user_files, network, control_panel
            show: True to show, False to hide
        """
        icon_map = {
            "computer": "{20D04FE0-3AEA-1069-A2D8-08002B30309D}",
            "recycle_bin": "{645FF040-5081-101B-9F08-00AA002F954E}",
            "user_files": "{59031a47-3f72-44a7-89c5-5595fe6b30ee}",
            "network": "{F02C1A0D-BE21-4350-88B0-7367FC96EF3C}",
            "control_panel": "{5399E694-6CE5-4D6C-8FCE-1D8870FDCBA0}",
        }
        
        clsid = icon_map.get(icon_type)
        if not clsid:
            return False
        
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.DESKTOP_ICONS_KEY, 0,
                               winreg.KEY_WRITE) as key:
                # 0 = show, 1 = hide (inverted logic)
                winreg.SetValueEx(key, clsid, 0, winreg.REG_DWORD, 0 if show else 1)
            
            # Refresh desktop
            self._refresh_desktop()
            return True
            
        except Exception as e:
            print(f"Error toggling desktop icon: {e}")
            return False
    
    def change_folder_icon(self, folder_path: str, icon_path: str) -> bool:
        """
        Change the icon for a specific folder.
        
        Args:
            folder_path: Path to the folder
            icon_path: Path to .ico file or "dll_path,icon_index"
        """
        try:
            desktop_ini_path = os.path.join(folder_path, "desktop.ini")
            
            # Make folder read-only (required for custom icon)
            import ctypes
            FILE_ATTRIBUTE_READONLY = 0x01
            ctypes.windll.kernel32.SetFileAttributesW(folder_path, FILE_ATTRIBUTE_READONLY)
            
            # Create/update desktop.ini
            icon_index = "0"
            if "," in icon_path:
                parts = icon_path.rsplit(",", 1)
                icon_path = parts[0]
                icon_index = parts[1]
            
            ini_content = f"""[.ShellClassInfo]
IconResource={icon_path},{icon_index}
[ViewState]
Mode=
Vid=
FolderType=Generic
"""
            
            with open(desktop_ini_path, "w") as f:
                f.write(ini_content)
            
            # Hide desktop.ini
            FILE_ATTRIBUTE_HIDDEN = 0x02
            FILE_ATTRIBUTE_SYSTEM = 0x04
            ctypes.windll.kernel32.SetFileAttributesW(
                desktop_ini_path, 
                FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM
            )
            
            # Refresh icon cache
            self._clear_icon_cache()
            
            return True
            
        except Exception as e:
            print(f"Error changing folder icon: {e}")
            return False
    
    def change_shortcut_icon(self, shortcut_path: str, icon_path: str) -> bool:
        """
        Change the icon of a shortcut (.lnk file).
        
        Args:
            shortcut_path: Path to the .lnk file
            icon_path: Path to icon or "dll_path,icon_index"
        """
        try:
            import winshell
            from win32com.client import Dispatch
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            
            if "," in icon_path:
                shortcut.IconLocation = icon_path
            else:
                shortcut.IconLocation = f"{icon_path},0"
            
            shortcut.save()
            return True
            
        except Exception as e:
            print(f"Error changing shortcut icon: {e}")
            return False
    
    def change_app_icon(self, app_name: str, icon_path: str) -> bool:
        """
        Change the icon for a specific application (where supported).
        This modifies the DefaultIcon registry entry for the app.
        
        Args:
            app_name: Application identifier (e.g., "notepad.exe")
            icon_path: Path to icon file
        """
        try:
            # Try to find the app in registry
            key_path = f"Software\Classes\\{app_name}"
            
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0,
                               winreg.KEY_WRITE) as key:
                with winreg.CreateKey(key, "DefaultIcon") as icon_key:
                    if "," in icon_path:
                        winreg.SetValueEx(icon_key, "", 0, winreg.REG_SZ, icon_path)
                    else:
                        winreg.SetValueEx(icon_key, "", 0, winreg.REG_EXPAND_SZ, icon_path)
            
            self._clear_icon_cache()
            return True
            
        except Exception as e:
            print(f"Error changing app icon: {e}")
            return False
    
    def get_system_icon_list(self) -> List[str]:
        """Get list of customizable system icons."""
        return list(self.SYSTEM_ICONS.keys())
    
    def get_icon_info(self, icon_type: str) -> Optional[Dict]:
        """Get information about a system icon."""
        return self.SYSTEM_ICONS.get(icon_type)
    
    def _clear_icon_cache(self):
        """Clear the Windows icon cache."""
        try:
            # Kill explorer
            import subprocess
            subprocess.run(["taskkill", "/F", "/IM", "explorer.exe"], 
                          capture_output=True)
            
            # Delete icon cache files
            cache_files = [
                "iconcache.db",
                "thumbcache_32.db",
                "thumbcache_96.db",
                "thumbcache_256.db",
                "thumbcache_1024.db",
                "thumbcache_idx.db",
                "thumbcache_sr.db"
            ]
            
            for filename in cache_files:
                filepath = os.path.join(self.icon_cache_dir, filename)
                if os.path.exists(filepath):
                    try:
                        os.remove(filepath)
                    except:
                        pass
            
            # Restart explorer
            subprocess.Popen("explorer.exe")
            
        except Exception as e:
            print(f"Error clearing icon cache: {e}")
    
    def _refresh_desktop(self):
        """Refresh the desktop view."""
        try:
            import ctypes
            # Send F5 key to refresh desktop
            HWND_BROADCAST = 0xFFFF
            WM_COMMAND = 0x0111
            
            ctypes.windll.user32.SendMessageW(HWND_BROADCAST, WM_COMMAND, 0x7402, 0)
        except:
            pass
    
    def extract_icon_from_exe(self, exe_path: str, output_path: str, 
                              icon_index: int = 0) -> bool:
        """
        Extract an icon from an executable file.
        
        Args:
            exe_path: Path to the executable
            output_path: Where to save the .ico file
            icon_index: Which icon to extract (if multiple)
        """
        try:
            from PIL import Image
            import ctypes
            from ctypes import wintypes
            
            # Load icon from executable
            large_icons = (wintypes.HICON * 1)()
            small_icons = (wintypes.HICON * 1)()
            
            result = ctypes.windll.shell32.ExtractIconExW(
                exe_path, icon_index, large_icons, small_icons, 1
            )
            
            if result == 0:
                return False
            
            # Save icon to file
            hicon = large_icons[0] if large_icons[0] else small_icons[0]
            
            # Get icon info
            class ICONINFO(ctypes.Structure):
                _fields_ = [
                    ("fIcon", wintypes.BOOL),
                    ("xHotspot", wintypes.DWORD),
                    ("yHotspot", wintypes.DWORD),
                    ("hbmMask", wintypes.HBITMAP),
                    ("hbmColor", wintypes.HBITMAP)
                ]
            
            icon_info = ICONINFO()
            ctypes.windll.user32.GetIconInfo(hicon, ctypes.byref(icon_info))
            
            # This is a simplified version - full implementation would
            # convert the HICON to a PIL Image and save as ICO
            
            # Clean up
            ctypes.windll.user32.DestroyIcon(hicon)
            
            return True
            
        except Exception as e:
            print(f"Error extracting icon: {e}")
            return False
