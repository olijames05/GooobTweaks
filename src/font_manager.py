"""
System font management utilities.
Allows changing system fonts that Windows doesn't expose in Settings.
"""

import winreg
import ctypes
from typing import Dict, Optional


class FontManager:
    """Manages system fonts."""
    
    # Font substitution key
    FONT_SUBSTITUTES_KEY = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\FontSubstitutes"
    FONT_LINK_KEY = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\FontLink\SystemLink"
    
    # Common Windows UI font elements
    FONT_ELEMENTS = {
        "Caption": "Window title bar font",
        "SmCaption": "Small window caption font",
        "Menu": "Menu font",
        "Message": "Message box font",
        "Status": "Status bar font",
        "Icon": "Icon font",
        "Tooltip": "Tooltip font"
    }
    
    def __init__(self):
        self._original_fonts: Dict[str, str] = {}
        self._save_original_fonts()
    
    def _save_original_fonts(self):
        """Save the original font settings."""
        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Control Panel\Desktop\WindowMetrics",
                0,
                winreg.KEY_READ
            ) as key:
                for element in self.FONT_ELEMENTS.keys():
                    try:
                        value, _ = winreg.QueryValueEx(key, f"{element}Font")
                        self._original_fonts[element] = value
                    except:
                        pass
        except Exception as e:
            print(f"Error saving original fonts: {e}")
    
    def set_ui_font(self, font_name: str, font_size: int = 9, element: str = "all") -> bool:
        """
        Set the font for UI elements.
        
        Args:
            font_name: Name of the font (must be installed)
            font_size: Font size in points
            element: Which element to change ("all" or specific element name)
        
        Returns:
            True if successful
        """
        try:
            # Font format in WindowMetrics: "name,height,weight,italic,charset"
            # Height is negative point size
            font_value = f"{font_name},-{font_size},0,0,0"
            
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Control Panel\Desktop\WindowMetrics",
                0,
                winreg.KEY_WRITE
            ) as key:
                
                if element == "all":
                    for elem in self.FONT_ELEMENTS.keys():
                        winreg.SetValueEx(key, f"{elem}Font", 0, winreg.REG_SZ, font_value)
                else:
                    winreg.SetValueEx(key, f"{element}Font", 0, winreg.REG_SZ, font_value)
            
            # Notify system of change
            self._refresh_fonts()
            return True
            
        except Exception as e:
            print(f"Error setting font: {e}")
            return False
    
    def set_system_font(self, font_name: str) -> bool:
        """
        Set the system-wide default font by modifying font substitutes.
        This changes the default font used when applications request "MS Shell Dlg".
        
        Args:
            font_name: Name of the font to use
        """
        try:
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                self.FONT_SUBSTITUTES_KEY,
                0,
                winreg.KEY_WRITE
            ) as key:
                # Set font substitutes for common system font aliases
                substitutes = [
                    "MS Shell Dlg",
                    "MS Shell Dlg 2",
                    "Tahoma",
                    "Microsoft Sans Serif"
                ]
                
                for substitute in substitutes:
                    winreg.SetValueEx(key, substitute, 0, winreg.REG_SZ, font_name)
            
            return True
            
        except Exception as e:
            print(f"Error setting system font: {e}")
            return False
    
    def restore_default_fonts(self) -> bool:
        """Restore the original font settings."""
        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Control Panel\Desktop\WindowMetrics",
                0,
                winreg.KEY_WRITE
            ) as key:
                for element, value in self._original_fonts.items():
                    winreg.SetValueEx(key, f"{element}Font", 0, winreg.REG_SZ, value)
            
            self._refresh_fonts()
            return True
            
        except Exception as e:
            print(f"Error restoring fonts: {e}")
            return False
    
    def get_installed_fonts(self) -> list:
        """Get a list of installed font names."""
        fonts = []
        
        try:
            # Get fonts from Windows Fonts folder
            import os
            fonts_path = os.path.expandvars(r"%SystemRoot%\Fonts")
            
            for file in os.listdir(fonts_path):
                if file.lower().endswith(('.ttf', '.otf', '.ttc')):
                    # Remove extension for display
                    font_name = os.path.splitext(file)[0]
                    fonts.append(font_name)
            
            # Also check registry for proper font names
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts",
                0,
                winreg.KEY_READ
            ) as key:
                index = 0
                while True:
                    try:
                        name, _, _ = winreg.EnumValue(key, index)
                        # Extract font name from "FontName (TrueType)" format
                        if "(TrueType)" in name:
                            font_name = name.replace(" (TrueType)", "").strip()
                            if font_name not in fonts:
                                fonts.append(font_name)
                        index += 1
                    except OSError:
                        break
            
            return sorted(set(fonts))
            
        except Exception as e:
            print(f"Error getting fonts: {e}")
            return ["Segoe UI", "Arial", "Calibri", "Tahoma", "Verdana"]
    
    def get_current_fonts(self) -> Dict[str, str]:
        """Get the current font settings for all elements."""
        fonts = {}
        
        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Control Panel\Desktop\WindowMetrics",
                0,
                winreg.KEY_READ
            ) as key:
                for element in self.FONT_ELEMENTS.keys():
                    try:
                        value, _ = winreg.QueryValueEx(key, f"{element}Font")
                        # Parse "name,height,weight,italic,charset"
                        parts = value.split(",")
                        fonts[element] = {
                            "name": parts[0] if parts else "Segoe UI",
                            "size": abs(int(parts[1])) if len(parts) > 1 and parts[1] else 9
                        }
                    except:
                        fonts[element] = {"name": "Segoe UI", "size": 9}
                        
        except Exception as e:
            print(f"Error getting current fonts: {e}")
        
        return fonts
    
    def _refresh_fonts(self):
        """Notify Windows to refresh font settings."""
        # Send WM_SETTINGCHANGE message
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        SMTO_ABORTIFHUNG = 0x0002
        
        result = ctypes.c_long()
        ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST,
            WM_SETTINGCHANGE,
            0,
            ctypes.c_wchar_p("WindowMetrics"),
            SMTO_ABORTIFHUNG,
            5000,
            ctypes.byref(result)
        )
    
    def change_dpi_scaling(self, scaling_percent: int) -> bool:
        """
        Change system DPI scaling.
        
        Args:
            scaling_percent: DPI scaling percentage (100, 125, 150, etc.)
        """
        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Control Panel\Desktop",
                0,
                winreg.KEY_WRITE
            ) as key:
                # LogPixels value = scaling_percent * 96 / 100
                log_pixels = int(scaling_percent * 96 / 100)
                winreg.SetValueEx(key, "LogPixels", 0, winreg.REG_DWORD, log_pixels)
            
            return True
            
        except Exception as e:
            print(f"Error changing DPI: {e}")
            return False
