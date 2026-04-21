"""
Windows Theme Manager - Apply color themes to Windows.
Supports Orange, Blue, Violet, and custom accent colors.
"""

import winreg
import ctypes
from typing import Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Theme:
    """Represents a Windows color theme."""
    name: str
    accent_color: str  # Hex color like "#0078D4"
    light_mode: bool
    transparency: bool
    taskbar_colorized: bool
    start_colorized: bool


class ThemeManager:
    """Manages Windows accent color themes."""
    
    # Predefined themes
    THEMES = {
        "default": Theme(
            name="Windows Default",
            accent_color="#0078D4",
            light_mode=True,
            transparency=True,
            taskbar_colorized=False,
            start_colorized=False
        ),
        "orange": Theme(
            name="Sunset Orange",
            accent_color="#FF6B35",
            light_mode=False,
            transparency=True,
            taskbar_colorized=True,
            start_colorized=True
        ),
        "blue": Theme(
            name="Ocean Blue",
            accent_color="#0066CC",
            light_mode=False,
            transparency=True,
            taskbar_colorized=True,
            start_colorized=True
        ),
        "violet": Theme(
            name="Royal Violet",
            accent_color="#7B2CBF",
            light_mode=False,
            transparency=True,
            taskbar_colorized=True,
            start_colorized=True
        ),
        "green": Theme(
            name="Forest Green",
            accent_color="#2D6A4F",
            light_mode=False,
            transparency=True,
            taskbar_colorized=True,
            start_colorized=True
        ),
        "red": Theme(
            name="Crimson Red",
            accent_color="#C9184A",
            light_mode=False,
            transparency=True,
            taskbar_colorized=True,
            start_colorized=True
        ),
        "pink": Theme(
            name="Neon Pink",
            accent_color="#FF006E",
            light_mode=False,
            transparency=True,
            taskbar_colorized=True,
            start_colorized=True
        ),
        "cyan": Theme(
            name="Electric Cyan",
            accent_color="#00B4D8",
            light_mode=False,
            transparency=True,
            taskbar_colorized=True,
            start_colorized=True
        ),
        "yellow": Theme(
            name="Golden Yellow",
            accent_color="#FFB703",
            light_mode=True,
            transparency=True,
            taskbar_colorized=True,
            start_colorized=True
        ),
        "purple": Theme(
            name="Deep Purple",
            accent_color="#7209B7",
            light_mode=False,
            transparency=True,
            taskbar_colorized=True,
            start_colorized=True
        ),
        "teal": Theme(
            name="Teal Wave",
            accent_color="#0A9396",
            light_mode=False,
            transparency=True,
            taskbar_colorized=True,
            start_colorized=True
        ),
        "black": Theme(
            name="Midnight Black",
            accent_color="#333333",
            light_mode=False,
            transparency=False,
            taskbar_colorized=True,
            start_colorized=True
        ),
    }
    
    def __init__(self):
        self.personalize_key = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        self.colors_key = r"Software\Microsoft\Windows\DWM"
    
    def apply_theme(self, theme_id: str) -> bool:
        """
        Apply a predefined theme.
        
        Args:
            theme_id: Key from THEMES dict
        
        Returns:
            True if successful
        """
        theme = self.THEMES.get(theme_id)
        if not theme:
            return False
        
        return self._apply_theme_settings(theme)
    
    def apply_custom_theme(self, accent_color: str, light_mode: bool = False,
                          transparency: bool = True, colorize_taskbar: bool = True,
                          colorize_start: bool = True) -> bool:
        """
        Apply a custom color theme.
        
        Args:
            accent_color: Hex color code (e.g., "#FF5733")
            light_mode: Use light mode
            transparency: Enable transparency effects
            colorize_taskbar: Apply accent to taskbar
            colorize_start: Apply accent to start menu
        """
        theme = Theme(
            name="Custom",
            accent_color=accent_color,
            light_mode=light_mode,
            transparency=transparency,
            taskbar_colorized=colorize_taskbar,
            start_colorized=colorize_start
        )
        
        return self._apply_theme_settings(theme)
    
    def _apply_theme_settings(self, theme: Theme) -> bool:
        """Apply theme settings to registry."""
        try:
            # Convert hex color to Windows color format (BGR)
            color_hex = theme.accent_color.lstrip("#")
            r = int(color_hex[0:2], 16)
            g = int(color_hex[2:4], 16)
            b = int(color_hex[4:6], 16)
            # Windows uses BGR format
            color_value = (b << 16) | (g << 8) | r
            
            # Set accent color
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.colors_key, 0, 
                               winreg.KEY_WRITE) as key:
                winreg.SetValueEx(key, "AccentColor", 0, winreg.REG_DWORD, color_value)
            
            # Set personalization settings
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.personalize_key, 0,
                               winreg.KEY_WRITE) as key:
                # Light/Dark mode
                winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, 
                                 1 if theme.light_mode else 0)
                winreg.SetValueEx(key, "SystemUsesLightTheme", 0, winreg.REG_DWORD,
                                 1 if theme.light_mode else 0)
                
                # Transparency
                winreg.SetValueEx(key, "EnableTransparency", 0, winreg.REG_DWORD,
                                 1 if theme.transparency else 0)
                
                # Colorize taskbar and start
                color_prevalence = 1 if (theme.taskbar_colorized or theme.start_colorized) else 0
                winreg.SetValueEx(key, "ColorPrevalence", 0, winreg.REG_DWORD, color_prevalence)
            
            # Notify Windows of changes
            self._refresh_theme()
            
            return True
            
        except Exception as e:
            print(f"Error applying theme: {e}")
            return False
    
    def get_current_accent_color(self) -> str:
        """Get the current accent color as hex."""
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.colors_key, 0,
                               winreg.KEY_READ) as key:
                color_value, _ = winreg.QueryValueEx(key, "AccentColor")
                
                # Convert BGR to RGB hex
                b = (color_value >> 16) & 0xFF
                g = (color_value >> 8) & 0xFF
                r = color_value & 0xFF
                
                return f"#{r:02X}{g:02X}{b:02X}"
        except:
            return "#0078D4"
    
    def is_dark_mode(self) -> bool:
        """Check if dark mode is currently enabled."""
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.personalize_key, 0,
                               winreg.KEY_READ) as key:
                value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                return value == 0
        except:
            return False
    
    def set_dark_mode(self, enabled: bool) -> bool:
        """Enable or disable dark mode."""
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.personalize_key, 0,
                               winreg.KEY_WRITE) as key:
                value = 0 if enabled else 1
                winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, value)
                winreg.SetValueEx(key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, value)
            
            self._refresh_theme()
            return True
        except Exception as e:
            print(f"Error setting dark mode: {e}")
            return False
    
    def _refresh_theme(self):
        """Notify Windows to refresh theme settings."""
        # Send WM_SETTINGCHANGE
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        SMTO_ABORTIFHUNG = 0x0002
        
        result = ctypes.c_long()
        ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST,
            WM_SETTINGCHANGE,
            0,
            ctypes.c_wchar_p("ImmersiveColorSet"),
            SMTO_ABORTIFHUNG,
            5000,
            ctypes.byref(result)
        )
    
    def get_available_themes(self) -> Dict[str, str]:
        """Get list of available theme IDs and names."""
        return {k: v.name for k, v in self.THEMES.items()}
