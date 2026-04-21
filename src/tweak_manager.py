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
            
            if not write_registry_value(
                change.hive,
                change.key_path,
                change.value_name,
                reg_value,
                change.value_type
            ):
                success = False
        
        return success
    
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
                    import winreg
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
