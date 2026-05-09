"""
Tweak manager - handles applying and reading tweak states.
"""

import winreg
from typing import Any, Dict, Optional
from tweaks import ALL_TWEAKS, Tweak, RegistryChange
from registry_utils import read_registry_value, write_registry_value, delete_registry_value


class TweakManager:
    """Manages Windows tweaks - reading current states and applying changes."""
    
    def __init__(self):
        self.tweaks = {tweak.id: tweak for tweak in ALL_TWEAKS}
        self._special_handlers = {
            "taskbar_search_box": self._handle_search_box,
            "explorer_launch_to": self._handle_launch_to,
            "perf_menu_delay": self._handle_menu_delay,
            "context_old_menu": self._handle_context_menu,
            "context_open_with_notepad": self._handle_notepad_context,
            "context_pwsh_admin_here": self._make_shell_add_handler(
                root_keys=[r"Directory\Background\shell\PowerShellAdmin"]
            ),
            "context_cmd_admin_here": self._make_shell_add_handler(
                root_keys=[r"Directory\Background\shell\CmdAdmin"]
            ),
            "context_take_ownership": self._make_shell_add_handler(
                root_keys=[r"*\shell\TakeOwnership", r"Directory\shell\TakeOwnership"]
            ),
            "taskbar_transparency_level": self._handle_transparency_level,
            "taskbar_position": self._handle_taskbar_position,
            "taskbar_autohide": self._handle_taskbar_autohide,
            "context_copy_as_path": self._handle_copy_as_path,
            "context_no_share": self._make_blocked_ext_handler(),
            "context_no_cast": self._make_blocked_ext_handler(),
        }
    
    def get_tweak(self, tweak_id: str) -> Optional[Tweak]:
        """Get a tweak by its ID."""
        return self.tweaks.get(tweak_id)
    
    def get_tweak_value(self, tweak_id: str) -> Any:
        """
        Get the current value of a tweak from the registry.
        Returns the option's default if the value can't be read.
        """
        tweak = self.get_tweak(tweak_id)
        if not tweak:
            return None
        
        # Use special handler if available
        if tweak_id in self._special_handlers:
            return self._special_handlers[tweak_id](tweak, read=True)
        
        # For most tweaks, check the first registry change
        if not tweak.registry_changes:
            return tweak.option.default
        
        change = tweak.registry_changes[0]
        current_value = read_registry_value(
            change.hive,
            change.key_path,
            change.value_name,
            default=None
        )
        
        if current_value is None:
            return tweak.option.default
        
        # For checkbox tweaks
        if tweak.option.type == "checkbox":
            return current_value == change.enabled_value

        # Spinbox values stored as REG_SZ need int conversion for the UI
        if tweak.option.type == "spinbox" and change.value_type == winreg.REG_SZ:
            try:
                return int(current_value)
            except (ValueError, TypeError):
                return tweak.option.default

        return current_value
    
    def apply_tweak(self, tweak_id: str, value: Any) -> bool:
        """
        Apply a tweak with the given value.
        Returns True if successful.
        """
        tweak = self.get_tweak(tweak_id)
        if not tweak:
            return False
        
        # Use special handler if available
        if tweak_id in self._special_handlers:
            return self._special_handlers[tweak_id](tweak, value=value, read=False)
        
        success = True
        for change in tweak.registry_changes:
            if tweak.option.type == "checkbox":
                reg_value = change.enabled_value if value else change.disabled_value
            else:
                reg_value = value

            # Spinbox values destined for REG_SZ keys need string conversion
            if (
                tweak.option.type == "spinbox"
                and change.value_type == winreg.REG_SZ
                and not isinstance(reg_value, str)
            ):
                reg_value = str(reg_value)

            if not write_registry_value(
                change.hive,
                change.key_path,
                change.value_name,
                reg_value,
                change.value_type
            ):
                success = False

        return success
    
    def _handle_transparency_level(self, _tweak: Tweak, value: Any = None, read: bool = False):
        """Handle taskbar transparency using Win32 SetLayeredWindowAttributes."""
        import ctypes

        _PERSIST_KEY = r"Software\WinTweaks"
        _PERSIST_VALUE = "TaskbarOpacity"

        if read:
            stored = read_registry_value(
                winreg.HKEY_CURRENT_USER, _PERSIST_KEY, _PERSIST_VALUE, default=100
            )
            try:
                return int(stored)
            except (ValueError, TypeError):
                return 100

        pct = max(0, min(100, int(value)))
        alpha = int(pct * 255 / 100)

        user32 = ctypes.windll.user32
        GWL_EXSTYLE = -20
        WS_EX_LAYERED = 0x00080000
        LWA_ALPHA = 0x2

        tray_classes = ("Shell_TrayWnd", "Shell_SecondaryTrayWnd")
        ok = False
        for cls in tray_classes:
            hwnd = user32.FindWindowW(cls, None)
            if not hwnd:
                continue
            style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED)
            if user32.SetLayeredWindowAttributes(hwnd, 0, alpha, LWA_ALPHA):
                ok = True

        if ok:
            write_registry_value(
                winreg.HKEY_CURRENT_USER, _PERSIST_KEY, _PERSIST_VALUE,
                pct, winreg.REG_DWORD
            )
        return ok

    def _handle_taskbar_position(self, tweak: Tweak, value: Any = None, read: bool = False):
        """Handle taskbar position via StuckRects3 Settings binary."""
        change = tweak.registry_changes[0]
        mapping = {"bottom": 3, "top": 1, "left": 0, "right": 2}
        reverse_map = {v: k for k, v in mapping.items()}
        if read:
            current_bytes = read_registry_value(
                change.hive, change.key_path, change.value_name, default=None
            )
            if current_bytes and len(current_bytes) >= 13:
                edge_val = current_bytes[12]
                return reverse_map.get(edge_val, "bottom")
            return "bottom"
        else:
            edge_val = mapping.get(value, 3)
            current_bytes = read_registry_value(
                change.hive, change.key_path, change.value_name, default=None
            )
            if current_bytes is None:
                # Create default StuckRects3 Settings (28 bytes)
                current_bytes = bytes([
                    0x28, 0x00, 0x00, 0x00,  # Size (DWORD, typically 40)
                    0x01, 0x00, 0x00, 0x00,  # Unknown/reserved
                    0x03, 0x00, 0x00, 0x00,  # Primary monitor edge (bottom)
                    0x00, 0x00, 0x00, 0x00,  # Monitor work rect left
                    0x00, 0x00, 0x00, 0x00,  # top
                    0x00, 0x00, 0x00, 0x00,  # right (will be set later)
                    0x00, 0x00, 0x00, 0x00,  # bottom
                    0x01, 0x00, 0x00, 0x00,  # Flags (always 1)
                ])
            if len(current_bytes) < 28:
                current_bytes = current_bytes.ljust(28, b'\x00')
            new_bytes = bytearray(current_bytes)
            new_bytes[12] = edge_val
            return write_registry_value(
                change.hive, change.key_path, change.value_name,
                bytes(new_bytes), change.value_type
            )

    def _handle_search_box(self, tweak: Tweak, value: Any = None, read: bool = False):
        """Handle search box mode tweak."""
        change = tweak.registry_changes[0]
        
        if read:
            current = read_registry_value(
                change.hive, change.key_path, change.value_name, default=1
            )
            mapping = {0: "hidden", 1: "icon", 2: "box"}
            return mapping.get(current, "icon")
        else:
            mapping = {"hidden": 0, "icon": 1, "box": 2}
            reg_value = mapping.get(value, 1)
            return write_registry_value(
                change.hive, change.key_path, change.value_name,
                reg_value, change.value_type
            )
    
    def _handle_launch_to(self, tweak: Tweak, value: Any = None, read: bool = False):
        """Handle File Explorer launch location tweak."""
        change = tweak.registry_changes[0]
        
        if read:
            current = read_registry_value(
                change.hive, change.key_path, change.value_name, default=2
            )
            mapping = {1: "this_pc", 2: "quick_access", 3: "downloads", 4: "documents"}
            return mapping.get(current, "quick_access")
        else:
            mapping = {"this_pc": 1, "quick_access": 2, "downloads": 3, "documents": 4}
            reg_value = mapping.get(value, 2)
            return write_registry_value(
                change.hive, change.key_path, change.value_name,
                reg_value, change.value_type
            )
    
    def _handle_menu_delay(self, tweak: Tweak, value: Any = None, read: bool = False):
        """Handle menu delay tweak."""
        change = tweak.registry_changes[0]
        
        if read:
            current = read_registry_value(
                change.hive, change.key_path, change.value_name, default="400"
            )
            try:
                return int(current)
            except (ValueError, TypeError):
                return 400
        else:
            return write_registry_value(
                change.hive, change.key_path, change.value_name,
                str(value), change.value_type
            )
    
    def _handle_context_menu(self, tweak: Tweak, value: Any = None, read: bool = False):
        """Handle classic context menu tweak (requires special key handling)."""
        change = tweak.registry_changes[0]
        
        if read:
            # Check if the key exists (enabled means classic menu)
            exists = read_registry_value(
                change.hive, change.key_path, change.value_name, default=None
            )
            return exists is not None
        else:
            if value:
                # Enable classic menu - create the key
                return write_registry_value(
                    change.hive, change.key_path, change.value_name,
                    "", change.value_type
                )
            else:
                # Disable classic menu - delete the key
                # We need to delete the entire key, not just the value
                try:
                    import winreg
                    # Delete the InprocServer32 key
                    winreg.DeleteKey(change.hive, change.key_path)
                    # Try to delete the parent CLSID key
                    parent_key = r"Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}"
                    try:
                        winreg.DeleteKey(change.hive, parent_key)
                    except:
                        pass
                    return True
                except Exception as e:
                    print(f"Error deleting context menu key: {e}")
                    return False
    
    def _handle_notepad_context(self, tweak: Tweak, value: Any = None, read: bool = False):
        """Handle 'Open with Notepad' context menu tweak."""
        if read:
            # Check if the key exists
            change = tweak.registry_changes[0]
            exists = read_registry_value(
                change.hive, change.key_path, change.value_name, default=None
            )
            return exists is not None
        else:
            if value:
                # Add the context menu entries
                success = True
                for change in tweak.registry_changes:
                    if not write_registry_value(
                        change.hive, change.key_path, change.value_name,
                        change.enabled_value, change.value_type
                    ):
                        success = False
                return success
            else:
                # Remove the context menu entries
                try:
                    # Delete command key first (child)
                    winreg.DeleteKey(
                        winreg.HKEY_CLASSES_ROOT,
                        r"*\shell\Open with Notepad\command"
                    )
                    # Delete parent key
                    winreg.DeleteKey(
                        winreg.HKEY_CLASSES_ROOT,
                        r"*\shell\Open with Notepad"
                    )
                    return True
                except Exception as e:
                    print(f"Error removing notepad context menu: {e}")
                    return False

    def _make_shell_add_handler(self, root_keys):
        """
        Build a handler for context menu 'add this entry' tweaks.

        Each root_key has a child '\\command' subkey. Enabling writes every
        registry_change; disabling deletes both \\command and the root key
        for each entry.
        """
        def handler(tweak: Tweak, value: Any = None, read: bool = False):
            if read:
                change = tweak.registry_changes[0]
                exists = read_registry_value(
                    change.hive, change.key_path, change.value_name, default=None
                )
                return exists is not None
            if value:
                success = True
                for change in tweak.registry_changes:
                    if not write_registry_value(
                        change.hive, change.key_path, change.value_name,
                        change.enabled_value, change.value_type
                    ):
                        success = False
                return success
            # Disable: tear down each shell key and its \command subkey
            success = True
            for root in root_keys:
                for subpath in (root + r"\command", root):
                    try:
                        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, subpath)
                    except FileNotFoundError:
                        pass
                    except OSError as e:
                        print(f"Error removing {subpath}: {e}")
                        success = False
            return success
        return handler

    def _handle_taskbar_autohide(self, tweak: Tweak, value: Any = None, read: bool = False):
        """Toggle taskbar auto-hide by setting/clearing bit 0x01 in StuckRects3 Settings byte 8."""
        change = tweak.registry_changes[0]
        current_bytes = read_registry_value(
            change.hive, change.key_path, change.value_name, default=None
        )
        if current_bytes is None:
            current_bytes = bytes([
                0x28, 0x00, 0x00, 0x00,
                0x01, 0x00, 0x00, 0x00,
                0x02, 0x00, 0x00, 0x00,
                0x03, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x01, 0x00, 0x00, 0x00,
            ])
        if len(current_bytes) < 28:
            current_bytes = current_bytes.ljust(28, b'\x00')
        if read:
            return bool(current_bytes[8] & 0x01)
        new_bytes = bytearray(current_bytes)
        if value:
            new_bytes[8] = new_bytes[8] | 0x01
        else:
            new_bytes[8] = new_bytes[8] & 0xFE
        return write_registry_value(
            change.hive, change.key_path, change.value_name,
            bytes(new_bytes), change.value_type
        )

    def _handle_copy_as_path(self, tweak: Tweak, value: Any = None, read: bool = False):
        """Add/remove 'Copy as Path' by creating or deleting the shell extension key."""
        change = tweak.registry_changes[0]
        if read:
            exists = read_registry_value(
                change.hive, change.key_path, change.value_name, default=None
            )
            return exists is not None
        if value:
            return write_registry_value(
                change.hive, change.key_path, change.value_name,
                change.enabled_value, change.value_type
            )
        try:
            winreg.DeleteKey(change.hive, change.key_path)
            return True
        except FileNotFoundError:
            return True
        except Exception as e:
            print(f"Error removing CopyAsPath context menu: {e}")
            return False

    def _make_blocked_ext_handler(self):
        """
        Build a handler for Shell Extensions Blocked entries.
        Enabling writes an empty REG_SZ value; disabling deletes that named value.
        """
        def handler(tweak: Tweak, value: Any = None, read: bool = False):
            change = tweak.registry_changes[0]
            if read:
                exists = read_registry_value(
                    change.hive, change.key_path, change.value_name, default=None
                )
                return exists is not None
            if value:
                return write_registry_value(
                    change.hive, change.key_path, change.value_name,
                    "", change.value_type
                )
            try:
                key = winreg.OpenKey(change.hive, change.key_path, 0, winreg.KEY_SET_VALUE)
                winreg.DeleteValue(key, change.value_name)
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                return True
            except Exception as e:
                print(f"Error removing blocked extension {change.value_name}: {e}")
                return False
        return handler
