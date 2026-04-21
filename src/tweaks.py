"""
Windows tweaks collection.
Each tweak is a dictionary with metadata and registry operations.
"""

import winreg
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class TweakCategory(Enum):
    TASKBAR = "Taskbar"
    EXPLORER = "Explorer"
    SYSTEM = "System"
    PRIVACY = "Privacy"
    PERFORMANCE = "Performance"
    CONTEXT_MENU = "Context Menu"
    PERSONALIZATION = "Personalization"
    ACCESSIBILITY = "Accessibility"


@dataclass
class TweakOption:
    """Represents a single option for a tweak."""
    name: str
    label: str
    type: str  # 'checkbox', 'dropdown', 'spinbox'
    default: Any
    description: str = ""
    choices: List[tuple] = field(default_factory=list)  # For dropdown: [(value, label), ...]
    min_value: Optional[int] = None  # For spinbox
    max_value: Optional[int] = None  # For spinbox


@dataclass
class RegistryChange:
    """Represents a single registry change."""
    hive: int
    key_path: str
    value_name: str
    value_type: int
    enabled_value: Any
    disabled_value: Any


@dataclass
class Tweak:
    """Represents a Windows tweak."""
    id: str
    name: str
    category: TweakCategory
    description: str
    option: TweakOption
    registry_changes: List[RegistryChange]
    requires_restart: bool = False
    requires_logoff: bool = False


# =============================================================================
# TASKBAR TWEAKS
# =============================================================================

TASKBAR_TWEAKS = [
    Tweak(
        id="taskbar_small_icons",
        name="Small Taskbar Icons",
        category=TweakCategory.TASKBAR,
        description="Use smaller icons on the taskbar",
        option=TweakOption(
            name="enabled",
            label="Enable small taskbar icons",
            type="checkbox",
            default=False,
            description="Reduces the size of taskbar icons and buttons"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="TaskbarSmallIcons",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ],
        requires_restart=False
    ),
    Tweak(
        id="taskbar_combine_never",
        name="Never Combine Taskbar Buttons",
        category=TweakCategory.TASKBAR,
        description="Show labels on taskbar buttons and never combine them",
        option=TweakOption(
            name="enabled",
            label="Never combine taskbar buttons",
            type="checkbox",
            default=False,
            description="Shows window titles and prevents button combining"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="TaskbarGlomLevel",
                value_type=winreg.REG_DWORD,
                enabled_value=2,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="taskbar_transparency",
        name="Taskbar Transparency",
        category=TweakCategory.TASKBAR,
        description="Enable or disable taskbar transparency effects",
        option=TweakOption(
            name="enabled",
            label="Enable taskbar transparency",
            type="checkbox",
            default=True,
            description="Makes the taskbar semi-transparent"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
                value_name="EnableTransparency",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="taskbar_search_box",
        name="Search Box on Taskbar",
        category=TweakCategory.TASKBAR,
        description="Configure the search box on the taskbar",
        option=TweakOption(
            name="mode",
            label="Search box mode",
            type="dropdown",
            default="icon",
            description="Choose how search appears on the taskbar",
            choices=[
                ("hidden", "Hidden"),
                ("icon", "Show icon only"),
                ("box", "Show search box")
            ]
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Search",
                value_name="SearchboxTaskbarMode",
                value_type=winreg.REG_DWORD,
                enabled_value=None,  # Handled specially
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="taskbar_cortana",
        name="Hide Cortana Button",
        category=TweakCategory.TASKBAR,
        description="Hide the Cortana button from the taskbar",
        option=TweakOption(
            name="enabled",
            label="Hide Cortana button",
            type="checkbox",
            default=False,
            description="Removes the Cortana button from the taskbar"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="ShowCortanaButton",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="taskbar_task_view",
        name="Hide Task View Button",
        category=TweakCategory.TASKBAR,
        description="Hide the Task View button from the taskbar",
        option=TweakOption(
            name="enabled",
            label="Hide Task View button",
            type="checkbox",
            default=False,
            description="Removes the Task View button from the taskbar"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="ShowTaskViewButton",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="taskbar_widgets",
        name="Hide Widgets Button",
        category=TweakCategory.TASKBAR,
        description="Hide the Widgets button from the taskbar (Windows 11)",
        option=TweakOption(
            name="enabled",
            label="Hide Widgets button",
            type="checkbox",
            default=False,
            description="Removes the Widgets button from the taskbar"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="TaskbarDa",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="taskbar_chat",
        name="Hide Chat Button",
        category=TweakCategory.TASKBAR,
        description="Hide the Chat (Teams) button from the taskbar (Windows 11)",
        option=TweakOption(
            name="enabled",
            label="Hide Chat button",
            type="checkbox",
            default=False,
            description="Removes the Chat button from the taskbar"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="TaskbarMn",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="taskbar_align_left",
        name="Left-Align Taskbar",
        category=TweakCategory.TASKBAR,
        description="Align taskbar icons to the left (Windows 11)",
        option=TweakOption(
            name="enabled",
            label="Align taskbar to the left",
            type="checkbox",
            default=False,
            description="Moves taskbar icons to the left side"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="TaskbarAl",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="taskbar_last_active",
        name="Click on Last Active Window",
        category=TweakCategory.TASKBAR,
        description="Clicking a taskbar button switches to the last active window",
        option=TweakOption(
            name="enabled",
            label="Switch to last active window",
            type="checkbox",
            default=False,
            description="When clicking grouped taskbar buttons, switch to the most recently used window"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="LastActiveClick",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="taskbar_no_grouping",
        name="Disable Taskbar Grouping",
        category=TweakCategory.TASKBAR,
        description="Show each window separately without grouping",
        option=TweakOption(
            name="enabled",
            label="Disable grouping",
            type="checkbox",
            default=False,
            description="Each window gets its own taskbar button"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="NoTaskGrouping",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="taskbar_seconds",
        name="Show Seconds in Clock",
        category=TweakCategory.TASKBAR,
        description="Display seconds in the taskbar clock (Windows 11)",
        option=TweakOption(
            name="enabled",
            label="Show seconds",
            type="checkbox",
            default=False,
            description="Adds seconds to the system tray clock"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="ShowSecondsInSystemClock",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
]

# =============================================================================
# EXPLORER TWEAKS
# =============================================================================

EXPLORER_TWEAKS = [
    Tweak(
        id="explorer_show_file_extensions",
        name="Show File Extensions",
        category=TweakCategory.EXPLORER,
        description="Always show file extensions in File Explorer",
        option=TweakOption(
            name="enabled",
            label="Show file extensions",
            type="checkbox",
            default=False,
            description="Displays file extensions like .txt, .exe, .jpg"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="HideFileExt",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="explorer_show_hidden_files",
        name="Show Hidden Files",
        category=TweakCategory.EXPLORER,
        description="Show hidden files and folders in File Explorer",
        option=TweakOption(
            name="enabled",
            label="Show hidden files",
            type="checkbox",
            default=False,
            description="Displays hidden files and folders"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="Hidden",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=2
            )
        ]
    ),
    Tweak(
        id="explorer_show_super_hidden",
        name="Show Protected System Files",
        category=TweakCategory.EXPLORER,
        description="Show protected operating system files",
        option=TweakOption(
            name="enabled",
            label="Show protected system files",
            type="checkbox",
            default=False,
            description="Displays system files (not recommended for most users)"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="ShowSuperHidden",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="explorer_compact_view",
        name="Compact Mode in File Explorer",
        category=TweakCategory.EXPLORER,
        description="Use compact spacing in File Explorer (Windows 11)",
        option=TweakOption(
            name="enabled",
            label="Use compact mode",
            type="checkbox",
            default=False,
            description="Reduces spacing between files and folders"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="UseCompactMode",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="explorer_launch_to",
        name="Launch File Explorer To",
        category=TweakCategory.EXPLORER,
        description="Choose where File Explorer opens by default",
        option=TweakOption(
            name="location",
            label="Open File Explorer to",
            type="dropdown",
            default="quick_access",
            description="Select the default location when opening File Explorer",
            choices=[
                ("quick_access", "Quick Access"),
                ("this_pc", "This PC"),
                ("downloads", "Downloads"),
                ("documents", "Documents")
            ]
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="LaunchTo",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="explorer_full_path_title",
        name="Show Full Path in Title Bar",
        category=TweakCategory.EXPLORER,
        description="Display the full folder path in File Explorer's title bar",
        option=TweakOption(
            name="enabled",
            label="Show full path in title bar",
            type="checkbox",
            default=False,
            description="Shows the complete path instead of just the folder name"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\CabinetState",
                value_name="FullPath",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="explorer_disable_thumbnails",
        name="Disable Thumbnail Previews",
        category=TweakCategory.EXPLORER,
        description="Disable thumbnail previews for files and folders",
        option=TweakOption(
            name="enabled",
            label="Disable thumbnails",
            type="checkbox",
            default=False,
            description="Shows icons instead of thumbnail previews"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="IconsOnly",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="explorer_details_pane",
        name="Disable Details Pane",
        category=TweakCategory.EXPLORER,
        description="Hide the details pane in File Explorer",
        option=TweakOption(
            name="enabled",
            label="Hide details pane",
            type="checkbox",
            default=False,
            description="Removes the file details pane at the bottom"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="ShowInfoTip",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="explorer_preview_pane",
        name="Disable Preview Pane",
        category=TweakCategory.EXPLORER,
        description="Disable the preview pane in File Explorer",
        option=TweakOption(
            name="enabled",
            label="Disable preview pane",
            type="checkbox",
            default=False,
            description="Prevents showing file previews"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="ShowPreviewPane",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="explorer_checkboxes",
        name="Enable Item Checkboxes",
        category=TweakCategory.EXPLORER,
        description="Show checkboxes next to files and folders for selection",
        option=TweakOption(
            name="enabled",
            label="Show checkboxes",
            type="checkbox",
            default=False,
            description="Adds checkboxes for easier multi-select"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="AutoCheckSelect",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="explorer_ribbon",
        name="Always Show Ribbon",
        category=TweakCategory.EXPLORER,
        description="Keep the ribbon expanded in File Explorer",
        option=TweakOption(
            name="enabled",
            label="Always show ribbon",
            type="checkbox",
            default=False,
            description="Prevents the ribbon from collapsing"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Ribbon",
                value_name="MinimizedStateTabletModeOff",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="explorer_quick_access",
        name="Remove Quick Access",
        category=TweakCategory.EXPLORER,
        description="Remove Quick Access from File Explorer navigation pane",
        option=TweakOption(
            name="enabled",
            label="Remove Quick Access",
            type="checkbox",
            default=False,
            description="Hides Quick Access from the navigation pane"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer",
                value_name="HubMode",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
]

# =============================================================================
# SYSTEM TWEAKS
# =============================================================================

SYSTEM_TWEAKS = [
    Tweak(
        id="system_dark_mode",
        name="Dark Mode",
        category=TweakCategory.SYSTEM,
        description="Enable system-wide dark mode",
        option=TweakOption(
            name="enabled",
            label="Enable dark mode",
            type="checkbox",
            default=False,
            description="Applies dark theme to Windows and apps"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
                value_name="AppsUseLightTheme",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            ),
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
                value_name="SystemUsesLightTheme",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="system_accent_color",
        name="Accent Color on Title Bars",
        category=TweakCategory.SYSTEM,
        description="Show accent color on window title bars",
        option=TweakOption(
            name="enabled",
            label="Show accent color on title bars",
            type="checkbox",
            default=False,
            description="Applies your accent color to window title bars"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
                value_name="ColorPrevalence",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="system_snap_assist",
        name="Disable Snap Assist",
        category=TweakCategory.SYSTEM,
        description="Disable the Snap Assist feature when snapping windows",
        option=TweakOption(
            name="enabled",
            label="Disable Snap Assist",
            type="checkbox",
            default=False,
            description="Prevents showing other windows when snapping"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="SnapAssist",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="system_shake_minimize",
        name="Disable Shake to Minimize",
        category=TweakCategory.SYSTEM,
        description="Disable the 'Aero Shake' feature that minimizes other windows",
        option=TweakOption(
            name="enabled",
            label="Disable shake to minimize",
            type="checkbox",
            default=False,
            description="Prevents minimizing other windows when shaking a window"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="DisallowShaking",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="system_edge_swipe",
        name="Disable Edge Swipes",
        category=TweakCategory.SYSTEM,
        description="Disable touchpad edge swipes (for tablets/touchscreens)",
        option=TweakOption(
            name="enabled",
            label="Disable edge swipes",
            type="checkbox",
            default=False,
            description="Prevents edge swipe gestures"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows\EdgeUI",
                value_name="AllowEdgeSwipe",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="system_sticky_keys",
        name="Disable Sticky Keys Prompt",
        category=TweakCategory.SYSTEM,
        description="Disable the Sticky Keys popup when pressing Shift 5 times",
        option=TweakOption(
            name="enabled",
            label="Disable Sticky Keys prompt",
            type="checkbox",
            default=False,
            description="Prevents the Sticky Keys dialog from appearing"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Accessibility\StickyKeys",
                value_name="Flags",
                value_type=winreg.REG_SZ,
                enabled_value="506",
                disabled_value="510"
            )
        ]
    ),
    Tweak(
        id="system_filter_keys",
        name="Disable Filter Keys Prompt",
        category=TweakCategory.SYSTEM,
        description="Disable the Filter Keys popup when holding Shift for 8 seconds",
        option=TweakOption(
            name="enabled",
            label="Disable Filter Keys prompt",
            type="checkbox",
            default=False,
            description="Prevents the Filter Keys dialog from appearing"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Accessibility\Keyboard Response",
                value_name="Flags",
                value_type=winreg.REG_SZ,
                enabled_value="122",
                disabled_value="126"
            )
        ]
    ),
    Tweak(
        id="system_caps_lock",
        name="Disable Caps Lock Key",
        category=TweakCategory.SYSTEM,
        description="Completely disable the Caps Lock key",
        option=TweakOption(
            name="enabled",
            label="Disable Caps Lock",
            type="checkbox",
            default=False,
            description="Caps Lock key will do nothing when pressed"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Keyboard Layout",
                value_name="Scancode Map",
                value_type=winreg.REG_BINARY,
                enabled_value=b"\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x3a\x00\x00\x00\x00\x00",
                disabled_value=None
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="system_numlock_startup",
        name="Enable Num Lock on Startup",
        category=TweakCategory.SYSTEM,
        description="Automatically turn on Num Lock when Windows starts",
        option=TweakOption(
            name="enabled",
            label="Enable Num Lock on startup",
            type="checkbox",
            default=False,
            description="Num Lock will be on at login"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Keyboard",
                value_name="InitialKeyboardIndicators",
                value_type=winreg.REG_SZ,
                enabled_value="2",
                disabled_value="0"
            )
        ]
    ),
    Tweak(
        id="system_auto_restart",
        name="Disable Auto Restart on BSOD",
        category=TweakCategory.SYSTEM,
        description="Prevent Windows from automatically restarting after a crash",
        option=TweakOption(
            name="enabled",
            label="Disable auto restart",
            type="checkbox",
            default=False,
            description="Stays on the blue screen so you can read the error"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\CrashControl",
                value_name="AutoReboot",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="system_error_reporting",
        name="Disable Error Reporting",
        category=TweakCategory.SYSTEM,
        description="Disable Windows Error Reporting",
        option=TweakOption(
            name="enabled",
            label="Disable error reporting",
            type="checkbox",
            default=False,
            description="Stops sending error reports to Microsoft"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\Windows Error Reporting",
                value_name="Disabled",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
]

# =============================================================================
# PRIVACY TWEAKS
# =============================================================================

PRIVACY_TWEAKS = [
    Tweak(
        id="privacy_telemetry",
        name="Disable Telemetry",
        category=TweakCategory.PRIVACY,
        description="Disable Windows telemetry and data collection",
        option=TweakOption(
            name="enabled",
            label="Disable telemetry",
            type="checkbox",
            default=False,
            description="Reduces data sent to Microsoft"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows\DataCollection",
                value_name="AllowTelemetry",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="privacy_advertising",
        name="Disable Advertising ID",
        category=TweakCategory.PRIVACY,
        description="Disable the advertising ID for personalized ads",
        option=TweakOption(
            name="enabled",
            label="Disable advertising ID",
            type="checkbox",
            default=False,
            description="Prevents apps from using your advertising ID"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo",
                value_name="Enabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="privacy_cortana",
        name="Disable Cortana",
        category=TweakCategory.PRIVACY,
        description="Completely disable Cortana",
        option=TweakOption(
            name="enabled",
            label="Disable Cortana",
            type="checkbox",
            default=False,
            description="Turns off Cortana completely"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows\Windows Search",
                value_name="AllowCortana",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="privacy_recent_files",
        name="Disable Recent Files in Quick Access",
        category=TweakCategory.PRIVACY,
        description="Stop showing recent files in Quick Access",
        option=TweakOption(
            name="enabled",
            label="Hide recent files",
            type="checkbox",
            default=False,
            description="Removes recent files from Quick Access"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer",
                value_name="ShowRecent",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="privacy_frequent_folders",
        name="Disable Frequent Folders in Quick Access",
        category=TweakCategory.PRIVACY,
        description="Stop showing frequent folders in Quick Access",
        option=TweakOption(
            name="enabled",
            label="Hide frequent folders",
            type="checkbox",
            default=False,
            description="Removes frequent folders from Quick Access"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer",
                value_name="ShowFrequent",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="privacy_feedback",
        name="Disable Feedback Notifications",
        category=TweakCategory.PRIVACY,
        description="Disable Windows feedback notifications",
        option=TweakOption(
            name="enabled",
            label="Disable feedback notifications",
            type="checkbox",
            default=False,
            description="Stops Windows from asking for feedback"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Siuf\Rules",
                value_name="NumberOfSIUFInPeriod",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
]

# =============================================================================
# PERFORMANCE TWEAKS
# =============================================================================

PERFORMANCE_TWEAKS = [
    Tweak(
        id="perf_visual_effects",
        name="Adjust for Best Performance",
        category=TweakCategory.PERFORMANCE,
        description="Disable visual effects for better performance",
        option=TweakOption(
            name="enabled",
            label="Optimize for best performance",
            type="checkbox",
            default=False,
            description="Disables animations and visual effects"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects",
                value_name="VisualFXSetting",
                value_type=winreg.REG_DWORD,
                enabled_value=2,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="perf_menu_delay",
        name="Reduce Menu Delay",
        category=TweakCategory.PERFORMANCE,
        description="Reduce the delay before menus appear",
        option=TweakOption(
            name="delay",
            label="Menu delay (ms)",
            type="spinbox",
            default=400,
            description="Lower values make menus appear faster",
            min_value=0,
            max_value=1000
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Desktop",
                value_name="MenuShowDelay",
                value_type=winreg.REG_SZ,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="perf_thumbnail_cache",
        name="Disable Thumbnail Cache",
        category=TweakCategory.PERFORMANCE,
        description="Disable thumbnail cache to save disk space",
        option=TweakOption(
            name="enabled",
            label="Disable thumbnail cache",
            type="checkbox",
            default=False,
            description="Prevents Windows from caching thumbnails"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer",
                value_name="DisableThumbsDBOnNetworkFolders",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
]

# =============================================================================
# CONTEXT MENU TWEAKS
# =============================================================================

CONTEXT_MENU_TWEAKS = [
    Tweak(
        id="context_old_menu",
        name="Use Classic Context Menu",
        category=TweakCategory.CONTEXT_MENU,
        description="Use the classic Windows 10-style context menu (Windows 11)",
        option=TweakOption(
            name="enabled",
            label="Use classic context menu",
            type="checkbox",
            default=False,
            description="Replaces the new context menu with the classic one"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32",
                value_name="",
                value_type=winreg.REG_SZ,
                enabled_value="",
                disabled_value=None
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="context_open_with_notepad",
        name="Add 'Open with Notepad'",
        category=TweakCategory.CONTEXT_MENU,
        description="Add 'Open with Notepad' to the context menu for all files",
        option=TweakOption(
            name="enabled",
            label="Add 'Open with Notepad'",
            type="checkbox",
            default=False,
            description="Adds a quick option to open files with Notepad"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CLASSES_ROOT,
                key_path=r"*\shell\Open with Notepad",
                value_name="",
                value_type=winreg.REG_SZ,
                enabled_value="Open with Notepad",
                disabled_value=None
            ),
            RegistryChange(
                hive=winreg.HKEY_CLASSES_ROOT,
                key_path=r"*\shell\Open with Notepad\command",
                value_name="",
                value_type=winreg.REG_SZ,
                enabled_value="notepad.exe %1",
                disabled_value=None
            )
        ]
    ),
]

# =============================================================================
# PERSONALIZATION TWEAKS
# =============================================================================

PERSONALIZATION_TWEAKS = [
    Tweak(
        id="pers_disable_lockscreen",
        name="Disable Lock Screen",
        category=TweakCategory.PERSONALIZATION,
        description="Skip the lock screen and go straight to login",
        option=TweakOption(
            name="enabled",
            label="Disable lock screen",
            type="checkbox",
            default=False,
            description="Removes the lock screen wallpaper/time display"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows\Personalization",
                value_name="NoLockScreen",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="pers_disable_blur",
        name="Disable Login Screen Blur",
        category=TweakCategory.PERSONALIZATION,
        description="Disable the acrylic blur effect on the login screen",
        option=TweakOption(
            name="enabled",
            label="Disable login blur",
            type="checkbox",
            default=False,
            description="Shows a clear background on the login screen"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows\System",
                value_name="DisableAcrylicBackgroundOnLogon",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="pers_colorize_start",
        name="Colorize Start and Taskbar",
        category=TweakCategory.PERSONALIZATION,
        description="Show accent color on Start menu and taskbar",
        option=TweakOption(
            name="enabled",
            label="Colorize Start and Taskbar",
            type="checkbox",
            default=False,
            description="Applies accent color to Start menu and taskbar"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
                value_name="ColorPrevalence",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="pers_transparency",
        name="Disable Transparency Effects",
        category=TweakCategory.PERSONALIZATION,
        description="Turn off transparency effects throughout Windows",
        option=TweakOption(
            name="enabled",
            label="Disable transparency",
            type="checkbox",
            default=False,
            description="Removes transparency from taskbar, Start menu, etc."
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
                value_name="EnableTransparency",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="pers_disable_animations",
        name="Disable Window Animations",
        category=TweakCategory.PERSONALIZATION,
        description="Turn off window open/close/minimize animations",
        option=TweakOption(
            name="enabled",
            label="Disable animations",
            type="checkbox",
            default=False,
            description="Makes windows appear and disappear instantly"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Desktop\WindowMetrics",
                value_name="MinAnimate",
                value_type=winreg.REG_SZ,
                enabled_value="0",
                disabled_value="1"
            )
        ]
    ),
    Tweak(
        id="pers_disable_shadows",
        name="Disable Window Shadows",
        category=TweakCategory.PERSONALIZATION,
        description="Remove drop shadows from windows",
        option=TweakOption(
            name="enabled",
            label="Disable shadows",
            type="checkbox",
            default=False,
            description="Removes shadow effects from window borders"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="ListviewShadow",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="pers_rounded_corners",
        name="Disable Rounded Corners",
        category=TweakCategory.PERSONALIZATION,
        description="Use square corners instead of rounded (Windows 11)",
        option=TweakOption(
            name="enabled",
            label="Disable rounded corners",
            type="checkbox",
            default=False,
            description="Makes window corners square instead of rounded"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\DWM",
                value_name="RoundCorners",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="pers_boot_animation",
        name="Verbose Boot Messages",
        category=TweakCategory.PERSONALIZATION,
        description="Show detailed boot information instead of the Windows logo",
        option=TweakOption(
            name="enabled",
            label="Verbose boot",
            type="checkbox",
            default=False,
            description="Shows driver loading info during boot"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System",
                value_name="VerboseStatus",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="pers_boot_logo",
        name="Disable Boot Logo",
        category=TweakCategory.PERSONALIZATION,
        description="Disable the Windows logo during boot",
        option=TweakOption(
            name="enabled",
            label="Disable boot logo",
            type="checkbox",
            default=False,
            description="Shows a black screen instead of the Windows logo"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System",
                value_name="DisableBootLogo",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="pers_cursor_shadow",
        name="Disable Cursor Shadow",
        category=TweakCategory.PERSONALIZATION,
        description="Remove the shadow effect from the mouse cursor",
        option=TweakOption(
            name="enabled",
            label="Disable cursor shadow",
            type="checkbox",
            default=False,
            description="Removes shadow from mouse pointer"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Cursors",
                value_name="CursorShadow",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="pers_beep",
        name="Disable System Beep",
        category=TweakCategory.PERSONALIZATION,
        description="Turn off the system beep sound",
        option=TweakOption(
            name="enabled",
            label="Disable system beep",
            type="checkbox",
            default=False,
            description="Prevents the PC speaker from beeping"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Sound",
                value_name="Beep",
                value_type=winreg.REG_SZ,
                enabled_value="no",
                disabled_value="yes"
            )
        ]
    ),
    Tweak(
        id="pers_error_beeps",
        name="Disable Error Beeps",
        category=TweakCategory.PERSONALIZATION,
        description="Turn off error beep sounds",
        option=TweakOption(
            name="enabled",
            label="Disable error beeps",
            type="checkbox",
            default=False,
            description="Silences error notification sounds"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Sound",
                value_name="ExtendedSounds",
                value_type=winreg.REG_SZ,
                enabled_value="no",
                disabled_value="yes"
            )
        ]
    ),
]

# =============================================================================
# ACCESSIBILITY TWEAKS
# =============================================================================

ACCESSIBILITY_TWEAKS = [
    Tweak(
        id="acc_high_contrast",
        name="High Contrast Mode",
        category=TweakCategory.ACCESSIBILITY,
        description="Enable high contrast mode for better visibility",
        option=TweakOption(
            name="enabled",
            label="Enable high contrast",
            type="checkbox",
            default=False,
            description="Increases contrast between elements"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Themes",
                value_name="CurrentTheme",
                value_type=winreg.REG_SZ,
                enabled_value=r"%SystemRoot%\resources\Ease of Access Themes\hcblack.theme",
                disabled_value=r"%SystemRoot%\resources\Themes\aero.theme"
            )
        ],
        requires_logoff=True
    ),
    Tweak(
        id="acc_large_cursors",
        name="Large Mouse Cursors",
        category=TweakCategory.ACCESSIBILITY,
        description="Use larger mouse cursor for better visibility",
        option=TweakOption(
            name="enabled",
            label="Enable large cursors",
            type="checkbox",
            default=False,
            description="Increases cursor size"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Cursors",
                value_name="Scheme",
                value_type=winreg.REG_SZ,
                enabled_value="Windows Black (extra large)",
                disabled_value="Windows Default"
            )
        ]
    ),
    Tweak(
        id="acc_mouse_trails",
        name="Mouse Trails",
        category=TweakCategory.ACCESSIBILITY,
        description="Show trails behind the mouse cursor",
        option=TweakOption(
            name="enabled",
            label="Enable mouse trails",
            type="checkbox",
            default=False,
            description="Helps track cursor movement"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Mouse",
                value_name="MouseTrails",
                value_type=winreg.REG_SZ,
                enabled_value="7",
                disabled_value="0"
            )
        ]
    ),
    Tweak(
        id="acc_snap_to_default",
        name="Snap To Default Button",
        category=TweakCategory.ACCESSIBILITY,
        description="Automatically move cursor to default button in dialogs",
        option=TweakOption(
            name="enabled",
            label="Enable snap to default",
            type="checkbox",
            default=False,
            description="Moves cursor to OK/Yes buttons automatically"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Mouse",
                value_name="SnapToDefaultButton",
                value_type=winreg.REG_SZ,
                enabled_value="1",
                disabled_value="0"
            )
        ]
    ),
    Tweak(
        id="acc_toggle_keys",
        name="Toggle Keys Beep",
        category=TweakCategory.ACCESSIBILITY,
        description="Play a beep when Caps Lock, Num Lock, or Scroll Lock is pressed",
        option=TweakOption(
            name="enabled",
            label="Enable toggle keys beep",
            type="checkbox",
            default=False,
            description="Audible feedback for lock keys"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Accessibility\ToggleKeys",
                value_name="Flags",
                value_type=winreg.REG_SZ,
                enabled_value="63",
                disabled_value="58"
            )
        ]
    ),
    Tweak(
        id="acc_mouse_keys",
        name="Mouse Keys",
        category=TweakCategory.ACCESSIBILITY,
        description="Control mouse pointer with numeric keypad",
        option=TweakOption(
            name="enabled",
            label="Enable mouse keys",
            type="checkbox",
            default=False,
            description="Use Numpad to move mouse cursor"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Accessibility\MouseKeys",
                value_name="Flags",
                value_type=winreg.REG_SZ,
                enabled_value="63",
                disabled_value="0"
            )
        ]
    ),
    Tweak(
        id="acc_sound_sentry",
        name="Sound Sentry",
        category=TweakCategory.ACCESSIBILITY,
        description="Flash screen or window when system makes a sound",
        option=TweakOption(
            name="enabled",
            label="Enable sound sentry",
            type="checkbox",
            default=False,
            description="Visual notification for system sounds"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Accessibility\SoundSentry",
                value_name="Flags",
                value_type=winreg.REG_SZ,
                enabled_value="3",
                disabled_value="0"
            ),
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Accessibility\SoundSentry",
                value_name="WindowsEffect",
                value_type=winreg.REG_SZ,
                enabled_value="1",
                disabled_value="0"
            )
        ]
    ),
    Tweak(
        id="acc_show_sounds",
        name="Show Sounds",
        category=TweakCategory.ACCESSIBILITY,
        description="Show captions for speech and sounds",
        option=TweakOption(
            name="enabled",
            label="Enable show sounds",
            type="checkbox",
            default=False,
            description="Displays visual cues for sounds"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Accessibility\ShowSounds",
                value_name="On",
                value_type=winreg.REG_SZ,
                enabled_value="1",
                disabled_value="0"
            )
        ]
    ),
    Tweak(
        id="acc_caret_width",
        name="Thick Text Cursor",
        category=TweakCategory.ACCESSIBILITY,
        description="Make the text cursor (caret) thicker for better visibility",
        option=TweakOption(
            name="enabled",
            label="Enable thick cursor",
            type="checkbox",
            default=False,
            description="Increases text cursor width"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Desktop",
                value_name="CaretWidth",
                value_type=winreg.REG_DWORD,
                enabled_value=3,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="acc_cursor_blink",
        name="Disable Cursor Blink",
        category=TweakCategory.ACCESSIBILITY,
        description="Stop the text cursor from blinking",
        option=TweakOption(
            name="enabled",
            label="Disable cursor blink",
            type="checkbox",
            default=False,
            description="Makes text cursor solid instead of blinking"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Desktop",
                value_name="CursorBlinkRate",
                value_type=winreg.REG_SZ,
                enabled_value="-1",
                disabled_value="530"
            )
        ]
    ),
    Tweak(
        id="acc_scroll_lines",
        name="Reduce Scroll Lines",
        category=TweakCategory.ACCESSIBILITY,
        description="Scroll fewer lines at a time for better control",
        option=TweakOption(
            name="enabled",
            label="Reduce scroll speed",
            type="checkbox",
            default=False,
            description="Scrolls 1 line instead of 3"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Desktop",
                value_name="WheelScrollLines",
                value_type=winreg.REG_SZ,
                enabled_value="1",
                disabled_value="3"
            )
        ]
    ),
    Tweak(
        id="acc_icon_size",
        name="Large Desktop Icons",
        category=TweakCategory.ACCESSIBILITY,
        description="Use larger icons on the desktop",
        option=TweakOption(
            name="enabled",
            label="Enable large icons",
            type="checkbox",
            default=False,
            description="Increases desktop icon size"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="TaskbarSizeMove",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="acc_underline_shortcuts",
        name="Always Underline Shortcuts",
        category=TweakCategory.ACCESSIBILITY,
        description="Always show underlines for keyboard shortcuts",
        option=TweakOption(
            name="enabled",
            label="Always underline shortcuts",
            type="checkbox",
            default=False,
            description="Shows Alt key underlines all the time"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Accessibility\Keyboard Preference",
                value_name="On",
                value_type=winreg.REG_SZ,
                enabled_value="1",
                disabled_value="0"
            )
        ]
    ),
]

# =============================================================================
# ALL TWEAKS
# =============================================================================

ALL_TWEAKS = (
    TASKBAR_TWEAKS +
    EXPLORER_TWEAKS +
    SYSTEM_TWEAKS +
    PRIVACY_TWEAKS +
    PERFORMANCE_TWEAKS +
    CONTEXT_MENU_TWEAKS +
    PERSONALIZATION_TWEAKS +
    ACCESSIBILITY_TWEAKS
)

# Group tweaks by category
TWEAKS_BY_CATEGORY = {
    category: [t for t in ALL_TWEAKS if t.category == category]
    for category in TweakCategory
}
