"""
Wallpaper management utilities.
Allows changing wallpaper even on unactivated Windows.
Supports static images and animated wallpapers.
"""

import os
import ctypes
import winreg
from pathlib import Path
from typing import Optional, Callable
import threading
import time


class WallpaperManager:
    """Manages desktop wallpaper settings."""
    
    # Windows SPI constants
    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINIFILE = 0x01
    SPIF_SENDCHANGE = 0x02
    
    def __init__(self):
        self._animated_wallpaper_thread: Optional[threading.Thread] = None
        self._stop_animation = threading.Event()
        self._animated_wallpaper_callback: Optional[Callable] = None
    
    def set_static_wallpaper(self, image_path: str, style: str = "fill") -> bool:
        """
        Set a static wallpaper image.
        Works even on unactivated Windows by using SystemParametersInfo.
        
        Args:
            image_path: Path to the image file
            style: Wallpaper style - "fill", "fit", "stretch", "tile", "center", "span"
        
        Returns:
            True if successful
        """
        if not os.path.exists(image_path):
            return False
        
        # Convert to absolute path
        image_path = os.path.abspath(image_path)
        
        # Set wallpaper style in registry
        style_map = {
            "fill": "10",
            "fit": "6",
            "stretch": "2",
            "tile": "1",
            "center": "0",
            "span": "22"
        }
        
        try:
            # Set the wallpaper style
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Control Panel\Desktop",
                0,
                winreg.KEY_WRITE
            ) as key:
                winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, style_map.get(style, "10"))
                winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "0" if style != "tile" else "1")
            
            # Apply the wallpaper using SystemParametersInfo
            # This bypasses the activation check!
            result = ctypes.windll.user32.SystemParametersInfoW(
                self.SPI_SETDESKWALLPAPER,
                0,
                image_path,
                self.SPIF_UPDATEINIFILE | self.SPIF_SENDCHANGE
            )
            
            return result != 0
            
        except Exception as e:
            print(f"Error setting wallpaper: {e}")
            return False
    
    def get_current_wallpaper(self) -> Optional[str]:
        """Get the path to the current wallpaper."""
        try:
            buffer = ctypes.create_unicode_buffer(512)
            ctypes.windll.user32.SystemParametersInfoW(
                0x73,  # SPI_GETDESKWALLPAPER
                512,
                buffer,
                0
            )
            path = buffer.value
            return path if os.path.exists(path) else None
        except Exception as e:
            print(f"Error getting wallpaper: {e}")
            return None
    
    def set_solid_color(self, color: str) -> bool:
        """
        Set a solid color as wallpaper.
        
        Args:
            color: Hex color code (e.g., "#FF5733")
        """
        try:
            # Remove # if present
            color = color.lstrip("#")
            
            # Convert to RGB tuple for Windows
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
            
            # Set background color in registry
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Control Panel\Colors",
                0,
                winreg.KEY_WRITE
            ) as key:
                winreg.SetValueEx(key, "Background", 0, winreg.REG_SZ, f"{r} {g} {b}")
            
            # Apply changes
            ctypes.windll.user32.SetSysColors(
                1,
                ctypes.c_int(1),  # COLOR_BACKGROUND
                ctypes.c_int((r << 16) | (g << 8) | b)
            )
            
            return True
            
        except Exception as e:
            print(f"Error setting solid color: {e}")
            return False
    
    def start_animated_wallpaper(self, image_paths: list, interval: float = 5.0) -> bool:
        """
        Start an animated wallpaper that cycles through images.
        
        Args:
            image_paths: List of image paths to cycle through
            interval: Seconds between each image
        """
        if not image_paths:
            return False
        
        # Stop any existing animation
        self.stop_animated_wallpaper()
        
        self._stop_animation.clear()
        
        def animation_loop():
            index = 0
            while not self._stop_animation.is_set():
                image_path = image_paths[index % len(image_paths)]
                if os.path.exists(image_path):
                    self.set_static_wallpaper(image_path)
                    if self._animated_wallpaper_callback:
                        self._animated_wallpaper_callback(index, image_path)
                
                # Wait for interval or until stopped
                self._stop_animation.wait(interval)
                index += 1
        
        self._animated_wallpaper_thread = threading.Thread(
            target=animation_loop,
            daemon=True
        )
        self._animated_wallpaper_thread.start()
        return True
    
    def stop_animated_wallpaper(self):
        """Stop the animated wallpaper."""
        if self._animated_wallpaper_thread and self._animated_wallpaper_thread.is_alive():
            self._stop_animation.set()
            self._animated_wallpaper_thread.join(timeout=1.0)
            self._animated_wallpaper_thread = None
    
    def is_animation_running(self) -> bool:
        """Check if animated wallpaper is currently running."""
        return (self._animated_wallpaper_thread is not None and 
                self._animated_wallpaper_thread.is_alive())
    
    def set_animated_wallpaper_callback(self, callback: Callable):
        """Set a callback function called when wallpaper changes during animation."""
        self._animated_wallpaper_callback = callback
    
    def get_windows_wallpaper_folder(self) -> str:
        """Get the path to Windows' default wallpaper folder."""
        return os.path.expandvars(r"%SystemRoot%\Web\Wallpaper")
    
    def get_spotlight_images(self) -> list:
        """Get Windows Spotlight images if available."""
        spotlight_path = os.path.expandvars(
            r"%LocalAppData%\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets"
        )
        
        if not os.path.exists(spotlight_path):
            return []
        
        images = []
        for file in os.listdir(spotlight_path):
            file_path = os.path.join(spotlight_path, file)
            # Spotlight files have no extension, check if they're images
            if os.path.isfile(file_path) and os.path.getsize(file_path) > 100000:  # > 100KB
                images.append(file_path)
        
        return images
