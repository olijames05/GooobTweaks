"""
Video wallpaper support using external players.
Supports MP4, WebM, and other video formats.
"""

import os
import subprocess
import ctypes
import winreg
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Callable
import threading
import time


class VideoWallpaperManager:
    """Manages video wallpapers using various playback methods."""
    
    def __init__(self):
        self._video_process: Optional[subprocess.Popen] = None
        self._stop_event = threading.Event()
        self._worker_thread: Optional[threading.Thread] = None
        self._current_video: Optional[str] = None
        self._wallpaper_hwnd: Optional[int] = None
        self._temp_dir = tempfile.mkdtemp(prefix="wintweaks_video_")
    
    def is_supported(self) -> bool:
        """Check if video wallpaper is supported on this system."""
        # Check for Windows 10/11
        try:
            import sys
            return sys.platform == "win32"
        except:
            return False
    
    def set_video_wallpaper(self, video_path: str, audio: bool = False, 
                           playback_speed: float = 1.0) -> bool:
        """
        Set a video as the desktop wallpaper.
        
        Args:
            video_path: Path to the video file (MP4, WebM, AVI, etc.)
            audio: Whether to play audio (default: False)
            playback_speed: Playback speed multiplier
        
        Returns:
            True if successful
        """
        if not os.path.exists(video_path):
            return False
        
        # Stop any existing video wallpaper
        self.stop_video_wallpaper()
        
        self._current_video = video_path
        
        # Use the most reliable method available
        if self._try_active_movie_method(video_path, audio, playback_speed):
            return True
        elif self._try_vlc_method(video_path, audio, playback_speed):
            return True
        elif self._try_mpv_method(video_path, audio, playback_speed):
            return True
        elif self._try_ffmpeg_method(video_path, playback_speed):
            return True
        
        return False
    
    def _try_active_movie_method(self, video_path: str, audio: bool, 
                                  playback_speed: float) -> bool:
        """
        Try to use Active Desktop / Windows Media Player method.
        This works on older Windows versions.
        """
        try:
            # Create an HTML file that embeds the video
            html_content = f"""<!DOCTYPE html>
<html>
<head>
<style>
body {{ margin: 0; padding: 0; overflow: hidden; background: black; }}
video {{ width: 100%; height: 100%; object-fit: cover; }}
</style>
</head>
<body>
<video autoplay loop muted={"false" if audio else "true"} playsinline>
    <source src="{video_path}" type="video/mp4">
</video>
</body>
</html>"""
            
            html_path = os.path.join(self._temp_dir, "wallpaper.html")
            with open(html_path, "w") as f:
                f.write(html_content)
            
            # Use Windows API to set HTML wallpaper
            # This requires Active Desktop which was removed in Windows 10
            # But we'll try anyway for compatibility
            spi_setdeskwallpaper = 20
            spi_updateinifile = 0x01
            spi_sendchange = 0x02
            
            result = ctypes.windll.user32.SystemParametersInfoW(
                spi_setdeskwallpaper,
                0,
                html_path,
                spi_updateinifile | spi_sendchange
            )
            
            return result != 0
            
        except Exception as e:
            print(f"Active Movie method failed: {e}")
            return False
    
    def _try_vlc_method(self, video_path: str, audio: bool, 
                        playback_speed: float) -> bool:
        """Try to use VLC for video wallpaper."""
        vlc_paths = [
            r"C:\Program Files\VideoLAN\VLC\vlc.exe",
            r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe",
        ]
        
        vlc_path = None
        for path in vlc_paths:
            if os.path.exists(path):
                vlc_path = path
                break
        
        if not vlc_path:
            return False
        
        try:
            # VLC command to play video as wallpaper
            # --video-wallpaper flag makes it draw directly to desktop
            cmd = [
                vlc_path,
                "--video-wallpaper",
                "--loop",
                "--no-video-title-show",
                "--rate", str(playback_speed),
            ]
            
            if not audio:
                cmd.append("--volume=0")
            
            cmd.append(video_path)
            
            self._video_process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            return True
            
        except Exception as e:
            print(f"VLC method failed: {e}")
            return False
    
    def _try_mpv_method(self, video_path: str, audio: bool,
                        playback_speed: float) -> bool:
        """Try to use MPV for video wallpaper."""
        mpv_paths = [
            r"C:\Program Files\mpv\mpv.exe",
            r"C:\Program Files (x86)\mpv\mpv.exe",
            r"C:\mpv\mpv.exe",
            "mpv",  # If in PATH
        ]
        
        mpv_path = None
        for path in mpv_paths:
            if os.path.exists(path) or shutil.which(path):
                mpv_path = path if os.path.exists(path) else path
                break
        
        if not mpv_path:
            return False
        
        try:
            # MPV command for wallpaper mode
            cmd = [
                mpv_path,
                "--loop-file=inf",
                "--speed", str(playback_speed),
                "--no-osc",
                "--no-osd-bar",
                "--no-border",
                "--fs",
                "--ontop",
                "--geometry=100%:100%",
            ]
            
            if not audio:
                cmd.append("--mute=yes")
            
            cmd.append(video_path)
            
            self._video_process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            return True
            
        except Exception as e:
            print(f"MPV method failed: {e}")
            return False
    
    def _try_ffmpeg_method(self, video_path: str, playback_speed: float) -> bool:
        """
        Use FFmpeg to extract frames and cycle through them.
        This is a fallback method that doesn't require video players.
        """
        try:
            import subprocess
            import glob
            
            # Check if ffmpeg exists
            ffmpeg_path = shutil.which("ffmpeg") or r"C:\ffmpeg\bin\ffmpeg.exe"
            if not os.path.exists(ffmpeg_path):
                return False
            
            # Create frames directory
            frames_dir = os.path.join(self._temp_dir, "frames")
            os.makedirs(frames_dir, exist_ok=True)
            
            # Extract frames from video
            frame_pattern = os.path.join(frames_dir, "frame_%04d.jpg")
            
            cmd = [
                ffmpeg_path,
                "-i", video_path,
                "-vf", "fps=10,scale=1920:-1:flags=lanczos",
                "-q:v", "3",
                frame_pattern
            ]
            
            # Run extraction (this may take a moment)
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
            
            # Get all extracted frames
            frames = sorted(glob.glob(os.path.join(frames_dir, "frame_*.jpg")))
            
            if not frames:
                return False
            
            # Start cycling through frames
            self._stop_event.clear()
            
            def frame_cycle():
                from wallpaper_manager import WallpaperManager
                wm = WallpaperManager()
                
                interval = 0.1 / playback_speed  # 10 fps
                index = 0
                
                while not self._stop_event.is_set():
                    frame = frames[index % len(frames)]
                    wm.set_static_wallpaper(frame, "fill")
                    time.sleep(interval)
                    index += 1
            
            self._worker_thread = threading.Thread(target=frame_cycle, daemon=True)
            self._worker_thread.start()
            
            return True
            
        except Exception as e:
            print(f"FFmpeg method failed: {e}")
            return False
    
    def stop_video_wallpaper(self):
        """Stop the video wallpaper."""
        self._stop_event.set()
        
        # Stop external player process
        if self._video_process:
            try:
                self._video_process.terminate()
                self._video_process.wait(timeout=2)
            except:
                try:
                    self._video_process.kill()
                except:
                    pass
            self._video_process = None
        
        # Stop worker thread
        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=2)
            self._worker_thread = None
        
        self._current_video = None
    
    def is_playing(self) -> bool:
        """Check if a video wallpaper is currently playing."""
        if self._video_process:
            return self._video_process.poll() is None
        if self._worker_thread:
            return self._worker_thread.is_alive()
        return False
    
    def get_current_video(self) -> Optional[str]:
        """Get the path to the currently playing video."""
        return self._current_video
    
    def pause(self):
        """Pause the video wallpaper (if supported by player)."""
        # This would require window handle manipulation
        # For now, we'll just note it's not fully implemented
        pass
    
    def resume(self):
        """Resume the video wallpaper."""
        pass
    
    def cleanup(self):
        """Clean up temporary files."""
        self.stop_video_wallpaper()
        try:
            if os.path.exists(self._temp_dir):
                shutil.rmtree(self._temp_dir)
        except:
            pass
