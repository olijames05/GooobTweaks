"""
Registry utility functions for Windows tweaks.
Handles reading and writing Windows registry values safely.
"""

import winreg
import ctypes
from typing import Optional, Union, Any


def is_admin() -> bool:
    """Check if the current process has administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def read_registry_value(
    hive: int,
    key_path: str,
    value_name: str,
    default: Any = None
) -> Any:
    """
    Read a value from the Windows registry.
    
    Args:
        hive: Registry hive (e.g., winreg.HKEY_CURRENT_USER)
        key_path: Path to the registry key
        value_name: Name of the value to read
        default: Default value to return if key/value doesn't exist
        
    Returns:
        The registry value or default if not found
    """
    try:
        with winreg.OpenKey(hive, key_path, 0, winreg.KEY_READ) as key:
            value, _ = winreg.QueryValueEx(key, value_name)
            return value
    except (FileNotFoundError, OSError):
        return default


def write_registry_value(
    hive: int,
    key_path: str,
    value_name: str,
    value: Any,
    value_type: int = winreg.REG_DWORD
) -> bool:
    """
    Write a value to the Windows registry.
    
    Args:
        hive: Registry hive (e.g., winreg.HKEY_CURRENT_USER)
        key_path: Path to the registry key
        value_name: Name of the value to write
        value: Value to write
        value_type: Registry value type (e.g., winreg.REG_DWORD, winreg.REG_SZ)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create the key if it doesn't exist
        with winreg.CreateKey(hive, key_path) as key:
            winreg.SetValueEx(key, value_name, 0, value_type, value)
        return True
    except (OSError, PermissionError) as e:
        print(f"Error writing registry value: {e}")
        return False


def delete_registry_value(
    hive: int,
    key_path: str,
    value_name: str
) -> bool:
    """
    Delete a value from the Windows registry.
    
    Args:
        hive: Registry hive
        key_path: Path to the registry key
        value_name: Name of the value to delete
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with winreg.OpenKey(hive, key_path, 0, winreg.KEY_WRITE) as key:
            winreg.DeleteValue(key, value_name)
        return True
    except (FileNotFoundError, OSError) as e:
        print(f"Error deleting registry value: {e}")
        return False


def registry_value_exists(
    hive: int,
    key_path: str,
    value_name: str
) -> bool:
    """
    Check if a registry value exists.
    
    Args:
        hive: Registry hive
        key_path: Path to the registry key
        value_name: Name of the value to check
        
    Returns:
        True if the value exists, False otherwise
    """
    try:
        with winreg.OpenKey(hive, key_path, 0, winreg.KEY_READ) as key:
            winreg.QueryValueEx(key, value_name)
            return True
    except (FileNotFoundError, OSError):
        return False
