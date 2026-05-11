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
    NETWORK = "Network"
    POWER = "Power & Battery"
    GAMING = "Gaming"
    PERFORMANCE = "Performance"
    SECURITY = "Security & Defender"
    PRIVACY = "Privacy"
    APPS_SERVICES = "Apps & Services"
    CONTEXT_MENU = "Context Menu"
    PERSONALIZATION = "Personalization"
    ACCESSIBILITY = "Accessibility"
    DISPLAY = "Display"
    MOUSE_INPUT = "Mouse & Input"
    STARTUP_BOOT = "Startup & Boot"
    NOTIFICATIONS = "Notifications"
    DEVELOPER = "Developer Tools"


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
    Tweak(
        id="taskbar_rounded_corners",
        name="Taskbar Rounded Corners",
        category=TweakCategory.TASKBAR,
        description="Enable or disable rounded corners on the taskbar",
        option=TweakOption(
            name="enabled",
            label="Enable rounded corners",
            type="checkbox",
            default=True,
            description="Controls whether taskbar corners are rounded or square"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\DWM",
                value_name="RoundCorners",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="taskbar_transparency_level",
        name="Taskbar Transparency Level",
        category=TweakCategory.TASKBAR,
        description="Control the transparency level of the taskbar",
        option=TweakOption(
            name="level",
            label="Transparency",
            type="spinbox",
            default=100,
            description="0 = completely transparent, 100 = fully opaque",
            min_value=0,
            max_value=100
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="TaskbarAcrylicOpacity",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="taskbar_position",
        name="Taskbar Position",
        category=TweakCategory.TASKBAR,
        description="Position the taskbar on any screen edge",
        option=TweakOption(
            name="position",
            label="Placement",
            type="dropdown",
            default="bottom",
            description="Choose which edge of the screen the taskbar appears on",
            choices=[
                ("bottom", "Bottom"),
                ("top", "Top"),
                ("left", "Left"),
                ("right", "Right")
            ]
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\StuckRects3",
                value_name="Settings",
                value_type=winreg.REG_BINARY,
                enabled_value=None,
                disabled_value=None
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="taskbar_autohide",
        name="Auto-Hide Taskbar",
        category=TweakCategory.TASKBAR,
        description="Automatically hide the taskbar when not in use",
        option=TweakOption(
            name="enabled",
            label="Auto-hide taskbar",
            type="checkbox",
            default=False,
            description="Taskbar slides off-screen until you move the mouse to the screen edge"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\StuckRects3",
                value_name="Settings",
                value_type=winreg.REG_BINARY,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="taskbar_show_all_tray_icons",
        name="Always Show All Notification Icons",
        category=TweakCategory.TASKBAR,
        description="Show every system tray icon without hiding inactive ones",
        option=TweakOption(
            name="enabled",
            label="Show all tray icons",
            type="checkbox",
            default=False,
            description="Disables the 'hide inactive icons' feature so all system tray icons are always visible"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer",
                value_name="EnableAutoTray",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="taskbar_end_task",
        name="Enable End Task from Taskbar",
        category=TweakCategory.TASKBAR,
        description="Add an End Task option to the right-click menu of taskbar buttons (Windows 11)",
        option=TweakOption(
            name="enabled",
            label="Enable End Task context menu",
            type="checkbox",
            default=False,
            description="Right-clicking a taskbar button shows 'End Task' to force-close without opening Task Manager"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\TaskbarDeveloperSettings",
                value_name="TaskbarEndTask",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="taskbar_hide_meet_now",
        name="Hide Meet Now (Skype) Button",
        category=TweakCategory.TASKBAR,
        description="Remove the Meet Now / Skype button from the system tray area",
        option=TweakOption(
            name="enabled",
            label="Hide Meet Now button",
            type="checkbox",
            default=False,
            description="Cleans up the system tray notification area for non-Skype users"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer",
                value_name="HideSCAMeetNow",
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
    Tweak(
        id="explorer_desktop_thispc",
        name="Show 'This PC' on Desktop",
        category=TweakCategory.EXPLORER,
        description="Show the 'This PC' icon on the desktop",
        option=TweakOption(
            name="enabled",
            label="Show This PC icon",
            type="checkbox",
            default=False,
            description="Adds the This PC icon to your desktop"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel",
                value_name="{20D04FE0-3AEA-1069-A2D8-08002B30309D}",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="explorer_desktop_userfolder",
        name="Show User Folder on Desktop",
        category=TweakCategory.EXPLORER,
        description="Show your user profile folder icon on the desktop",
        option=TweakOption(
            name="enabled",
            label="Show user folder icon",
            type="checkbox",
            default=False,
            description="Adds the user profile folder icon to your desktop"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel",
                value_name="{59031a47-3f72-44a7-89c5-5595fe6b30ee}",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="explorer_desktop_network",
        name="Show Network on Desktop",
        category=TweakCategory.EXPLORER,
        description="Show the Network icon on the desktop",
        option=TweakOption(
            name="enabled",
            label="Show Network icon",
            type="checkbox",
            default=False,
            description="Adds the Network icon to your desktop"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel",
                value_name="{F02C1A0D-BE21-4350-88B0-7367FC96EF3C}",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="explorer_desktop_recyclebin",
        name="Show Recycle Bin on Desktop",
        category=TweakCategory.EXPLORER,
        description="Show the Recycle Bin icon on the desktop",
        option=TweakOption(
            name="enabled",
            label="Show Recycle Bin icon",
            type="checkbox",
            default=True,
            description="Adds the Recycle Bin icon to your desktop"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel",
                value_name="{645FF040-5081-101B-9F08-00AA002F954E}",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="explorer_desktop_controlpanel",
        name="Show Control Panel on Desktop",
        category=TweakCategory.EXPLORER,
        description="Show the Control Panel icon on the desktop",
        option=TweakOption(
            name="enabled",
            label="Show Control Panel icon",
            type="checkbox",
            default=False,
            description="Adds the Control Panel icon to your desktop"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel",
                value_name="{5399E694-6CE5-4D6C-8FCE-1D8870FDCBA0}",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="explorer_no_recent_jump",
        name="Disable Recent Files in Jump Lists",
        category=TweakCategory.EXPLORER,
        description="Stop recording recent files in taskbar jump lists",
        option=TweakOption(
            name="enabled",
            label="Disable recent items history",
            type="checkbox",
            default=False,
            description="Prevents recently used files from appearing in jump lists"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer",
                value_name="NoRecentDocsHistory",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="explorer_navpane_all_folders",
        name="Show All Folders in Navigation Pane",
        category=TweakCategory.EXPLORER,
        description="Expand the navigation pane to show every folder",
        option=TweakOption(
            name="enabled",
            label="Show all folders",
            type="checkbox",
            default=False,
            description="Includes Desktop, Recycle Bin, Control Panel and more in the side pane"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="NavPaneShowAllFolders",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="explorer_no_sync_ads",
        name="Hide OneDrive Sync Ads in Explorer",
        category=TweakCategory.EXPLORER,
        description="Remove the 'Get more storage' and OneDrive promotion banners in File Explorer",
        option=TweakOption(
            name="enabled",
            label="Hide sync provider notifications",
            type="checkbox",
            default=False,
            description="Removes OneDrive advertising banners from Explorer"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="ShowSyncProviderNotifications",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="explorer_expand_nav_to_folder",
        name="Auto-Expand Navigation Pane to Current Folder",
        category=TweakCategory.EXPLORER,
        description="Automatically expand the left navigation pane to show the currently open folder",
        option=TweakOption(
            name="enabled",
            label="Expand nav pane to current folder",
            type="checkbox",
            default=False,
            description="Navigation pane always highlights and expands to where you are"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="NavPaneExpandToCurrentFolder",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="explorer_full_path_address_bar",
        name="Show Full Path in Address Bar",
        category=TweakCategory.EXPLORER,
        description="Display the complete folder path in Explorer's address bar instead of breadcrumbs",
        option=TweakOption(
            name="enabled",
            label="Show full path in address bar",
            type="checkbox",
            default=False,
            description="Address bar shows e.g. C:\\Users\\You\\Documents instead of > Documents"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="FullPathAddress",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="explorer_no_recycle_confirm",
        name="Skip Recycle Bin Delete Confirmation",
        category=TweakCategory.EXPLORER,
        description="Delete files directly to Recycle Bin without the 'Are you sure?' prompt",
        option=TweakOption(
            name="enabled",
            label="Skip delete confirmation dialog",
            type="checkbox",
            default=False,
            description="Files go straight to Recycle Bin — no confirm box"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer",
                value_name="ConfirmFileDelete",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="explorer_show_encrypted_color",
        name="Show Encrypted/Compressed Files in Color",
        category=TweakCategory.EXPLORER,
        description="Display encrypted files in green and compressed files in blue in Explorer",
        option=TweakOption(
            name="enabled",
            label="Color-code encrypted/compressed files",
            type="checkbox",
            default=False,
            description="Easy visual identification of NTFS-encrypted and compressed files"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="ShowEncryptCompressedColor",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="explorer_status_bar",
        name="Show Status Bar",
        category=TweakCategory.EXPLORER,
        description="Show the status bar at the bottom of File Explorer windows",
        option=TweakOption(
            name="enabled",
            label="Show status bar",
            type="checkbox",
            default=False,
            description="Displays item count, selected size, and file details at the bottom of Explorer"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="ShowStatusBar",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="explorer_folder_size_tips",
        name="Show Folder Size in Tooltips",
        category=TweakCategory.EXPLORER,
        description="Display item count and size information in folder hover tooltips",
        option=TweakOption(
            name="enabled",
            label="Show folder contents info",
            type="checkbox",
            default=False,
            description="Hovering over a folder shows a tooltip with the number of items inside"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="FolderContentsInfoTip",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="explorer_sharing_wizard",
        name="Disable Simplified Sharing Wizard",
        category=TweakCategory.EXPLORER,
        description="Use the full Share dialog instead of the simplified wizard",
        option=TweakOption(
            name="enabled",
            label="Disable sharing wizard",
            type="checkbox",
            default=False,
            description="Shows advanced permissions dialog when sharing; gives finer control over share settings"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="SharingWizardOn",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="explorer_separate_process",
        name="Run Explorer Windows in Separate Processes",
        category=TweakCategory.EXPLORER,
        description="Each File Explorer window gets its own process — a crash won't take down all windows",
        option=TweakOption(
            name="enabled",
            label="Separate process per window",
            type="checkbox",
            default=False,
            description="More resilient but uses slightly more RAM; useful on unstable systems"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="SeparateProcess",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="explorer_icon_cache",
        name="Icon Cache Size",
        category=TweakCategory.EXPLORER,
        description="Set the maximum number of icons Windows caches in memory",
        option=TweakOption(
            name="size",
            label="Cache size (icons)",
            type="spinbox",
            default=4096,
            description="Default is 500; raising to 4096+ reduces icon re-rendering in large folders",
            min_value=500,
            max_value=16384
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer",
                value_name="Max Cached Icons",
                value_type=winreg.REG_SZ,
                enabled_value=None,
                disabled_value=None
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
    Tweak(
        id="system_disable_winl",
        name="Disable Win+L Lock Hotkey",
        category=TweakCategory.SYSTEM,
        description="Disable the Win+L keyboard shortcut that locks the workstation",
        option=TweakOption(
            name="enabled",
            label="Disable Win+L",
            type="checkbox",
            default=False,
            description="Useful if you keep accidentally locking yourself out"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Policies\System",
                value_name="DisableLockWorkstation",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="system_long_paths",
        name="Enable Long File Paths (>260 chars)",
        category=TweakCategory.SYSTEM,
        description="Allow file paths longer than the legacy 260-character MAX_PATH limit",
        option=TweakOption(
            name="enabled",
            label="Enable long paths",
            type="checkbox",
            default=False,
            description="Required by some dev tools and deep folder structures"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\FileSystem",
                value_name="LongPathsEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="system_verbose_status",
        name="Show Verbose Boot/Shutdown Status",
        category=TweakCategory.SYSTEM,
        description="Display detailed status messages during Windows startup and shutdown",
        option=TweakOption(
            name="enabled",
            label="Show detailed status messages",
            type="checkbox",
            default=False,
            description="See exactly what Windows is loading or stopping at each step"
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
        id="system_remote_uac",
        name="Disable UAC for Remote Admin Connections",
        category=TweakCategory.SYSTEM,
        description="Allow local admin accounts to connect remotely without UAC token filtering",
        option=TweakOption(
            name="enabled",
            label="Disable remote UAC filtering",
            type="checkbox",
            default=False,
            description="Useful for remote management; built-in Administrator is unaffected"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System",
                value_name="LocalAccountTokenFilterPolicy",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="system_print_screen_snip",
        name="PrtScn Opens Snipping Tool",
        category=TweakCategory.SYSTEM,
        description="Make the Print Screen key open Snipping Tool instead of copying to clipboard",
        option=TweakOption(
            name="enabled",
            label="PrtScn → Snipping Tool",
            type="checkbox",
            default=False,
            description="Pressing PrtScn launches the modern Snipping Tool overlay"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Keyboard",
                value_name="PrintScreenKeyForSnippingEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="system_show_seconds_clock",
        name="Show Seconds in Taskbar Clock",
        category=TweakCategory.SYSTEM,
        description="Display seconds alongside hours and minutes in the taskbar system clock",
        option=TweakOption(
            name="enabled",
            label="Show seconds in clock",
            type="checkbox",
            default=False,
            description="Taskbar clock shows HH:MM:SS instead of HH:MM"
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
        ],
        requires_restart=True
    ),
    Tweak(
        id="system_delivery_optimization",
        name="Disable Delivery Optimization P2P Upload",
        category=TweakCategory.SYSTEM,
        description="Stop Windows from using your bandwidth to upload updates to other PCs",
        option=TweakOption(
            name="mode",
            label="Download mode",
            type="dropdown",
            default=1,
            description="HTTP Only stops all P2P sharing; LAN-only keeps local sharing but blocks internet upload",
            choices=[
                (0, "HTTP only (no P2P)"),
                (1, "LAN only (no internet P2P)"),
                (3, "LAN + Internet P2P (default)")
            ]
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows\DeliveryOptimization",
                value_name="DODownloadMode",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="system_consumer_features",
        name="Disable Consumer Experience / Cloud Features",
        category=TweakCategory.SYSTEM,
        description="Stop Windows from auto-installing suggested/promoted apps from the cloud",
        option=TweakOption(
            name="enabled",
            label="Disable consumer experience",
            type="checkbox",
            default=False,
            description="Blocks the Windows consumer features check that installs Candy Crush etc. on first login"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows\CloudContent",
                value_name="DisableWindowsConsumerFeatures",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="system_startup_sound",
        name="Disable Windows Startup Sound",
        category=TweakCategory.SYSTEM,
        description="Silence the chime that plays when Windows boots to the login screen",
        option=TweakOption(
            name="enabled",
            label="Disable startup sound",
            type="checkbox",
            default=False,
            description="Suppresses the boot sound; useful for shared offices or late-night reboots"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\LogonUI\BootAnimation",
                value_name="DisableStartupSound",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="system_utc_clock",
        name="Hardware Clock Uses UTC",
        category=TweakCategory.SYSTEM,
        description="Tell Windows to treat the hardware (BIOS) clock as UTC instead of local time",
        option=TweakOption(
            name="enabled",
            label="Hardware clock is UTC",
            type="checkbox",
            default=False,
            description="Essential for dual-boot with Linux; prevents the two OSes from fighting over the clock"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\TimeZoneInformation",
                value_name="RealTimeIsUniversal",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="system_auto_maintenance",
        name="Disable Automatic Maintenance",
        category=TweakCategory.SYSTEM,
        description="Prevent Windows from running scheduled maintenance tasks in the background",
        option=TweakOption(
            name="enabled",
            label="Disable automatic maintenance",
            type="checkbox",
            default=False,
            description="Stops disk defrag, security scans, and diagnostics from running automatically; run them manually instead"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\Maintenance",
                value_name="MaintenanceDisabled",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="system_max_connections",
        name="Max HTTP Connections per Server",
        category=TweakCategory.SYSTEM,
        description="Increase the maximum simultaneous HTTP/1.1 connections to a single host",
        option=TweakOption(
            name="connections",
            label="Max connections",
            type="spinbox",
            default=10,
            description="Default is 2 (per HTTP spec); raising to 10 speeds up apps with many parallel web requests",
            min_value=2,
            max_value=32
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                value_name="MaxConnectionsPerServer",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            ),
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                value_name="MaxConnectionsPer1_0Server",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
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
    Tweak(
        id="privacy_activity_history",
        name="Disable Activity History",
        category=TweakCategory.PRIVACY,
        description="Stop Windows from collecting activity history (Timeline)",
        option=TweakOption(
            name="enabled",
            label="Disable activity history",
            type="checkbox",
            default=False,
            description="Prevents apps from publishing activities to your account"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows\System",
                value_name="PublishUserActivities",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            ),
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows\System",
                value_name="UploadUserActivities",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="privacy_inking_typing",
        name="Disable Inking & Typing Personalization",
        category=TweakCategory.PRIVACY,
        description="Stop Windows from learning from your handwriting and typing",
        option=TweakOption(
            name="enabled",
            label="Disable inking/typing data collection",
            type="checkbox",
            default=False,
            description="Prevents Windows from building a personal dictionary from your input"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\InputPersonalization",
                value_name="RestrictImplicitTextCollection",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            ),
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\InputPersonalization",
                value_name="RestrictImplicitInkCollection",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="priv_app_suggestions_start",
        name="Disable App Suggestions in Start Menu",
        category=TweakCategory.PRIVACY,
        description="Remove Microsoft's suggested/promoted apps from the Start menu",
        option=TweakOption(
            name="enabled",
            label="Disable app suggestions",
            type="checkbox",
            default=False,
            description="Stops sponsored app ads appearing in Start"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                value_name="SubscribedContent-338388Enabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="priv_windows_tips",
        name="Disable Windows Tips & Tricks Notifications",
        category=TweakCategory.PRIVACY,
        description="Stop Windows from showing tips and suggestions as notifications",
        option=TweakOption(
            name="enabled",
            label="Disable tips notifications",
            type="checkbox",
            default=False,
            description="Suppresses 'Did you know...' and feature discovery balloons"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                value_name="SubscribedContent-338389Enabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="priv_welcome_experience",
        name="Disable Welcome Experience After Updates",
        category=TweakCategory.PRIVACY,
        description="Prevent Windows from showing 'What's new' screens after feature updates",
        option=TweakOption(
            name="enabled",
            label="Disable post-update welcome screen",
            type="checkbox",
            default=False,
            description="Skips the Microsoft account promotion splash after Windows updates"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                value_name="SubscribedContent-310093Enabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="priv_map_updates",
        name="Disable Automatic Map Downloads",
        category=TweakCategory.PRIVACY,
        description="Stop Windows Maps from automatically downloading map data in the background",
        option=TweakOption(
            name="enabled",
            label="Disable automatic map updates",
            type="checkbox",
            default=False,
            description="Saves bandwidth and background CPU used by the Maps service"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\Maps",
                value_name="AutoUpdateEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="priv_lock_screen_ads",
        name="Disable Lock Screen Ads & Spotlight Tips",
        category=TweakCategory.PRIVACY,
        description="Remove Microsoft-curated images and promotional tips from the lock screen",
        option=TweakOption(
            name="enabled",
            label="Disable lock screen ads",
            type="checkbox",
            default=False,
            description="Stops Spotlight images and ad overlays on the lock screen"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                value_name="RotatingLockScreenOverlayEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="priv_location_services",
        name="Disable Location Services",
        category=TweakCategory.PRIVACY,
        description="Block all apps from accessing Windows Location Services",
        option=TweakOption(
            name="enabled",
            label="Disable location access",
            type="checkbox",
            default=False,
            description="Denies location permission system-wide; individual apps can't override"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location",
                value_name="Value",
                value_type=winreg.REG_SZ,
                enabled_value="Deny",
                disabled_value="Allow"
            )
        ]
    ),
    Tweak(
        id="priv_camera_global",
        name="Disable Camera Access (All Apps)",
        category=TweakCategory.PRIVACY,
        description="Block all apps from accessing the camera at the system level",
        option=TweakOption(
            name="enabled",
            label="Deny camera to all apps",
            type="checkbox",
            default=False,
            description="System-wide camera deny; no app can request camera until re-enabled"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam",
                value_name="Value",
                value_type=winreg.REG_SZ,
                enabled_value="Deny",
                disabled_value="Allow"
            )
        ]
    ),
    Tweak(
        id="priv_microphone_global",
        name="Disable Microphone Access (All Apps)",
        category=TweakCategory.PRIVACY,
        description="Block all apps from accessing the microphone at the system level",
        option=TweakOption(
            name="enabled",
            label="Deny microphone to all apps",
            type="checkbox",
            default=False,
            description="System-wide microphone deny; no app can record audio until re-enabled"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\microphone",
                value_name="Value",
                value_type=winreg.REG_SZ,
                enabled_value="Deny",
                disabled_value="Allow"
            )
        ]
    ),
    Tweak(
        id="priv_app_launch_tracking",
        name="Disable App Launch Tracking",
        category=TweakCategory.PRIVACY,
        description="Stop Windows from tracking which apps you launch to personalise Start Menu",
        option=TweakOption(
            name="enabled",
            label="Disable launch tracking",
            type="checkbox",
            default=False,
            description="Windows won't build a 'most used apps' list or promote frequently-opened apps"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="Start_TrackProgs",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="priv_settings_ads",
        name="Disable Ads and Suggested Content in Settings",
        category=TweakCategory.PRIVACY,
        description="Remove Microsoft promotional content from the Settings app",
        option=TweakOption(
            name="enabled",
            label="Disable Settings ads",
            type="checkbox",
            default=False,
            description="Blocks the three SubscribedContent keys that push ads into Settings pages"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                value_name="SubscribedContent-338393Enabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            ),
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                value_name="SubscribedContent-353694Enabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            ),
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                value_name="SubscribedContent-353696Enabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="priv_voice_activation",
        name="Disable Voice Activation for All Apps",
        category=TweakCategory.PRIVACY,
        description="Prevent any app from being activated by voice commands in the background",
        option=TweakOption(
            name="enabled",
            label="Disable voice activation",
            type="checkbox",
            default=False,
            description="Blocks always-on mic listening for voice assistants at the user-preference level"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Speech_OneCore\Settings\VoiceActivation\UserPreferenceForAllApps",
                value_name="AgentActivationEnabled",
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
    Tweak(
        id="perf_no_drag_full",
        name="Disable Drag Full Windows",
        category=TweakCategory.PERFORMANCE,
        description="Show only the window outline while dragging instead of full contents",
        option=TweakOption(
            name="enabled",
            label="Show outline only when dragging",
            type="checkbox",
            default=False,
            description="Reduces GPU work when moving windows around"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Desktop",
                value_name="DragFullWindows",
                value_type=winreg.REG_SZ,
                enabled_value="0",
                disabled_value="1"
            )
        ],
        requires_logoff=True
    ),
    Tweak(
        id="perf_hung_timeout",
        name="Reduce Hung App Timeout",
        category=TweakCategory.PERFORMANCE,
        description="How long Windows waits before declaring an app unresponsive",
        option=TweakOption(
            name="timeout",
            label="Hung app timeout (ms)",
            type="spinbox",
            default=5000,
            description="Lower = faster 'Not Responding' detection (default 5000)",
            min_value=1000,
            max_value=20000
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Desktop",
                value_name="HungAppTimeout",
                value_type=winreg.REG_SZ,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="perf_kill_timeout",
        name="Reduce Wait-To-Kill App Timeout",
        category=TweakCategory.PERFORMANCE,
        description="How long Windows waits for an app to close on shutdown",
        option=TweakOption(
            name="timeout",
            label="Wait-to-kill timeout (ms)",
            type="spinbox",
            default=5000,
            description="Lower = faster shutdowns when apps stall (default 20000)",
            min_value=1000,
            max_value=30000
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Desktop",
                value_name="WaitToKillAppTimeout",
                value_type=winreg.REG_SZ,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="perf_no_startup_delay",
        name="Disable Startup Delay",
        category=TweakCategory.PERFORMANCE,
        description="Remove the artificial delay before startup apps launch",
        option=TweakOption(
            name="enabled",
            label="Disable startup delay",
            type="checkbox",
            default=False,
            description="Boots straight into your startup apps without the throttling delay"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Serialize",
                value_name="StartupDelayInMSec",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="perf_min_animate",
        name="Disable Minimize/Maximize Animations",
        category=TweakCategory.PERFORMANCE,
        description="Skip the shrink/grow animation when minimizing or maximizing windows",
        option=TweakOption(
            name="enabled",
            label="Disable min/max animations",
            type="checkbox",
            default=False,
            description="Windows snap open and shut instantly instead of animating"
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
        ],
        requires_logoff=True
    ),
    Tweak(
        id="perf_auto_end_tasks",
        name="Auto-End Unresponsive Apps on Shutdown",
        category=TweakCategory.PERFORMANCE,
        description="Automatically kill hung apps during shutdown instead of waiting for you to confirm",
        option=TweakOption(
            name="enabled",
            label="Auto-end unresponsive apps",
            type="checkbox",
            default=False,
            description="Speeds up shutdown when apps refuse to close"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Desktop",
                value_name="AutoEndTasks",
                value_type=winreg.REG_SZ,
                enabled_value="1",
                disabled_value="0"
            )
        ]
    ),
    Tweak(
        id="perf_low_disk_check",
        name="Disable Low Disk Space Warnings",
        category=TweakCategory.PERFORMANCE,
        description="Stop Windows from scanning drives and showing low disk space balloon tips",
        option=TweakOption(
            name="enabled",
            label="Disable low disk space checks",
            type="checkbox",
            default=False,
            description="Removes periodic disk-scan overhead and the warning balloons"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer",
                value_name="NoLowDiskSpaceChecks",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="perf_paging_exec",
        name="Keep Kernel in RAM",
        category=TweakCategory.PERFORMANCE,
        description="Prevent Windows from paging kernel and driver code to disk",
        option=TweakOption(
            name="enabled",
            label="Disable kernel paging (keep in RAM)",
            type="checkbox",
            default=False,
            description="Reduces latency on systems with enough RAM (4 GB+)"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management",
                value_name="DisablePagingExecutive",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="perf_ntfs_timestamp",
        name="Disable NTFS Last Access Timestamps",
        category=TweakCategory.PERFORMANCE,
        description="Stop NTFS from updating the last-accessed time on every file read",
        option=TweakOption(
            name="enabled",
            label="Disable last access timestamps",
            type="checkbox",
            default=False,
            description="Cuts disk write overhead on busy drives"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\FileSystem",
                value_name="NtfsDisableLastAccessUpdate",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="perf_8dot3_names",
        name="Disable 8.3 Filename Creation",
        category=TweakCategory.PERFORMANCE,
        description="Stop NTFS from generating legacy short filenames (e.g. PROGRA~1)",
        option=TweakOption(
            name="enabled",
            label="Disable 8.3 short name creation",
            type="checkbox",
            default=False,
            description="Speeds up file operations on drives with many files"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\FileSystem",
                value_name="NtfsDisable8dot3NameCreation",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="perf_prefetcher",
        name="Prefetcher Mode",
        category=TweakCategory.PERFORMANCE,
        description="Control what Windows Prefetcher pre-loads into RAM on boot",
        option=TweakOption(
            name="mode",
            label="Prefetch mode",
            type="dropdown",
            default=3,
            description="Controls what gets preloaded: apps, boot files, or both",
            choices=[
                (0, "Disabled"),
                (1, "App launch only"),
                (2, "Boot files only"),
                (3, "Apps + Boot (default)"),
            ]
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters",
                value_name="EnablePrefetcher",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="perf_foreground_timeout",
        name="Foreground App Switch Speed",
        category=TweakCategory.PERFORMANCE,
        description="How quickly Windows gives CPU priority to the app you just clicked",
        option=TweakOption(
            name="timeout",
            label="Foreground lock timeout (µs)",
            type="spinbox",
            default=200000,
            description="0 = instant switch, 200000 = Windows default. Lower = snappier switching",
            min_value=0,
            max_value=200000
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Desktop",
                value_name="ForegroundLockTimeout",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="perf_service_kill_timeout",
        name="Service Shutdown Timeout",
        category=TweakCategory.PERFORMANCE,
        description="How long Windows waits for services to stop during shutdown before killing them",
        option=TweakOption(
            name="timeout",
            label="Service kill timeout (ms)",
            type="spinbox",
            default=20000,
            description="Lower value = faster shutdowns when services hang (default 20000)",
            min_value=2000,
            max_value=20000
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control",
                value_name="WaitToKillServiceTimeout",
                value_type=winreg.REG_SZ,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="perf_clear_pagefile",
        name="Clear Pagefile on Shutdown",
        category=TweakCategory.PERFORMANCE,
        description="Wipe the pagefile when Windows shuts down for better security (slower shutdown)",
        option=TweakOption(
            name="enabled",
            label="Clear pagefile at shutdown",
            type="checkbox",
            default=False,
            description="Prevents data remnants in the pagefile — security benefit at cost of slower shutdown"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management",
                value_name="ClearPageFileAtShutdown",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="perf_games_cpu_priority",
        name="Raise CPU Priority for Games",
        category=TweakCategory.PERFORMANCE,
        description="Set the CPU scheduling priority for the Games multimedia task profile to maximum",
        option=TweakOption(
            name="priority",
            label="Games CPU priority (1–6)",
            type="spinbox",
            default=2,
            description="6 = highest priority, 2 = Windows default. Raises CPU time for game processes",
            min_value=1,
            max_value=6
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
                value_name="Priority",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="perf_win32_priority",
        name="Foreground Process Priority Boost",
        category=TweakCategory.PERFORMANCE,
        description="Control how much extra CPU priority the active foreground window receives",
        option=TweakOption(
            name="mode",
            label="Priority separation",
            type="dropdown",
            default=2,
            description="Controls foreground vs background CPU time slice length",
            choices=[
                (0, "No boost (equal priority)"),
                (2, "Short variable boost (default)"),
                (24, "Long fixed — best for apps"),
                (38, "Short fixed — best for gaming"),
            ]
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\PriorityControl",
                value_name="Win32PrioritySeparation",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="perf_trim_ssd",
        name="Enable SSD TRIM (Disable Delete Notification Throttle)",
        category=TweakCategory.PERFORMANCE,
        description="Ensure NTFS sends TRIM commands to SSDs without throttling",
        option=TweakOption(
            name="enabled",
            label="Enable TRIM (disable throttle)",
            type="checkbox",
            default=False,
            description="Sets DisableDeleteNotification=0; keeps SSD performance from degrading over time"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\FileSystem",
                value_name="DisableDeleteNotification",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="perf_optimize_for_programs",
        name="Optimize Memory for Programs (Not Throughput)",
        category=TweakCategory.PERFORMANCE,
        description="Set LargeSystemCache=0 to prioritize working set of running programs over file cache",
        option=TweakOption(
            name="enabled",
            label="Optimize for programs",
            type="checkbox",
            default=False,
            description="Default for workstations; servers use LargeSystemCache=1. Most desktops already have this set"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management",
                value_name="LargeSystemCache",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="perf_sfc_scan_disable",
        name="Disable SFC Boot Scan",
        category=TweakCategory.PERFORMANCE,
        description="Stop System File Checker from running a full integrity scan on every boot",
        option=TweakOption(
            name="enabled",
            label="Disable SFC boot scan",
            type="checkbox",
            default=False,
            description="⚠ Skips automatic OS file verification; boot is faster but corruption goes undetected"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon",
                value_name="SFCDisable",
                value_type=winreg.REG_DWORD,
                enabled_value=4,
                disabled_value=0
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="perf_heap_decommit",
        name="Heap Decommit Free Block Threshold",
        category=TweakCategory.PERFORMANCE,
        description="Control when the heap manager returns free memory blocks to the OS",
        option=TweakOption(
            name="threshold",
            label="Threshold (bytes)",
            type="spinbox",
            default=262144,
            description="Lower = faster reuse of small allocations; 262144 (256 KB) is a good balance",
            min_value=4096,
            max_value=4194304
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Session Manager\HeapManager",
                value_name="DeCommitFreeBlockThreshold",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="perf_wmi_adapter_disable",
        name="Disable WMI Performance Adapter Service",
        category=TweakCategory.PERFORMANCE,
        description="Stop the WmiApSrv service that exposes performance counters via WMI",
        option=TweakOption(
            name="enabled",
            label="Disable WMI performance adapter",
            type="checkbox",
            default=False,
            description="Reduces background WMI polling; safe unless you have monitoring tools that query WMI counters"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\wmiApSrv",
                value_name="Start",
                value_type=winreg.REG_DWORD,
                enabled_value=4,
                disabled_value=3
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="perf_crash_dump_type",
        name="Crash Dump Type",
        category=TweakCategory.PERFORMANCE,
        description="Choose how much data is saved when Windows crashes (BSOD)",
        option=TweakOption(
            name="type",
            label="Dump type",
            type="dropdown",
            default=7,
            description="Smaller dumps save disk space; complete dumps help debugging but require lots of space",
            choices=[
                (0, "None (no dump)"),
                (3, "Small memory dump"),
                (2, "Kernel memory dump"),
                (1, "Complete memory dump"),
                (7, "Automatic (default)")
            ]
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\CrashControl",
                value_name="CrashDumpEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="perf_max_connections",
        name="Max Internet Connections per Server",
        category=TweakCategory.PERFORMANCE,
        description="Increase the maximum simultaneous HTTP connections per host",
        option=TweakOption(
            name="connections",
            label="Max connections",
            type="spinbox",
            default=10,
            description="Default is 2 (HTTP/1.1 spec); raising to 10–16 speeds up sites/apps with many parallel requests",
            min_value=2,
            max_value=32
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                value_name="MaxConnectionsPerServer",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            ),
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                value_name="MaxConnectionsPer1_0Server",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
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
    Tweak(
        id="context_pwsh_admin_here",
        name="Add 'Open PowerShell Here as Admin'",
        category=TweakCategory.CONTEXT_MENU,
        description="Add 'Open PowerShell here as Administrator' to folder right-click",
        option=TweakOption(
            name="enabled",
            label="Add PowerShell admin shortcut",
            type="checkbox",
            default=False,
            description="Right-click any folder background to launch an elevated PowerShell"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CLASSES_ROOT,
                key_path=r"Directory\Background\shell\PowerShellAdmin",
                value_name="",
                value_type=winreg.REG_SZ,
                enabled_value="Open PowerShell here as Administrator",
                disabled_value=None
            ),
            RegistryChange(
                hive=winreg.HKEY_CLASSES_ROOT,
                key_path=r"Directory\Background\shell\PowerShellAdmin",
                value_name="HasLUAShield",
                value_type=winreg.REG_SZ,
                enabled_value="",
                disabled_value=None
            ),
            RegistryChange(
                hive=winreg.HKEY_CLASSES_ROOT,
                key_path=r"Directory\Background\shell\PowerShellAdmin\command",
                value_name="",
                value_type=winreg.REG_SZ,
                enabled_value=r'powershell.exe -Command "Start-Process powershell -ArgumentList \"-NoExit\", \"-Command\", \"Set-Location -LiteralPath \'%V\'\" -Verb RunAs"',
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="context_cmd_admin_here",
        name="Add 'Open Command Prompt Here as Admin'",
        category=TweakCategory.CONTEXT_MENU,
        description="Add 'Open Command Prompt here as Administrator' to folder right-click",
        option=TweakOption(
            name="enabled",
            label="Add Command Prompt admin shortcut",
            type="checkbox",
            default=False,
            description="Right-click any folder background to launch an elevated cmd.exe"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CLASSES_ROOT,
                key_path=r"Directory\Background\shell\CmdAdmin",
                value_name="",
                value_type=winreg.REG_SZ,
                enabled_value="Open Command Prompt here as Administrator",
                disabled_value=None
            ),
            RegistryChange(
                hive=winreg.HKEY_CLASSES_ROOT,
                key_path=r"Directory\Background\shell\CmdAdmin",
                value_name="HasLUAShield",
                value_type=winreg.REG_SZ,
                enabled_value="",
                disabled_value=None
            ),
            RegistryChange(
                hive=winreg.HKEY_CLASSES_ROOT,
                key_path=r"Directory\Background\shell\CmdAdmin\command",
                value_name="",
                value_type=winreg.REG_SZ,
                enabled_value=r'powershell.exe -Command "Start-Process cmd -ArgumentList \"/k\", \"cd /d %V\" -Verb RunAs"',
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="context_take_ownership",
        name="Add 'Take Ownership'",
        category=TweakCategory.CONTEXT_MENU,
        description="Add 'Take Ownership' to files and folders right-click menus",
        option=TweakOption(
            name="enabled",
            label="Add Take Ownership shortcut",
            type="checkbox",
            default=False,
            description="One-click takeown + icacls for the selected file or folder (requires admin)"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CLASSES_ROOT,
                key_path=r"*\shell\TakeOwnership",
                value_name="",
                value_type=winreg.REG_SZ,
                enabled_value="Take Ownership",
                disabled_value=None
            ),
            RegistryChange(
                hive=winreg.HKEY_CLASSES_ROOT,
                key_path=r"*\shell\TakeOwnership",
                value_name="HasLUAShield",
                value_type=winreg.REG_SZ,
                enabled_value="",
                disabled_value=None
            ),
            RegistryChange(
                hive=winreg.HKEY_CLASSES_ROOT,
                key_path=r"*\shell\TakeOwnership\command",
                value_name="",
                value_type=winreg.REG_SZ,
                enabled_value=r'cmd.exe /c takeown /f "%1" && icacls "%1" /grant administrators:F',
                disabled_value=None
            ),
            RegistryChange(
                hive=winreg.HKEY_CLASSES_ROOT,
                key_path=r"Directory\shell\TakeOwnership",
                value_name="",
                value_type=winreg.REG_SZ,
                enabled_value="Take Ownership",
                disabled_value=None
            ),
            RegistryChange(
                hive=winreg.HKEY_CLASSES_ROOT,
                key_path=r"Directory\shell\TakeOwnership",
                value_name="HasLUAShield",
                value_type=winreg.REG_SZ,
                enabled_value="",
                disabled_value=None
            ),
            RegistryChange(
                hive=winreg.HKEY_CLASSES_ROOT,
                key_path=r"Directory\shell\TakeOwnership\command",
                value_name="",
                value_type=winreg.REG_SZ,
                enabled_value=r'cmd.exe /c takeown /f "%1" /r /d y && icacls "%1" /grant administrators:F /t',
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="context_copy_as_path",
        name="Add 'Copy as Path' to Context Menu",
        category=TweakCategory.CONTEXT_MENU,
        description="Add a 'Copy as Path' entry to the right-click menu for files and folders",
        option=TweakOption(
            name="enabled",
            label="Add 'Copy as Path'",
            type="checkbox",
            default=False,
            description="One-click way to copy the full file path to clipboard without holding Shift"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Classes\Allfilesystemobjects\shellex\ContextMenuHandlers\CopyAsPathMenu",
                value_name="",
                value_type=winreg.REG_SZ,
                enabled_value="{f3d06e7c-1e45-4a26-847e-f9fcdee59be0}",
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="context_no_share",
        name="Remove 'Share' from Context Menu",
        category=TweakCategory.CONTEXT_MENU,
        description="Block the Share shell extension so it no longer appears in right-click menus",
        option=TweakOption(
            name="enabled",
            label="Remove Share entry",
            type="checkbox",
            default=False,
            description="Hides the Share option that opens the Windows sharing pane"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Shell Extensions\Blocked",
                value_name="{E2BF9676-5F8F-435C-97EB-11607A5BEDF7}",
                value_type=winreg.REG_SZ,
                enabled_value="",
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="context_no_cast",
        name="Remove 'Cast to Device' from Context Menu",
        category=TweakCategory.CONTEXT_MENU,
        description="Block the Cast to Device shell extension from the right-click menu",
        option=TweakOption(
            name="enabled",
            label="Remove Cast to Device entry",
            type="checkbox",
            default=False,
            description="Removes the DLNA casting option for users without smart TVs or Cast devices"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Shell Extensions\Blocked",
                value_name="{7AD84985-87B4-4a16-BE58-8B72A5B390F7}",
                value_type=winreg.REG_SZ,
                enabled_value="",
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
    Tweak(
        id="pers_no_lockscreen_tips",
        name="Disable Lock Screen Tips",
        category=TweakCategory.PERSONALIZATION,
        description="Hide tips, tricks and ads on the lock screen",
        option=TweakOption(
            name="enabled",
            label="Disable lock screen tips",
            type="checkbox",
            default=False,
            description="Stops Microsoft from showing 'fun facts' on the lock screen"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                value_name="RotatingLockScreenOverlayEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="pers_no_spotlight",
        name="Disable Windows Spotlight on Lock Screen",
        category=TweakCategory.PERSONALIZATION,
        description="Stop Windows from rotating Spotlight images on the lock screen",
        option=TweakOption(
            name="enabled",
            label="Disable Spotlight",
            type="checkbox",
            default=False,
            description="Lock screen will use a fixed picture instead of changing daily"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                value_name="RotatingLockScreenEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="pers_border_width",
        name="Window Border Width",
        category=TweakCategory.PERSONALIZATION,
        description="Inner border width around windows",
        option=TweakOption(
            name="width",
            label="Border width",
            type="spinbox",
            default=-15,
            description="Negative twips (default -15). Lower (more negative) = thicker border",
            min_value=-100,
            max_value=0
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Desktop\WindowMetrics",
                value_name="BorderWidth",
                value_type=winreg.REG_SZ,
                enabled_value=None,
                disabled_value=None
            )
        ],
        requires_logoff=True
    ),
    Tweak(
        id="pers_padded_border",
        name="Window Padded Border",
        category=TweakCategory.PERSONALIZATION,
        description="Outer padded border around windows (Win11 hover region)",
        option=TweakOption(
            name="width",
            label="Padded border",
            type="spinbox",
            default=-60,
            description="Negative twips (default -60). Affects window resize hit-zone",
            min_value=-200,
            max_value=0
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Desktop\WindowMetrics",
                value_name="PaddedBorderWidth",
                value_type=winreg.REG_SZ,
                enabled_value=None,
                disabled_value=None
            )
        ],
        requires_logoff=True
    ),
    Tweak(
        id="pers_font_smoothing",
        name="Disable ClearType Font Smoothing",
        category=TweakCategory.PERSONALIZATION,
        description="Turn off subpixel font smoothing system-wide",
        option=TweakOption(
            name="enabled",
            label="Disable font smoothing",
            type="checkbox",
            default=False,
            description="Some users prefer crisp pixel-aligned fonts on high-DPI displays"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Desktop",
                value_name="FontSmoothing",
                value_type=winreg.REG_SZ,
                enabled_value="0",
                disabled_value="2"
            )
        ],
        requires_logoff=True
    ),
    Tweak(
        id="pers_listview_alpha",
        name="Disable Translucent Selection Rectangle",
        category=TweakCategory.PERSONALIZATION,
        description="Use a classic outline instead of a translucent box when drag-selecting",
        option=TweakOption(
            name="enabled",
            label="Disable translucent rectangle",
            type="checkbox",
            default=False,
            description="Replaces the alpha-blended selection box with a classic dotted outline"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="ListviewAlphaSelect",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ],
        requires_restart=True
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
    Tweak(
        id="acc_double_click_speed",
        name="Mouse Double-Click Speed",
        category=TweakCategory.ACCESSIBILITY,
        description="How fast you have to double-click for it to register",
        option=TweakOption(
            name="speed",
            label="Double-click speed (ms)",
            type="spinbox",
            default=500,
            description="Lower = faster (default 500). Range 200-900",
            min_value=200,
            max_value=900
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Mouse",
                value_name="DoubleClickSpeed",
                value_type=winreg.REG_SZ,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="acc_mouse_hover_time",
        name="Mouse Hover Time",
        category=TweakCategory.ACCESSIBILITY,
        description="How long you must hover before tooltips and hover events fire",
        option=TweakOption(
            name="time",
            label="Hover time (ms)",
            type="spinbox",
            default=400,
            description="Lower = faster tooltips. Default 400",
            min_value=0,
            max_value=10000
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Mouse",
                value_name="MouseHoverTime",
                value_type=winreg.REG_SZ,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="acc_keyboard_delay",
        name="Keyboard Repeat Delay",
        category=TweakCategory.ACCESSIBILITY,
        description="Pause before a held key starts repeating",
        option=TweakOption(
            name="delay",
            label="Repeat delay (0=long, 3=short)",
            type="spinbox",
            default=1,
            description="0=longest, 3=shortest delay before key repeats",
            min_value=0,
            max_value=3
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Keyboard",
                value_name="KeyboardDelay",
                value_type=winreg.REG_SZ,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="acc_keyboard_rate",
        name="Keyboard Repeat Rate",
        category=TweakCategory.ACCESSIBILITY,
        description="Speed at which a held key repeats",
        option=TweakOption(
            name="rate",
            label="Repeat rate (0=slow, 31=fast)",
            type="spinbox",
            default=31,
            description="0=slow, 31=fast. Default Windows is 31",
            min_value=0,
            max_value=31
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Keyboard",
                value_name="KeyboardSpeed",
                value_type=winreg.REG_SZ,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="acc_mouse_speed",
        name="Mouse Pointer Speed",
        category=TweakCategory.ACCESSIBILITY,
        description="Set how fast the mouse cursor moves across the screen",
        option=TweakOption(
            name="speed",
            label="Pointer speed (1–20)",
            type="spinbox",
            default=10,
            description="1=slowest, 10=Windows default, 20=fastest",
            min_value=1,
            max_value=20
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Mouse",
                value_name="MouseSensitivity",
                value_type=winreg.REG_SZ,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="acc_scroll_inactive",
        name="Scroll Inactive Windows on Hover",
        category=TweakCategory.ACCESSIBILITY,
        description="Scroll any window under the mouse pointer, even if it doesn't have focus",
        option=TweakOption(
            name="enabled",
            label="Scroll inactive windows",
            type="checkbox",
            default=False,
            description="MouseWheelRouting=2 routes scroll events to whichever window is under the cursor"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Desktop",
                value_name="MouseWheelRouting",
                value_type=winreg.REG_DWORD,
                enabled_value=2,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="acc_natural_scrolling",
        name="Touchpad Natural (Reverse) Scrolling",
        category=TweakCategory.ACCESSIBILITY,
        description="Reverse the touchpad scroll direction to match iOS/macOS natural scrolling",
        option=TweakOption(
            name="enabled",
            label="Enable natural scrolling",
            type="checkbox",
            default=False,
            description="Content follows finger direction (swipe down = scroll down). Precision Touchpad only"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\PrecisionTouchPad",
                value_name="ScrollDirection",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="acc_cursor_size",
        name="Cursor Size",
        category=TweakCategory.ACCESSIBILITY,
        description="Increase the cursor size for better visibility",
        option=TweakOption(
            name="size",
            label="Cursor size (1–15)",
            type="spinbox",
            default=1,
            description="1=default system cursor, 15=largest accessibility cursor",
            min_value=1,
            max_value=15
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Accessibility",
                value_name="CursorSize",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="acc_click_lock",
        name="Enable ClickLock",
        category=TweakCategory.ACCESSIBILITY,
        description="Hold the mouse button briefly to lock a drag, then release without holding",
        option=TweakOption(
            name="enabled",
            label="Enable ClickLock",
            type="checkbox",
            default=False,
            description="Useful for users who have difficulty holding the mouse button while dragging"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Mouse",
                value_name="ClickLock",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
]

# =============================================================================
# NETWORK TWEAKS
# =============================================================================

NETWORK_TWEAKS = [
    Tweak(
        id="net_disable_ipv6",
        name="Disable IPv6",
        category=TweakCategory.NETWORK,
        description="Disable the IPv6 stack system-wide",
        option=TweakOption(
            name="enabled",
            label="Disable IPv6",
            type="checkbox",
            default=False,
            description="Some legacy networks/games perform better without IPv6"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\Tcpip6\Parameters",
                value_name="DisabledComponents",
                value_type=winreg.REG_DWORD,
                enabled_value=0xFF,
                disabled_value=0
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="net_disable_llmnr",
        name="Disable LLMNR",
        category=TweakCategory.NETWORK,
        description="Disable Link-Local Multicast Name Resolution",
        option=TweakOption(
            name="enabled",
            label="Disable LLMNR",
            type="checkbox",
            default=False,
            description="Reduces LAN broadcast noise and a known credential-leak vector"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows NT\DNSClient",
                value_name="EnableMulticast",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="net_disable_smb1_client",
        name="Disable SMB1 Client",
        category=TweakCategory.NETWORK,
        description="Disable the legacy SMB1 file-sharing client",
        option=TweakOption(
            name="enabled",
            label="Disable SMB1",
            type="checkbox",
            default=False,
            description="SMB1 is insecure and disabled by default on modern Windows"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\mrxsmb10",
                value_name="Start",
                value_type=winreg.REG_DWORD,
                enabled_value=4,
                disabled_value=2
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="net_disable_wifi_sense",
        name="Disable Wi-Fi Sense",
        category=TweakCategory.NETWORK,
        description="Stop Windows from auto-connecting to suggested networks",
        option=TweakOption(
            name="enabled",
            label="Disable Wi-Fi Sense",
            type="checkbox",
            default=False,
            description="Privacy/safety tweak: don't auto-share or auto-connect"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\WlanSvc\AnqpCache",
                value_name="OsuRegistrationStatus",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="net_disable_remote_assistance",
        name="Disable Remote Assistance",
        category=TweakCategory.NETWORK,
        description="Block Remote Assistance invitations and offers",
        option=TweakOption(
            name="enabled",
            label="Disable Remote Assistance",
            type="checkbox",
            default=False,
            description="Stops both invitation and offer-based Remote Assistance"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Remote Assistance",
                value_name="fAllowToGetHelp",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="net_disable_rdp",
        name="Disable Remote Desktop",
        category=TweakCategory.NETWORK,
        description="Refuse all incoming Remote Desktop connections",
        option=TweakOption(
            name="enabled",
            label="Disable Remote Desktop",
            type="checkbox",
            default=True,
            description="Sets fDenyTSConnections=1 to block RDP"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Terminal Server",
                value_name="fDenyTSConnections",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="net_disable_teredo",
        name="Disable Teredo Tunneling",
        category=TweakCategory.NETWORK,
        description="Disable IPv6 Teredo tunneling adapter",
        option=TweakOption(
            name="enabled",
            label="Disable Teredo",
            type="checkbox",
            default=False,
            description="Removes the IPv6-over-IPv4 NAT traversal adapter"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\Tcpip6\Parameters",
                value_name="DisabledComponents",
                value_type=winreg.REG_DWORD,
                enabled_value=0x01,
                disabled_value=0
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="net_disable_netbios_release",
        name="Disable NetBIOS Name Release",
        category=TweakCategory.NETWORK,
        description="Ignore NetBIOS name-release requests from rogue hosts",
        option=TweakOption(
            name="enabled",
            label="Disable NetBIOS name release",
            type="checkbox",
            default=False,
            description="Hardens against NetBIOS denial-of-service attacks"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\Netbt\Parameters",
                value_name="NoNameReleaseOnDemand",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="net_disable_link_local",
        name="Disable Link-Local Auto-IP",
        category=TweakCategory.NETWORK,
        description="Disable APIPA 169.254.x.x fallback addressing",
        option=TweakOption(
            name="enabled",
            label="Disable APIPA",
            type="checkbox",
            default=False,
            description="Prevents Windows from assigning a 169.254 address when DHCP fails"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                value_name="IPAutoconfigurationEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="net_disable_nagle",
        name="Disable Nagle Algorithm",
        category=TweakCategory.NETWORK,
        description="Disable TCP Nagle algorithm for lower socket latency (games, RDP, SSH)",
        option=TweakOption(
            name="enabled",
            label="Disable Nagle algorithm",
            type="checkbox",
            default=False,
            description="Sets TCP_NODELAY system-wide; reduces buffering delay at the cost of slightly more packets"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                value_name="TcpNoDelay",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="net_qos_reserve",
        name="Disable QoS Bandwidth Reserve",
        category=TweakCategory.NETWORK,
        description="Remove the 20% bandwidth reserve held by QoS Packet Scheduler",
        option=TweakOption(
            name="enabled",
            label="Remove QoS bandwidth reserve",
            type="checkbox",
            default=False,
            description="Sets NonBestEffortLimit to 0; reclaims the reserved 20% of bandwidth"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows\Psched",
                value_name="NonBestEffortLimit",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=20
            )
        ]
    ),
    Tweak(
        id="net_dns_max_ttl",
        name="DNS Cache Max TTL",
        category=TweakCategory.NETWORK,
        description="Cap how long DNS entries are cached (seconds)",
        option=TweakOption(
            name="ttl",
            label="Max TTL (seconds)",
            type="spinbox",
            default=86400,
            description="Lower values force fresher lookups; 3600 is a good balance",
            min_value=60,
            max_value=86400
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\Dnscache\Parameters",
                value_name="MaxCacheTtl",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="net_disable_wpad",
        name="Disable WPAD (Web Proxy Auto-Discovery)",
        category=TweakCategory.NETWORK,
        description="Disable the WinHTTP Auto-Proxy service to prevent WPAD attacks",
        option=TweakOption(
            name="enabled",
            label="Disable WPAD service",
            type="checkbox",
            default=False,
            description="Stops automatic proxy discovery; useful on untrusted networks"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\WinHttpAutoProxySvc",
                value_name="Start",
                value_type=winreg.REG_DWORD,
                enabled_value=4,
                disabled_value=3
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="net_tcp_1323",
        name="Enable RFC 1323 TCP Extensions",
        category=TweakCategory.NETWORK,
        description="Enable TCP window scaling and timestamps for high-bandwidth/high-latency links",
        option=TweakOption(
            name="enabled",
            label="Enable RFC 1323 extensions",
            type="checkbox",
            default=False,
            description="Enables large TCP windows and timestamps; helps on fast WAN connections"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                value_name="Tcp1323Opts",
                value_type=winreg.REG_DWORD,
                enabled_value=3,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="net_smb_no_throttle",
        name="Disable SMB Bandwidth Throttling",
        category=TweakCategory.NETWORK,
        description="Allow SMB file transfers to use full available bandwidth",
        option=TweakOption(
            name="enabled",
            label="Disable SMB bandwidth throttle",
            type="checkbox",
            default=False,
            description="SMB client will no longer self-throttle to be 'polite' on shared links"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters",
                value_name="DisableBandwidthThrottling",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="net_disable_nbt_broadcast",
        name="Disable NetBIOS Broadcast Name Resolution",
        category=TweakCategory.NETWORK,
        description="Set NetBIOS node type to P-node — no LAN broadcast for name lookups",
        option=TweakOption(
            name="enabled",
            label="Disable NetBIOS broadcasts",
            type="checkbox",
            default=False,
            description="P-node: use WINS/DNS only. Reduces LAN chatter and credential-leak risk"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\NetBT\Parameters",
                value_name="NodeType",
                value_type=winreg.REG_DWORD,
                enabled_value=2,
                disabled_value=8
            )
        ]
    ),
    Tweak(
        id="net_disable_task_offload",
        name="Disable TCP Task Offloading",
        category=TweakCategory.NETWORK,
        description="Disable hardware TCP/IP offloading (fixes rare NIC driver issues)",
        option=TweakOption(
            name="enabled",
            label="Disable TCP task offloading",
            type="checkbox",
            default=False,
            description="Forces software TCP processing; can fix dropped packet issues with some NICs"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                value_name="DisableTaskOffload",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="net_dns_no_devolution",
        name="Disable DNS Name Devolution",
        category=TweakCategory.NETWORK,
        description="Prevent DNS from appending domain suffixes to short hostnames",
        option=TweakOption(
            name="enabled",
            label="Disable DNS devolution",
            type="checkbox",
            default=False,
            description="Stops Windows from trying 'host.corp.com' when you type 'host' — speeds up resolution"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows NT\DNSClient",
                value_name="UseDomainNameDevolution",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="net_disable_metered_updates",
        name="Treat All Networks as Non-Metered",
        category=TweakCategory.NETWORK,
        description="Force Windows to never treat the connection as metered",
        option=TweakOption(
            name="enabled",
            label="Disable metered behavior",
            type="checkbox",
            default=False,
            description="Useful if Windows keeps deferring updates because it thinks you're on cellular"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\DefaultMediaCost",
                value_name="3G",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=2
            )
        ]
    ),
]

# =============================================================================
# POWER & BATTERY TWEAKS
# =============================================================================

POWER_TWEAKS = [
    Tweak(
        id="power_disable_hibernate",
        name="Disable Hibernation",
        category=TweakCategory.POWER,
        description="Disable hibernation and free up disk space (deletes hiberfil.sys)",
        option=TweakOption(
            name="enabled",
            label="Disable hibernation",
            type="checkbox",
            default=False,
            description="Reclaims several GB of disk used by hiberfil.sys"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Power",
                value_name="HibernateEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="power_disable_fast_startup",
        name="Disable Fast Startup",
        category=TweakCategory.POWER,
        description="Disable hybrid-shutdown 'Fast Startup' for cleaner boots",
        option=TweakOption(
            name="enabled",
            label="Disable Fast Startup",
            type="checkbox",
            default=False,
            description="Recommended on dual-boot systems and after hardware changes"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Session Manager\Power",
                value_name="HiberbootEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="power_show_hibernate_menu",
        name="Show 'Hibernate' in Power Menu",
        category=TweakCategory.POWER,
        description="Add a Hibernate entry to the Start menu power flyout",
        option=TweakOption(
            name="enabled",
            label="Show Hibernate option",
            type="checkbox",
            default=False,
            description="Requires hibernation to be enabled to actually work"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FlyoutMenuSettings",
                value_name="ShowHibernateOption",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="power_show_sleep_menu",
        name="Show 'Sleep' in Power Menu",
        category=TweakCategory.POWER,
        description="Add a Sleep entry to the Start menu power flyout",
        option=TweakOption(
            name="enabled",
            label="Show Sleep option",
            type="checkbox",
            default=True,
            description="Standard Sleep button in the power flyout"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FlyoutMenuSettings",
                value_name="ShowSleepOption",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="power_show_lock_menu",
        name="Show 'Lock' in Power Menu",
        category=TweakCategory.POWER,
        description="Add a Lock entry to the Start menu power flyout",
        option=TweakOption(
            name="enabled",
            label="Show Lock option",
            type="checkbox",
            default=False,
            description="Lock without signing out, from the same flyout as power"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FlyoutMenuSettings",
                value_name="ShowLockOption",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="power_disable_throttling",
        name="Disable CPU Power Throttling",
        category=TweakCategory.POWER,
        description="Stop Windows from throttling background processes",
        option=TweakOption(
            name="enabled",
            label="Disable power throttling",
            type="checkbox",
            default=False,
            description="Useful for compute jobs you don't want demoted in the background"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Power\PowerThrottling",
                value_name="PowerThrottlingOff",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="power_modern_standby_off",
        name="Disable Modern Standby Network",
        category=TweakCategory.POWER,
        description="Drop network connections during connected standby",
        option=TweakOption(
            name="enabled",
            label="Disable network during standby",
            type="checkbox",
            default=False,
            description="Saves battery on laptops by not waking radios for notifications"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Power\PowerSettings\F15576E8-98B7-4186-B944-EAFA664402D9",
                value_name="ACSettingIndex",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="power_unlock_minimum_state",
        name="Show Hidden Power Options in Control Panel",
        category=TweakCategory.POWER,
        description="Unhide every advanced power-plan setting in Control Panel",
        option=TweakOption(
            name="enabled",
            label="Show hidden power settings",
            type="checkbox",
            default=False,
            description="Reveals hidden options like CPU min/max state, lid actions, and more"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Power\PowerSettings\54533251-82BE-4824-96C1-47B60B740D00\893DEE8E-2BEF-41E0-89C6-B55D0929964C",
                value_name="Attributes",
                value_type=winreg.REG_DWORD,
                enabled_value=2,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="power_usb_suspend",
        name="Disable USB Selective Suspend",
        category=TweakCategory.POWER,
        description="Prevent Windows from powering down USB devices to save energy",
        option=TweakOption(
            name="enabled",
            label="Disable USB selective suspend",
            type="checkbox",
            default=False,
            description="Stops USB devices (headsets, controllers, hubs) from dropping out randomly"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\USB",
                value_name="DisableSelectiveSuspend",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="power_screensaver_off",
        name="Disable Screen Saver",
        category=TweakCategory.POWER,
        description="Permanently disable the Windows screen saver",
        option=TweakOption(
            name="enabled",
            label="Disable screen saver",
            type="checkbox",
            default=False,
            description="Stops the screen saver from activating regardless of idle time"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Desktop",
                value_name="ScreenSaveActive",
                value_type=winreg.REG_SZ,
                enabled_value="0",
                disabled_value="1"
            )
        ]
    ),
    Tweak(
        id="power_away_mode",
        name="Disable Away Mode",
        category=TweakCategory.POWER,
        description="Disable Away Mode (server-style always-on background processing)",
        option=TweakOption(
            name="enabled",
            label="Disable Away Mode",
            type="checkbox",
            default=False,
            description="Away Mode keeps the display off but CPU/network active; disable on desktops that should sleep"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Session Manager\Power",
                value_name="AwayModeEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="power_throttle_off",
        name="Disable Windows Power Throttling",
        category=TweakCategory.POWER,
        description="Disable the EcoQoS / Power Throttling feature that reduces background app performance",
        option=TweakOption(
            name="enabled",
            label="Disable power throttling",
            type="checkbox",
            default=False,
            description="Prevents Windows from throttling background processes; trades battery for responsiveness"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Power\PowerThrottling",
                value_name="PowerThrottlingOff",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="power_ndu_disable",
        name="Disable NDU Network Data Usage Monitor",
        category=TweakCategory.POWER,
        description="Disable the Ndu.sys kernel driver that tracks per-app network usage",
        option=TweakOption(
            name="enabled",
            label="Disable NDU service",
            type="checkbox",
            default=False,
            description="NDU can cause high RAM/CPU on some systems; disabling it is safe for most users"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\Ndu",
                value_name="Start",
                value_type=winreg.REG_DWORD,
                enabled_value=4,
                disabled_value=2
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="power_sleep_study",
        name="Disable SleepStudy",
        category=TweakCategory.POWER,
        description="Disable the SleepStudy background power-analysis process",
        option=TweakOption(
            name="enabled",
            label="Disable SleepStudy",
            type="checkbox",
            default=False,
            description="SleepStudy logs each sleep cycle for energy reports; disable to reduce disk writes"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Session Manager\Power",
                value_name="SleepStudyDisabled",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="power_write_cache",
        name="Enable Disk Write-Back Cache",
        category=TweakCategory.POWER,
        description="Enable write-back caching on disk controllers for better throughput",
        option=TweakOption(
            name="enabled",
            label="Enable disk write-back cache",
            type="checkbox",
            default=False,
            description="Batches disk writes in RAM buffer; faster but data may be lost on sudden power cut"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\disk",
                value_name="UserWriteCacheSetting",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="power_energy_estimation",
        name="Disable Energy Estimation",
        category=TweakCategory.POWER,
        description="Disable the kernel-level energy estimation sampling process",
        option=TweakOption(
            name="enabled",
            label="Disable energy estimation",
            type="checkbox",
            default=False,
            description="Reduces constant background CPU sampling used for battery predictions"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Power",
                value_name="EnergyEstimationEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
]

# =============================================================================
# GAMING TWEAKS
# =============================================================================

GAMING_TWEAKS = [
    Tweak(
        id="game_disable_gamebar",
        name="Disable Game Bar",
        category=TweakCategory.GAMING,
        description="Disable the Xbox Game Bar overlay (Win+G)",
        option=TweakOption(
            name="enabled",
            label="Disable Game Bar",
            type="checkbox",
            default=False,
            description="Frees up the Win+G hotkey and reduces overhead"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\GameBar",
                value_name="UseNexusForGameBarEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="game_disable_gamemode",
        name="Disable Game Mode",
        category=TweakCategory.GAMING,
        description="Disable Windows Game Mode auto-detection",
        option=TweakOption(
            name="enabled",
            label="Disable Game Mode",
            type="checkbox",
            default=False,
            description="Some users see better consistency with Game Mode disabled"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\GameBar",
                value_name="AllowAutoGameMode",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="game_hwsch",
        name="Hardware-Accelerated GPU Scheduling",
        category=TweakCategory.GAMING,
        description="Let the GPU manage its own video memory scheduling",
        option=TweakOption(
            name="enabled",
            label="Enable HW GPU Scheduling",
            type="checkbox",
            default=False,
            description="Reduces latency on supported GPUs (RTX 1000+, RX 5000+)"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers",
                value_name="HwSchMode",
                value_type=winreg.REG_DWORD,
                enabled_value=2,
                disabled_value=1
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="game_disable_fso",
        name="Disable Fullscreen Optimizations",
        category=TweakCategory.GAMING,
        description="Disable Windows DXGI fullscreen optimizations globally",
        option=TweakOption(
            name="enabled",
            label="Disable fullscreen optimizations",
            type="checkbox",
            default=False,
            description="Forces exclusive fullscreen for older DX9/11 titles"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"System\GameConfigStore",
                value_name="GameDVR_FSEBehaviorMode",
                value_type=winreg.REG_DWORD,
                enabled_value=2,
                disabled_value=0
            ),
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"System\GameConfigStore",
                value_name="GameDVR_DXGIHonorFSEWindowsCompatible",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            ),
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"System\GameConfigStore",
                value_name="GameDVR_HonorUserFSEBehaviorMode",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="game_no_mouse_accel",
        name="Disable Mouse Acceleration",
        category=TweakCategory.GAMING,
        description="Turn off Windows 'Enhance pointer precision' for raw mouse input",
        option=TweakOption(
            name="enabled",
            label="Disable mouse acceleration",
            type="checkbox",
            default=False,
            description="Critical for FPS games — provides 1:1 mouse movement"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Mouse",
                value_name="MouseSpeed",
                value_type=winreg.REG_SZ,
                enabled_value="0",
                disabled_value="1"
            ),
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Mouse",
                value_name="MouseThreshold1",
                value_type=winreg.REG_SZ,
                enabled_value="0",
                disabled_value="6"
            ),
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Mouse",
                value_name="MouseThreshold2",
                value_type=winreg.REG_SZ,
                enabled_value="0",
                disabled_value="10"
            )
        ]
    ),
    Tweak(
        id="game_no_net_throttle",
        name="Disable Network Throttling",
        category=TweakCategory.GAMING,
        description="Remove Windows' multimedia network throttling cap",
        option=TweakOption(
            name="enabled",
            label="Disable network throttling",
            type="checkbox",
            default=False,
            description="Useful when streaming or playing competitive online games"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile",
                value_name="NetworkThrottlingIndex",
                value_type=winreg.REG_DWORD,
                enabled_value=0xFFFFFFFF,
                disabled_value=10
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="game_responsiveness",
        name="Maximize System Responsiveness",
        category=TweakCategory.GAMING,
        description="Reserve 0% of CPU for low-priority work (full CPU for foreground)",
        option=TweakOption(
            name="enabled",
            label="Boost foreground priority",
            type="checkbox",
            default=False,
            description="Sets SystemResponsiveness to 0 instead of the default 20"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile",
                value_name="SystemResponsiveness",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=20
            )
        ]
    ),
    Tweak(
        id="game_disable_dvr",
        name="Disable Xbox Game DVR",
        category=TweakCategory.GAMING,
        description="Disable background recording / Xbox DVR completely",
        option=TweakOption(
            name="enabled",
            label="Disable Game DVR",
            type="checkbox",
            default=False,
            description="Removes the always-on background recorder"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows\GameDVR",
                value_name="AllowGameDVR",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="game_disable_vbs",
        name="Disable Memory Integrity (VBS)",
        category=TweakCategory.GAMING,
        description="Disable Virtualization-Based Security / HVCI",
        option=TweakOption(
            name="enabled",
            label="Disable VBS / Memory Integrity",
            type="checkbox",
            default=False,
            description="VBS adds 5-15% overhead in some games. Reduces security — use with care."
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity",
                value_name="Enabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="game_gpu_priority",
        name="Boost GPU Priority for Games",
        category=TweakCategory.GAMING,
        description="Set high GPU priority on the multimedia 'Games' task",
        option=TweakOption(
            name="enabled",
            label="Boost game GPU priority",
            type="checkbox",
            default=False,
            description="Sets GPU Priority=8 (max) and Priority=6 on the Games scheduler class"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
                value_name="GPU Priority",
                value_type=winreg.REG_DWORD,
                enabled_value=8,
                disabled_value=2
            ),
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
                value_name="Priority",
                value_type=winreg.REG_DWORD,
                enabled_value=6,
                disabled_value=2
            )
        ]
    ),
    Tweak(
        id="game_disable_mpo",
        name="Disable Multi-Plane Overlay (MPO)",
        category=TweakCategory.GAMING,
        description="Disable MPO to fix stutters and black screens on some NVIDIA/AMD GPUs",
        option=TweakOption(
            name="enabled",
            label="Disable Multi-Plane Overlay",
            type="checkbox",
            default=False,
            description="Known to fix micro-stutters on Ryzen + NVIDIA setups"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\Dwm",
                value_name="OverlayTestMode",
                value_type=winreg.REG_DWORD,
                enabled_value=5,
                disabled_value=None
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="game_disable_fse_behaviour",
        name="Force Fullscreen Optimizations Off",
        category=TweakCategory.GAMING,
        description="Globally disable fullscreen optimizations so games run in true exclusive fullscreen",
        option=TweakOption(
            name="enabled",
            label="Disable fullscreen optimizations globally",
            type="checkbox",
            default=False,
            description="Can reduce input lag and tearing in games that use exclusive fullscreen"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"System\GameConfigStore",
                value_name="GameDVR_FSEBehavior",
                value_type=winreg.REG_DWORD,
                enabled_value=2,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="game_shader_cache",
        name="Enable DirectX Shader Cache",
        category=TweakCategory.GAMING,
        description="Allow DirectX to cache compiled shaders so games compile them only once",
        option=TweakOption(
            name="enabled",
            label="Enable shader cache",
            type="checkbox",
            default=False,
            description="Reduces shader stutter on subsequent game launches"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\DirectX",
                value_name="D3D12_CACHE_DISABLE",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="game_raw_input",
        name="Disable Pointer Precision (Raw Input)",
        category=TweakCategory.GAMING,
        description="Turn off mouse pointer precision (acceleration) for 1:1 raw mouse movement",
        option=TweakOption(
            name="enabled",
            label="Disable pointer precision (raw input)",
            type="checkbox",
            default=False,
            description="Essential for FPS games — mouse moves exactly as far as you physically move it"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Mouse",
                value_name="MouseSpeed",
                value_type=winreg.REG_SZ,
                enabled_value="0",
                disabled_value="1"
            ),
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Mouse",
                value_name="MouseThreshold1",
                value_type=winreg.REG_SZ,
                enabled_value="0",
                disabled_value="6"
            ),
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Mouse",
                value_name="MouseThreshold2",
                value_type=winreg.REG_SZ,
                enabled_value="0",
                disabled_value="10"
            ),
        ],
        requires_logoff=True
    ),
    Tweak(
        id="game_high_perf_power",
        name="Use High Performance Power Plan",
        category=TweakCategory.GAMING,
        description="Switch Windows to the High Performance power plan to prevent CPU clock throttling",
        option=TweakOption(
            name="enabled",
            label="Enable High Performance plan",
            type="checkbox",
            default=False,
            description="Keeps CPU at max frequency — eliminates latency spikes caused by clock stepping"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Power\User\PowerSchemes",
                value_name="ActivePowerScheme",
                value_type=winreg.REG_SZ,
                enabled_value="8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c",
                disabled_value="381b4222-f694-41f0-9685-ff5bb260df2e"
            )
        ]
    ),
    Tweak(
        id="game_timer_no_lazy",
        name="Enable MMCSS NoLazyMode Timer",
        category=TweakCategory.GAMING,
        description="Disable lazy timer coalescing in the Multimedia Class Scheduler for lower latency",
        option=TweakOption(
            name="enabled",
            label="Enable NoLazyMode",
            type="checkbox",
            default=False,
            description="Forces immediate timer delivery instead of coalescing; reduces input lag in competitive games"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile",
                value_name="NoLazyMode",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="game_xbl_auth_disable",
        name="Disable Xbox Live Auth Manager",
        category=TweakCategory.GAMING,
        description="Stop the XblAuthManager background service for non-Xbox-Live users",
        option=TweakOption(
            name="enabled",
            label="Disable XblAuthManager service",
            type="checkbox",
            default=False,
            description="Frees RAM/CPU for users who don't use Xbox Live sign-in"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\XblAuthManager",
                value_name="Start",
                value_type=winreg.REG_DWORD,
                enabled_value=4,
                disabled_value=2
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="game_xbl_game_save",
        name="Disable Xbox Live Game Save",
        category=TweakCategory.GAMING,
        description="Stop the Xbox Live cloud-save sync service",
        option=TweakOption(
            name="enabled",
            label="Disable XblGameSave service",
            type="checkbox",
            default=False,
            description="Saves RAM/disk; only affects Xbox-enabled titles that use cloud saves"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\XblGameSave",
                value_name="Start",
                value_type=winreg.REG_DWORD,
                enabled_value=4,
                disabled_value=2
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="game_spectre_disable",
        name="Disable Spectre/Meltdown Mitigations",
        category=TweakCategory.GAMING,
        description="Remove CPU vulnerability mitigations — significant performance boost but reduced security",
        option=TweakOption(
            name="enabled",
            label="Disable Spectre/Meltdown mitigations",
            type="checkbox",
            default=False,
            description="⚠ Security trade-off: gains 5–15% CPU performance but exposes CPU timing vulnerabilities"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management",
                value_name="FeatureSettingsOverride",
                value_type=winreg.REG_DWORD,
                enabled_value=3,
                disabled_value=0
            ),
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management",
                value_name="FeatureSettingsOverrideMask",
                value_type=winreg.REG_DWORD,
                enabled_value=3,
                disabled_value=3
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="game_schedule_sfio",
        name="Set Games Task SFIO Priority to High",
        category=TweakCategory.GAMING,
        description="Boost the MMCSS Games task's Scheduled I/O priority",
        option=TweakOption(
            name="priority",
            label="SFIO Priority",
            type="dropdown",
            default="Normal",
            description="High gives game threads priority for storage I/O scheduling",
            choices=[
                ("High", "High"),
                ("Normal", "Normal"),
                ("Low", "Low")
            ]
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
                value_name="SFIO Priority",
                value_type=winreg.REG_SZ,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="game_xbgm_disable",
        name="Disable Xbox Game Monitoring Service",
        category=TweakCategory.GAMING,
        description="Stop the xbgm background service used for Xbox Game Streaming",
        option=TweakOption(
            name="enabled",
            label="Disable Xbox Game Monitoring",
            type="checkbox",
            default=False,
            description="Frees resources on systems that don't use Xbox casting or streaming"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\xbgm",
                value_name="Start",
                value_type=winreg.REG_DWORD,
                enabled_value=4,
                disabled_value=3
            )
        ],
        requires_restart=True
    ),
]

# =============================================================================
# SECURITY & DEFENDER TWEAKS
# =============================================================================

SECURITY_TWEAKS = [
    Tweak(
        id="sec_uac_never",
        name="Set UAC to Never Notify",
        category=TweakCategory.SECURITY,
        description="Lower UAC to its quietest level (still leaves LUA enabled)",
        option=TweakOption(
            name="enabled",
            label="Never notify",
            type="checkbox",
            default=False,
            description="Reduces UAC popups. Less secure — disables PromptOnSecureDesktop"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System",
                value_name="ConsentPromptBehaviorAdmin",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=5
            ),
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System",
                value_name="PromptOnSecureDesktop",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="sec_smartscreen_apps",
        name="Disable SmartScreen for Apps",
        category=TweakCategory.SECURITY,
        description="Stop SmartScreen from checking downloaded executables",
        option=TweakOption(
            name="enabled",
            label="Disable SmartScreen (apps)",
            type="checkbox",
            default=False,
            description="Removes the 'Windows protected your PC' prompt"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer",
                value_name="SmartScreenEnabled",
                value_type=winreg.REG_SZ,
                enabled_value="Off",
                disabled_value="Warn"
            )
        ]
    ),
    Tweak(
        id="sec_smartscreen_edge",
        name="Disable SmartScreen for Edge",
        category=TweakCategory.SECURITY,
        description="Disable Microsoft Edge's SmartScreen filter",
        option=TweakOption(
            name="enabled",
            label="Disable SmartScreen (Edge)",
            type="checkbox",
            default=False,
            description="Stops Edge from checking visited URLs against SmartScreen"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Edge\SmartScreenEnabled",
                value_name="(Default)",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="sec_defender_realtime",
        name="Disable Defender Real-time Protection",
        category=TweakCategory.SECURITY,
        description="Turn off Microsoft Defender real-time scanning",
        option=TweakOption(
            name="enabled",
            label="Disable real-time protection",
            type="checkbox",
            default=False,
            description="Tamper Protection may revert this — disable it manually first in Settings"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection",
                value_name="DisableRealtimeMonitoring",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="sec_defender_cloud",
        name="Disable Defender Cloud Protection",
        category=TweakCategory.SECURITY,
        description="Disable cloud-delivered protection (MAPS reporting)",
        option=TweakOption(
            name="enabled",
            label="Disable cloud protection",
            type="checkbox",
            default=False,
            description="Stops Defender from sending file telemetry to Microsoft cloud"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows Defender\Spynet",
                value_name="SpyNetReporting",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=2
            )
        ]
    ),
    Tweak(
        id="sec_defender_samples",
        name="Disable Defender Sample Submission",
        category=TweakCategory.SECURITY,
        description="Stop Defender from auto-uploading suspicious samples",
        option=TweakOption(
            name="enabled",
            label="Disable sample submission",
            type="checkbox",
            default=False,
            description="Defender will never auto-send file samples to Microsoft"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows Defender\Spynet",
                value_name="SubmitSamplesConsent",
                value_type=winreg.REG_DWORD,
                enabled_value=2,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="sec_disable_autorun",
        name="Disable AutoRun for All Drives",
        category=TweakCategory.SECURITY,
        description="Block AutoRun on USB sticks, optical media and network drives",
        option=TweakOption(
            name="enabled",
            label="Disable AutoRun",
            type="checkbox",
            default=False,
            description="Recommended security tweak — prevents drive-borne malware auto-execution"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer",
                value_name="NoDriveTypeAutoRun",
                value_type=winreg.REG_DWORD,
                enabled_value=255,
                disabled_value=145
            )
        ]
    ),
    Tweak(
        id="sec_disable_autoplay",
        name="Disable AutoPlay",
        category=TweakCategory.SECURITY,
        description="Disable the AutoPlay prompt that asks what to do with new drives",
        option=TweakOption(
            name="enabled",
            label="Disable AutoPlay",
            type="checkbox",
            default=False,
            description="No prompt when inserting USB sticks or memory cards"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\AutoplayHandlers",
                value_name="DisableAutoplay",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="sec_nolmhash",
        name="Disable LM Password Hash Storage",
        category=TweakCategory.SECURITY,
        description="Prevent Windows from storing the weak LAN Manager password hash",
        option=TweakOption(
            name="enabled",
            label="Disable LM hash storage",
            type="checkbox",
            default=False,
            description="LM hashes are trivially cracked; disabling forces NTLM/Kerberos only"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Lsa",
                value_name="NoLMHash",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="sec_ntlmv2_only",
        name="Force NTLMv2 Authentication Only",
        category=TweakCategory.SECURITY,
        description="Set LmCompatibilityLevel=5 to refuse LM/NTLMv1 and send NTLMv2 only",
        option=TweakOption(
            name="enabled",
            label="Force NTLMv2 only",
            type="checkbox",
            default=False,
            description="Prevents downgrade attacks; may break auth to very old (pre-2000) servers"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Lsa",
                value_name="LmCompatibilityLevel",
                value_type=winreg.REG_DWORD,
                enabled_value=5,
                disabled_value=3
            )
        ]
    ),
    Tweak(
        id="sec_disable_wer",
        name="Disable Windows Error Reporting Service",
        category=TweakCategory.SECURITY,
        description="Stop the WerSvc service from collecting and sending crash reports",
        option=TweakOption(
            name="enabled",
            label="Disable Windows Error Reporting",
            type="checkbox",
            default=False,
            description="Crash data is no longer uploaded to Microsoft; saves disk and bandwidth"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\WerSvc",
                value_name="Start",
                value_type=winreg.REG_DWORD,
                enabled_value=4,
                disabled_value=3
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="sec_disable_admin_shares",
        name="Disable Default Admin Shares (C$, ADMIN$)",
        category=TweakCategory.SECURITY,
        description="Disable automatic hidden administrative shares on workstations",
        option=TweakOption(
            name="enabled",
            label="Disable admin shares",
            type="checkbox",
            default=False,
            description="Reduces lateral movement risk; remote admin tools that rely on C$ will stop working"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters",
                value_name="AutoShareWks",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="sec_disable_wsh",
        name="Disable Windows Script Host",
        category=TweakCategory.SECURITY,
        description="Block execution of .vbs, .js, .wsf and other WSH scripts",
        option=TweakOption(
            name="enabled",
            label="Disable Windows Script Host",
            type="checkbox",
            default=False,
            description="Stops most script-based malware from running; may break some legitimate automation"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows Script Host\Settings",
                value_name="Enabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="sec_smb_signing",
        name="Require SMB Packet Signing",
        category=TweakCategory.SECURITY,
        description="Mandate SMB signing on the workstation client to prevent man-in-the-middle attacks",
        option=TweakOption(
            name="enabled",
            label="Require SMB signing",
            type="checkbox",
            default=False,
            description="Prevents SMB relay attacks; negligible performance impact on modern hardware"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters",
                value_name="RequireSecuritySignature",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="sec_rdp_nla",
        name="Require NLA for Remote Desktop",
        category=TweakCategory.SECURITY,
        description="Force Network Level Authentication before the RDP login screen is shown",
        option=TweakOption(
            name="enabled",
            label="Require NLA for RDP",
            type="checkbox",
            default=False,
            description="Prevents unauthenticated users from reaching the RDP login screen; stops CredSSP exploits"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp",
                value_name="UserAuthentication",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="sec_disable_remote_registry",
        name="Disable Remote Registry Service",
        category=TweakCategory.SECURITY,
        description="Stop the Remote Registry service so the registry can't be modified over the network",
        option=TweakOption(
            name="enabled",
            label="Disable Remote Registry",
            type="checkbox",
            default=False,
            description="Blocks remote registry editing tools; low risk to disable on personal machines"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\RemoteRegistry",
                value_name="Start",
                value_type=winreg.REG_DWORD,
                enabled_value=4,
                disabled_value=2
            )
        ],
        requires_restart=True
    ),
]

# =============================================================================
# APPS & SERVICES TWEAKS
# =============================================================================

APPS_SERVICES_TWEAKS = [
    Tweak(
        id="app_no_onedrive_autostart",
        name="Disable OneDrive Auto-start",
        category=TweakCategory.APPS_SERVICES,
        description="Stop OneDrive from launching at sign-in",
        option=TweakOption(
            name="enabled",
            label="Disable OneDrive auto-start",
            type="checkbox",
            default=False,
            description="OneDrive stays installed but won't auto-launch"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows\OneDrive",
                value_name="DisableFileSyncNGSC",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="app_no_cortana_startup",
        name="Disable Cortana Auto-start",
        category=TweakCategory.APPS_SERVICES,
        description="Stop Cortana from starting in the background",
        option=TweakOption(
            name="enabled",
            label="Disable Cortana auto-start",
            type="checkbox",
            default=False,
            description="Pairs well with the privacy 'Disable Cortana' toggle"
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
        id="app_no_store_autoupdate",
        name="Disable Microsoft Store Auto-update",
        category=TweakCategory.APPS_SERVICES,
        description="Stop the Store from auto-updating apps",
        option=TweakOption(
            name="enabled",
            label="Disable Store auto-update",
            type="checkbox",
            default=False,
            description="You can still manually check for updates in the Store app"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\WindowsStore",
                value_name="AutoDownload",
                value_type=winreg.REG_DWORD,
                enabled_value=2,
                disabled_value=4
            )
        ]
    ),
    Tweak(
        id="app_disable_search_index",
        name="Disable Windows Search Indexing Service",
        category=TweakCategory.APPS_SERVICES,
        description="Stop the WSearch indexing service",
        option=TweakOption(
            name="enabled",
            label="Disable WSearch service",
            type="checkbox",
            default=False,
            description="Saves CPU/disk; Start menu search becomes slower"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\WSearch",
                value_name="Start",
                value_type=winreg.REG_DWORD,
                enabled_value=4,
                disabled_value=2
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="app_disable_sysmain",
        name="Disable SysMain (Superfetch)",
        category=TweakCategory.APPS_SERVICES,
        description="Disable the SysMain / Superfetch prefetch service",
        option=TweakOption(
            name="enabled",
            label="Disable SysMain",
            type="checkbox",
            default=False,
            description="Helpful on SSDs where prefetch hurts more than it helps"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\SysMain",
                value_name="Start",
                value_type=winreg.REG_DWORD,
                enabled_value=4,
                disabled_value=2
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="app_disable_spooler",
        name="Disable Print Spooler",
        category=TweakCategory.APPS_SERVICES,
        description="Disable the Print Spooler service (PrintNightmare hardening)",
        option=TweakOption(
            name="enabled",
            label="Disable Print Spooler",
            type="checkbox",
            default=False,
            description="Disables all printing — only enable if you don't print"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\Spooler",
                value_name="Start",
                value_type=winreg.REG_DWORD,
                enabled_value=4,
                disabled_value=2
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="app_disable_diagtrack",
        name="Disable Connected User Experiences (DiagTrack)",
        category=TweakCategory.APPS_SERVICES,
        description="Disable the DiagTrack telemetry service",
        option=TweakOption(
            name="enabled",
            label="Disable DiagTrack",
            type="checkbox",
            default=False,
            description="Major telemetry source. Pair with privacy_telemetry"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\DiagTrack",
                value_name="Start",
                value_type=winreg.REG_DWORD,
                enabled_value=4,
                disabled_value=2
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="app_no_background_apps",
        name="Disable Background Apps",
        category=TweakCategory.APPS_SERVICES,
        description="Block UWP / packaged apps from running in the background",
        option=TweakOption(
            name="enabled",
            label="Disable background apps",
            type="checkbox",
            default=False,
            description="Saves battery and RAM; disables background notifications from MS Store apps"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications",
                value_name="GlobalUserDisabled",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="app_no_tips",
        name="Disable Windows Tips and Suggestions",
        category=TweakCategory.APPS_SERVICES,
        description="Stop Windows from showing notifications/tips/welcome experience",
        option=TweakOption(
            name="enabled",
            label="Disable tips & suggestions",
            type="checkbox",
            default=False,
            description="Removes the 'Get even more out of Windows' nags"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                value_name="SubscribedContent-338389Enabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            ),
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                value_name="SubscribedContent-310093Enabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="app_no_auto_reboot",
        name="Disable Auto-Restart for Updates",
        category=TweakCategory.APPS_SERVICES,
        description="Prevent Windows Update from restarting while you're signed in",
        option=TweakOption(
            name="enabled",
            label="Disable update auto-restart",
            type="checkbox",
            default=False,
            description="Updates still install — but Windows won't reboot without confirmation"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU",
                value_name="NoAutoRebootWithLoggedOnUsers",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="app_no_silent_promotion",
        name="Disable Silent Promoted App Installs",
        category=TweakCategory.APPS_SERVICES,
        description="Stop Windows from silently auto-installing promoted apps",
        option=TweakOption(
            name="enabled",
            label="Disable silent app installs",
            type="checkbox",
            default=False,
            description="Blocks Candy Crush / Disney / Spotify suggestions auto-installing"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                value_name="SilentInstalledAppsEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            ),
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                value_name="OemPreInstalledAppsEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            ),
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                value_name="PreInstalledAppsEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="app_disable_bing_search",
        name="Disable Bing Search in Start Menu",
        category=TweakCategory.APPS_SERVICES,
        description="Remove Bing web results from the Start Menu search box",
        option=TweakOption(
            name="enabled",
            label="Disable Bing search in Start",
            type="checkbox",
            default=False,
            description="Searches stay local; removes sponsored/web results from Start Menu"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Search",
                value_name="BingSearchEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            ),
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Search",
                value_name="CortanaConsent",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="app_disable_edge_preload",
        name="Disable Microsoft Edge Preload",
        category=TweakCategory.APPS_SERVICES,
        description="Prevent Edge from preloading at Windows startup to save RAM",
        option=TweakOption(
            name="enabled",
            label="Disable Edge startup boost",
            type="checkbox",
            default=False,
            description="Edge will start slightly slower on first launch; saves ~100–200 MB RAM"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Edge",
                value_name="StartupBoostEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="app_no_people_bar",
        name="Disable People Bar on Taskbar",
        category=TweakCategory.APPS_SERVICES,
        description="Remove the People / contacts button from the taskbar",
        option=TweakOption(
            name="enabled",
            label="Disable People Bar",
            type="checkbox",
            default=False,
            description="Hides the People pin from the taskbar (Windows 10)"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\People",
                value_name="PeopleBand",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="app_no_news_interests",
        name="Disable News and Interests Widget",
        category=TweakCategory.APPS_SERVICES,
        description="Hide the Windows Feeds / News and Interests weather widget on the taskbar",
        option=TweakOption(
            name="enabled",
            label="Disable News & Interests",
            type="checkbox",
            default=False,
            description="Removes the taskbar weather/news feed (Windows 10 21H2+)"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows\Windows Feeds",
                value_name="EnableFeeds",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="app_no_feedback_sampling",
        name="Disable Feedback Hub Diagnostic Sampling",
        category=TweakCategory.APPS_SERVICES,
        description="Stop Windows from periodically asking for feedback",
        option=TweakOption(
            name="enabled",
            label="Disable feedback sampling",
            type="checkbox",
            default=False,
            description="Sets frequency to zero so the Feedback Hub never prompts for diagnostics"
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
    Tweak(
        id="app_no_shared_experiences",
        name="Disable Shared Experiences (Cross-Device)",
        category=TweakCategory.APPS_SERVICES,
        description="Disable the Connected Devices Platform used for phone/PC handoff features",
        option=TweakOption(
            name="enabled",
            label="Disable Shared Experiences",
            type="checkbox",
            default=False,
            description="Turns off Near Share, Continue on PC, and phone-link pairing broadcasts"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\CDP",
                value_name="RomeSdkChannelUserAuthzPolicy",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="app_no_windows_ink",
        name="Disable Windows Ink Workspace Button",
        category=TweakCategory.APPS_SERVICES,
        description="Hide the Windows Ink Workspace pen button from the taskbar",
        option=TweakOption(
            name="enabled",
            label="Hide Windows Ink button",
            type="checkbox",
            default=False,
            description="Removes the pen/stylus workspace shortcut for non-tablet users"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\PenWorkspace",
                value_name="PenWorkspaceButtonDesiredVisibility",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="app_no_meet_now",
        name="Disable Meet Now (Skype) Taskbar Button",
        category=TweakCategory.APPS_SERVICES,
        description="Remove the Meet Now / Skype video-call button from the system tray",
        option=TweakOption(
            name="enabled",
            label="Hide Meet Now button",
            type="checkbox",
            default=False,
            description="Cleans up the system tray for users who don't use Skype"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer",
                value_name="HideSCAMeetNow",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
]

# =============================================================================
# DISPLAY TWEAKS
# =============================================================================

DISPLAY_TWEAKS = [
    Tweak(
        id="disp_dpi_scaling_mode",
        name="DPI Scaling Awareness Mode",
        category=TweakCategory.DISPLAY,
        description="Set the system-wide DPI awareness mode for legacy applications",
        option=TweakOption(
            name="mode",
            label="DPI mode",
            type="dropdown",
            default="PerMonitorV2",
            description="PerMonitorV2 is best for multi-monitor setups with different scales",
            choices=[
                ("PerMonitorV2", "Per-Monitor v2 (recommended)"),
                ("PerMonitor", "Per-Monitor v1"),
                ("System", "System DPI"),
                ("Unaware", "DPI Unaware (legacy)")
            ]
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Desktop",
                value_name="DpiScalingVer",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="disp_font_dpi",
        name="Custom Font DPI Override",
        category=TweakCategory.DISPLAY,
        description="Override the system font DPI (dots per inch) used for text sizing",
        option=TweakOption(
            name="dpi",
            label="Font DPI",
            type="spinbox",
            default=96,
            description="96=100%, 120=125%, 144=150%, 192=200%. Requires sign-out.",
            min_value=72,
            max_value=288
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Desktop",
                value_name="LogPixels",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ],
        requires_logoff=True
    ),
    Tweak(
        id="disp_night_light",
        name="Night Light (Blue Light Filter)",
        category=TweakCategory.DISPLAY,
        description="Enable the built-in Night Light blue-light reduction filter",
        option=TweakOption(
            name="enabled",
            label="Enable Night Light",
            type="checkbox",
            default=False,
            description="Warms screen color temperature to reduce eye strain in low-light environments"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\CloudStore\Store\DefaultAccount\Current\default$windows.data.bluelightreduction.bluelightreductionstate\windows.data.bluelightreduction.bluelightreductionstate",
                value_name="Data",
                value_type=winreg.REG_BINARY,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="disp_snap_layout_hover",
        name="Show Snap Layouts on Hover",
        category=TweakCategory.DISPLAY,
        description="Show Snap Layout grid when hovering the maximize button (Windows 11)",
        option=TweakOption(
            name="enabled",
            label="Show Snap Layouts on hover",
            type="checkbox",
            default=True,
            description="Hovering the maximize button reveals the Snap Layout picker"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="EnableSnapAssistFlyout",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="disp_snap_window_suggest",
        name="Snap Window Suggestions",
        category=TweakCategory.DISPLAY,
        description="Show suggested windows to snap alongside the current window",
        option=TweakOption(
            name="enabled",
            label="Enable snap suggestions",
            type="checkbox",
            default=True,
            description="After snapping a window, Windows suggests other windows to fill the remaining space"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="SnapAssist",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="disp_multimon_taskbar",
        name="Show Taskbar on All Monitors",
        category=TweakCategory.DISPLAY,
        description="Display the taskbar on every monitor in a multi-display setup",
        option=TweakOption(
            name="enabled",
            label="Taskbar on all monitors",
            type="checkbox",
            default=True,
            description="Each monitor gets its own taskbar; disable for a single primary taskbar"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="MMTaskbarEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="disp_multimon_taskbar_mode",
        name="Multi-Monitor Taskbar Button Mode",
        category=TweakCategory.DISPLAY,
        description="Control which taskbar shows buttons for open windows on multi-monitor setups",
        option=TweakOption(
            name="mode",
            label="Button mode",
            type="dropdown",
            default=0,
            description="Choose where window buttons appear across your monitors",
            choices=[
                (0, "All taskbars"),
                (1, "Main taskbar + window's monitor"),
                (2, "Window's monitor only")
            ]
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="MMTaskbarMode",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="disp_virtual_desktop_persist",
        name="Show All Virtual Desktop Windows on Taskbar",
        category=TweakCategory.DISPLAY,
        description="Show buttons for windows from all virtual desktops on the taskbar",
        option=TweakOption(
            name="enabled",
            label="Show all desktops on taskbar",
            type="checkbox",
            default=False,
            description="When enabled you see every window regardless of which virtual desktop is active"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="VirtualDesktopTaskbarFilter",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="disp_virtual_desktop_alt_tab",
        name="Alt+Tab Shows All Virtual Desktop Windows",
        category=TweakCategory.DISPLAY,
        description="Include windows from all virtual desktops in the Alt+Tab switcher",
        option=TweakOption(
            name="enabled",
            label="All desktops in Alt+Tab",
            type="checkbox",
            default=False,
            description="Disable to see only the current virtual desktop's windows in Alt+Tab"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="VirtualDesktopAltTabFilter",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="disp_wallpaper_quality",
        name="Desktop Wallpaper JPEG Quality",
        category=TweakCategory.DISPLAY,
        description="Set the JPEG compression quality Windows uses when processing wallpapers",
        option=TweakOption(
            name="quality",
            label="Quality (0–100)",
            type="spinbox",
            default=90,
            description="Default is 75; raise to 100 to prevent lossy compression of your wallpaper",
            min_value=0,
            max_value=100
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Desktop",
                value_name="JPEGImportQuality",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="disp_dynamic_refresh_rate",
        name="Dynamic Refresh Rate (DRR)",
        category=TweakCategory.DISPLAY,
        description="Allow Windows 11 to boost refresh rate during scrolling and animations (VRR panel required)",
        option=TweakOption(
            name="enabled",
            label="Enable Dynamic Refresh Rate",
            type="checkbox",
            default=False,
            description="Requires a variable-refresh-rate display; saves power while scrolling at high Hz"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows NT\CurrentVersion\dwm",
                value_name="DRREnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="disp_hw_accelerated_compositing",
        name="Disable DWM Hardware Compositing",
        category=TweakCategory.DISPLAY,
        description="Force DWM to use software compositing (debug / compatibility use)",
        option=TweakOption(
            name="enabled",
            label="Disable HW compositing",
            type="checkbox",
            default=False,
            description="⚠ Severely degrades visual performance; only useful for diagnosing GPU driver issues"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\DWM",
                value_name="DisableHWAcceleration",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="disp_disable_gdi_scaling",
        name="Disable GDI DPI Scaling for Blurry Apps Fix",
        category=TweakCategory.DISPLAY,
        description="Stop Windows from auto-scaling legacy GDI apps (can cause blur on hi-DPI)",
        option=TweakOption(
            name="enabled",
            label="Disable GDI DPI scaling",
            type="checkbox",
            default=False,
            description="Legacy apps will be crisp but tiny on 4K; modern apps unaffected"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\SideBySide",
                value_name="PreferExternalManifest",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="disp_monitor_timeout_ac",
        name="Monitor Sleep Timeout on AC Power (minutes)",
        category=TweakCategory.DISPLAY,
        description="Set how many minutes of inactivity before the monitor turns off on AC",
        option=TweakOption(
            name="minutes",
            label="Timeout (minutes, 0=never)",
            type="spinbox",
            default=10,
            description="0 = never turn off. Applies to the active power plan.",
            min_value=0,
            max_value=240
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Power\PowerSettings\3C0BC021-C8A8-4E07-A973-6B14CBCB2B7E",
                value_name="ACSettingIndex",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="disp_cleartype_enabled",
        name="ClearType Font Rendering",
        category=TweakCategory.DISPLAY,
        description="Enable or disable ClearType subpixel anti-aliasing for LCD text",
        option=TweakOption(
            name="enabled",
            label="Enable ClearType",
            type="checkbox",
            default=True,
            description="ClearType improves text readability on LCD screens; disable for OLED/4K/print-sharp text"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Desktop",
                value_name="FontSmoothingType",
                value_type=winreg.REG_DWORD,
                enabled_value=2,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="disp_cursor_blink_rate",
        name="Text Cursor Blink Rate",
        category=TweakCategory.DISPLAY,
        description="Set how fast the text cursor blinks in editors and text fields",
        option=TweakOption(
            name="rate",
            label="Blink rate (ms, -1=no blink)",
            type="spinbox",
            default=530,
            description="530ms = Windows default. Set -1 to disable blinking entirely.",
            min_value=-1,
            max_value=2000
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Desktop",
                value_name="CursorBlinkRate",
                value_type=winreg.REG_SZ,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="disp_taskbar_thumbnail_delay",
        name="Taskbar Thumbnail Preview Delay",
        category=TweakCategory.DISPLAY,
        description="Set the delay before taskbar thumbnail previews appear on hover",
        option=TweakOption(
            name="delay",
            label="Delay (ms)",
            type="spinbox",
            default=400,
            description="Lower = faster preview; 0 = instant; default is 400ms",
            min_value=0,
            max_value=2000
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="ExtendedUIHoverTime",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="disp_show_color_calibration",
        name="Show Color Calibration on Startup",
        category=TweakCategory.DISPLAY,
        description="Run the display color calibration tool automatically at login",
        option=TweakOption(
            name="enabled",
            label="Run calibration at startup",
            type="checkbox",
            default=False,
            description="Loads the ICC color profile calibration loader on each sign-in"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\ICM",
                value_name="Calibration0",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="disp_disable_rotation_lock",
        name="Disable Display Auto-Rotation Lock",
        category=TweakCategory.DISPLAY,
        description="Prevent Windows from locking screen rotation on convertible/tablet devices",
        option=TweakOption(
            name="enabled",
            label="Disable rotation lock",
            type="checkbox",
            default=False,
            description="Tablet/2-in-1 only: allows display to rotate freely based on accelerometer"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\AutoRotation",
                value_name="Enable",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="disp_hide_desktop_icons",
        name="Hide All Desktop Icons",
        category=TweakCategory.DISPLAY,
        description="Completely hide all icons on the desktop for a clean look",
        option=TweakOption(
            name="enabled",
            label="Hide desktop icons",
            type="checkbox",
            default=False,
            description="Icons are still there — just invisible. Right-click desktop → View → Show Desktop Icons to restore"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="HideIcons",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="disp_window_snap_across_monitors",
        name="Snap Windows Across Monitor Boundaries",
        category=TweakCategory.DISPLAY,
        description="Allow windows to snap to the edges between monitors",
        option=TweakOption(
            name="enabled",
            label="Cross-monitor snapping",
            type="checkbox",
            default=True,
            description="Disable to prevent accidentally snapping a window to another screen"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Desktop",
                value_name="MonitorSnapToEdges",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="disp_win_animation_speed",
        name="Window Open/Close Animation Speed",
        category=TweakCategory.DISPLAY,
        description="Control how fast window open, close and minimize animations play",
        option=TweakOption(
            name="speed",
            label="Animation duration (ms)",
            type="spinbox",
            default=200,
            description="Lower = snappier; 0 = instant; Windows default is ~200ms",
            min_value=0,
            max_value=1000
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Desktop\WindowMetrics",
                value_name="MinAnimate",
                value_type=winreg.REG_SZ,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
]

# =============================================================================
# MOUSE & INPUT TWEAKS
# =============================================================================

MOUSE_INPUT_TWEAKS = [
    Tweak(
        id="input_mouse_dpi_hint",
        name="Mouse Sensitivity (Control Panel)",
        category=TweakCategory.MOUSE_INPUT,
        description="Set Windows pointer speed — separate from your mouse's hardware DPI",
        option=TweakOption(
            name="speed",
            label="Speed (1–20)",
            type="spinbox",
            default=10,
            description="Windows default is 10; hardware DPI in your mouse software is independent",
            min_value=1,
            max_value=20
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Mouse",
                value_name="MouseSensitivity",
                value_type=winreg.REG_SZ,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="input_enhance_pointer_precision",
        name="Enhance Pointer Precision (Mouse Acceleration)",
        category=TweakCategory.MOUSE_INPUT,
        description="Enable or disable Windows mouse acceleration curve",
        option=TweakOption(
            name="enabled",
            label="Enable pointer precision",
            type="checkbox",
            default=True,
            description="Disable for raw 1:1 input — essential for FPS gaming and precise work"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Mouse",
                value_name="MouseSpeed",
                value_type=winreg.REG_SZ,
                enabled_value="1",
                disabled_value="0"
            ),
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Mouse",
                value_name="MouseThreshold1",
                value_type=winreg.REG_SZ,
                enabled_value="6",
                disabled_value="0"
            ),
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Mouse",
                value_name="MouseThreshold2",
                value_type=winreg.REG_SZ,
                enabled_value="10",
                disabled_value="0"
            )
        ]
    ),
    Tweak(
        id="input_scroll_lines",
        name="Mouse Wheel Scroll Lines",
        category=TweakCategory.MOUSE_INPUT,
        description="Set how many lines scroll per wheel notch",
        option=TweakOption(
            name="lines",
            label="Lines per scroll",
            type="spinbox",
            default=3,
            description="Windows default is 3; raise to 5–10 for faster scrolling in documents",
            min_value=1,
            max_value=20
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Desktop",
                value_name="WheelScrollLines",
                value_type=winreg.REG_SZ,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="input_scroll_chars",
        name="Mouse Wheel Horizontal Scroll Characters",
        category=TweakCategory.MOUSE_INPUT,
        description="Set characters scrolled per horizontal wheel tilt",
        option=TweakOption(
            name="chars",
            label="Characters per tilt",
            type="spinbox",
            default=3,
            description="Affects horizontal scrolling with tilt wheels; default is 3",
            min_value=1,
            max_value=20
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Desktop",
                value_name="WheelScrollChars",
                value_type=winreg.REG_SZ,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="input_double_click_speed",
        name="Double-Click Speed",
        category=TweakCategory.MOUSE_INPUT,
        description="Set the maximum time interval between two clicks to register as a double-click",
        option=TweakOption(
            name="speed",
            label="Speed (100–900 ms)",
            type="spinbox",
            default=500,
            description="Lower = faster double-click required; default Windows is 500ms",
            min_value=100,
            max_value=900
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Mouse",
                value_name="DoubleClickSpeed",
                value_type=winreg.REG_SZ,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="input_swap_mouse_buttons",
        name="Swap Primary/Secondary Mouse Buttons",
        category=TweakCategory.MOUSE_INPUT,
        description="Switch left and right mouse button functions (left-handed mouse setup)",
        option=TweakOption(
            name="enabled",
            label="Swap mouse buttons",
            type="checkbox",
            default=False,
            description="Right button becomes the primary click — useful for left-handed users"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Mouse",
                value_name="SwapMouseButtons",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="input_touchpad_sensitivity",
        name="Touchpad Sensitivity",
        category=TweakCategory.MOUSE_INPUT,
        description="Adjust Windows Precision Touchpad sensitivity level",
        option=TweakOption(
            name="level",
            label="Sensitivity",
            type="dropdown",
            default=3,
            description="Controls how easily accidental touches are ignored",
            choices=[
                (0, "Most sensitive"),
                (1, "High"),
                (2, "Medium"),
                (3, "Low (default)"),
                (4, "Least sensitive")
            ]
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\PrecisionTouchPad",
                value_name="AAPThreshold",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="input_touchpad_tap_to_click",
        name="Touchpad Tap to Click",
        category=TweakCategory.MOUSE_INPUT,
        description="Enable or disable tap-to-click on Windows Precision Touchpad",
        option=TweakOption(
            name="enabled",
            label="Enable tap to click",
            type="checkbox",
            default=True,
            description="Touching the touchpad surface registers as a left click"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\PrecisionTouchPad",
                value_name="TapsEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="input_touchpad_two_finger_tap",
        name="Touchpad Two-Finger Tap (Right-Click)",
        category=TweakCategory.MOUSE_INPUT,
        description="Enable two-finger tap as right-click on Precision Touchpad",
        option=TweakOption(
            name="enabled",
            label="Two-finger tap = right-click",
            type="checkbox",
            default=True,
            description="Tapping with two fingers simultaneously triggers a right-click context menu"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\PrecisionTouchPad",
                value_name="TwoFingerTapEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="input_touchpad_three_finger_tap",
        name="Touchpad Three-Finger Tap Action",
        category=TweakCategory.MOUSE_INPUT,
        description="Set what happens when you tap with three fingers on the touchpad",
        option=TweakOption(
            name="action",
            label="Action",
            type="dropdown",
            default=2,
            description="Three-finger tap shortcut",
            choices=[
                (0, "Nothing"),
                (1, "Middle click"),
                (2, "Search / Cortana"),
                (3, "Action Center")
            ]
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\PrecisionTouchPad",
                value_name="ThreeFingerTapEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="input_touchpad_zoom",
        name="Touchpad Pinch to Zoom",
        category=TweakCategory.MOUSE_INPUT,
        description="Enable or disable pinch-to-zoom gesture on the touchpad",
        option=TweakOption(
            name="enabled",
            label="Enable pinch to zoom",
            type="checkbox",
            default=True,
            description="Two-finger pinch gesture zooms content in supported apps"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\PrecisionTouchPad",
                value_name="ZoomEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="input_touchpad_scroll_direction",
        name="Touchpad Scroll Direction",
        category=TweakCategory.MOUSE_INPUT,
        description="Choose between natural (content follows finger) and traditional scroll direction",
        option=TweakOption(
            name="enabled",
            label="Natural scrolling (reversed)",
            type="checkbox",
            default=False,
            description="Natural = content moves with your finger (iOS/macOS style)"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\PrecisionTouchPad",
                value_name="ScrollDirection",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="input_raw_mouse_input",
        name="Force Raw Mouse Input",
        category=TweakCategory.MOUSE_INPUT,
        description="Hint to the system to prefer raw HID mouse input over accelerated Win32 cursor",
        option=TweakOption(
            name="enabled",
            label="Prefer raw mouse input",
            type="checkbox",
            default=False,
            description="Bypasses Windows cursor processing for lowest-latency input in games"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows",
                value_name="USBMousePollRate",
                value_type=winreg.REG_DWORD,
                enabled_value=1000,
                disabled_value=125
            )
        ]
    ),
    Tweak(
        id="input_keyboard_layout",
        name="Disable Keyboard Layout Switching Shortcut",
        category=TweakCategory.MOUSE_INPUT,
        description="Disable the Alt+Shift / Ctrl+Shift hotkey that switches keyboard layouts",
        option=TweakOption(
            name="enabled",
            label="Disable layout switch shortcut",
            type="checkbox",
            default=False,
            description="Prevents accidental language/layout changes while typing"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Keyboard Layout\Toggle",
                value_name="Language Hotkey",
                value_type=winreg.REG_SZ,
                enabled_value="3",
                disabled_value="1"
            )
        ]
    ),
    Tweak(
        id="input_ime_cand_window",
        name="IME Candidate Window Mode",
        category=TweakCategory.MOUSE_INPUT,
        description="Set IME (Input Method Editor) candidate window position preference",
        option=TweakOption(
            name="mode",
            label="Window position",
            type="dropdown",
            default=0,
            description="Affects CJK input method suggestion windows",
            choices=[
                (0, "Follow caret"),
                (1, "Fixed position"),
                (2, "Edge of screen")
            ]
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\IME\15.0\IMEJP\MSIME",
                value_name="CandidateWindowPosMode",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="input_num_lock_login",
        name="NumLock State at Login Screen",
        category=TweakCategory.MOUSE_INPUT,
        description="Set whether NumLock is on or off at the Windows login screen",
        option=TweakOption(
            name="enabled",
            label="NumLock ON at login",
            type="checkbox",
            default=True,
            description="NumLock on by default saves a keypress when entering numeric passwords"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_USERS,
                key_path=r".DEFAULT\Control Panel\Keyboard",
                value_name="InitialKeyboardIndicators",
                value_type=winreg.REG_SZ,
                enabled_value="2",
                disabled_value="0"
            )
        ]
    ),
    Tweak(
        id="input_keyboard_backlight_timeout",
        name="Keyboard Backlight Timeout",
        category=TweakCategory.MOUSE_INPUT,
        description="Set how quickly the keyboard backlight turns off (laptop keyboards)",
        option=TweakOption(
            name="timeout",
            label="Timeout (seconds, 0=always on)",
            type="spinbox",
            default=30,
            description="Reduces battery drain; 0 keeps backlight on whenever the display is on",
            min_value=0,
            max_value=300
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Power\PowerSettings\7516b95f-f776-4464-8c53-06167f40cc99\4faab71a-92e5-4726-b1e6-2636e4e807cb",
                value_name="ACSettingIndex",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="input_mouse_hover_time",
        name="Mouse Hover Dwell Time",
        category=TweakCategory.MOUSE_INPUT,
        description="Milliseconds the cursor must stay over a control before hover events fire",
        option=TweakOption(
            name="time",
            label="Hover time (ms)",
            type="spinbox",
            default=400,
            description="Lower = faster tooltip/hover response; Windows default 400ms",
            min_value=10,
            max_value=2000
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Mouse",
                value_name="MouseHoverTime",
                value_type=winreg.REG_SZ,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="input_disable_touchscreen",
        name="Disable Touchscreen Input",
        category=TweakCategory.MOUSE_INPUT,
        description="Disable the touchscreen digitizer (useful for touch-panel PCs used with mouse only)",
        option=TweakOption(
            name="enabled",
            label="Disable touchscreen",
            type="checkbox",
            default=False,
            description="Prevents accidental touches while typing on convertible laptops"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows\TabletPC",
                value_name="TurnOffSingleFingerPanning",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="input_mouse_sonar",
        name="Show Mouse Location on Ctrl Press (Sonar)",
        category=TweakCategory.MOUSE_INPUT,
        description="Press Ctrl to briefly highlight the mouse cursor location with a circle",
        option=TweakOption(
            name="enabled",
            label="Enable mouse sonar",
            type="checkbox",
            default=False,
            description="Useful on large or multi-monitor setups when you lose track of the cursor"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Mouse",
                value_name="MouseSonar",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="input_pointer_snap_default",
        name="Snap Pointer to Default Button",
        category=TweakCategory.MOUSE_INPUT,
        description="Automatically move the cursor to the default button when a dialog opens",
        option=TweakOption(
            name="enabled",
            label="Snap to default button",
            type="checkbox",
            default=False,
            description="Saves mouse movement in repetitive dialogs; can be surprising if unexpected"
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
        id="input_gamepad_vibration",
        name="Disable Controller Vibration (System-wide hint)",
        category=TweakCategory.MOUSE_INPUT,
        description="Hint to disable vibration for XInput game controllers",
        option=TweakOption(
            name="enabled",
            label="Disable gamepad vibration",
            type="checkbox",
            default=False,
            description="Reduces distraction and saves battery on wireless controllers"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\XInput",
                value_name="NoVibration",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
]

# =============================================================================
# STARTUP & BOOT TWEAKS
# =============================================================================

STARTUP_BOOT_TWEAKS = [
    Tweak(
        id="boot_timeout",
        name="Boot Menu Timeout",
        category=TweakCategory.STARTUP_BOOT,
        description="Seconds the boot menu waits before auto-selecting the default OS",
        option=TweakOption(
            name="seconds",
            label="Timeout (seconds)",
            type="spinbox",
            default=30,
            description="Set to 5 for fast single-OS boots; set higher if you dual-boot",
            min_value=0,
            max_value=999
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Session Manager\Boot Execute",
                value_name="BootExecute",
                value_type=winreg.REG_MULTI_SZ,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="boot_verbose_messages",
        name="Verbose Boot/Shutdown Messages",
        category=TweakCategory.STARTUP_BOOT,
        description="Show detailed status messages during Windows startup and shutdown",
        option=TweakOption(
            name="enabled",
            label="Show verbose messages",
            type="checkbox",
            default=False,
            description="Displays 'Starting services…', 'Stopping X…' instead of the spinning dots"
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
        id="boot_auto_restart_bsod",
        name="Auto-Restart After BSOD",
        category=TweakCategory.STARTUP_BOOT,
        description="Control whether Windows automatically reboots after a blue screen crash",
        option=TweakOption(
            name="enabled",
            label="Auto-restart after BSOD",
            type="checkbox",
            default=True,
            description="Disable to keep the BSOD on screen so you can read the error code"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\CrashControl",
                value_name="AutoReboot",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="boot_bsod_beep",
        name="Beep on BSOD",
        category=TweakCategory.STARTUP_BOOT,
        description="Play a system beep when a kernel crash (BSOD) occurs",
        option=TweakOption(
            name="enabled",
            label="Beep on BSOD",
            type="checkbox",
            default=True,
            description="Useful on headless/server systems to audibly alert you to a crash"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\CrashControl",
                value_name="Beep",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="boot_overwrite_existing_dump",
        name="Overwrite Existing Crash Dump",
        category=TweakCategory.STARTUP_BOOT,
        description="Replace the previous crash dump file rather than appending a new one",
        option=TweakOption(
            name="enabled",
            label="Overwrite crash dump",
            type="checkbox",
            default=True,
            description="Keeps disk usage predictable; disable to accumulate dumps for later analysis"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\CrashControl",
                value_name="Overwrite",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="boot_last_known_good",
        name="Enable Last Known Good Configuration",
        category=TweakCategory.STARTUP_BOOT,
        description="Preserve the Last Known Good boot configuration entry in the boot menu",
        option=TweakOption(
            name="enabled",
            label="Keep Last Known Good entry",
            type="checkbox",
            default=True,
            description="Allows recovery via boot menu if a driver or service breaks the system"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Session Manager\Configuration Manager",
                value_name="LastKnownGood",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="boot_startup_delay",
        name="Startup Program Launch Delay",
        category=TweakCategory.STARTUP_BOOT,
        description="Delay before startup programs are launched after login (seconds)",
        option=TweakOption(
            name="delay",
            label="Delay (seconds)",
            type="spinbox",
            default=10,
            description="Spreading startup programs out reduces the initial login slowdown",
            min_value=0,
            max_value=120
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Serialize",
                value_name="StartupDelayInMSec",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="boot_disable_startup_animation",
        name="Disable Windows Startup Animation",
        category=TweakCategory.STARTUP_BOOT,
        description="Skip the spinning dots boot animation for a faster perceived boot",
        option=TweakOption(
            name="enabled",
            label="Disable startup animation",
            type="checkbox",
            default=False,
            description="Removes the spinning circle animation; boot time is the same but it feels faster"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System",
                value_name="DisableStartupAnimation",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="boot_disable_first_logon_animation",
        name="Disable First Logon Animation",
        category=TweakCategory.STARTUP_BOOT,
        description="Skip the 'Hi! We're getting everything ready for you' first-logon experience",
        option=TweakOption(
            name="enabled",
            label="Disable first logon animation",
            type="checkbox",
            default=False,
            description="Skips the animated welcome screen on new user accounts or after major updates"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon",
                value_name="EnableFirstLogonAnimation",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="boot_legal_notice_title",
        name="Custom Login Screen Legal Notice Title",
        category=TweakCategory.STARTUP_BOOT,
        description="Show a custom title banner on the Windows login screen",
        option=TweakOption(
            name="title",
            label="Notice title text",
            type="spinbox",
            default=0,
            description="Leave blank to disable. Use registry editor to set custom text.",
            min_value=0,
            max_value=0
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon",
                value_name="LegalNoticeCaption",
                value_type=winreg.REG_SZ,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="boot_shutdown_timeout",
        name="System Shutdown Wait Timeout",
        category=TweakCategory.STARTUP_BOOT,
        description="Maximum seconds Windows waits for services to stop before force-shutting down",
        option=TweakOption(
            name="seconds",
            label="Timeout (ms)",
            type="spinbox",
            default=5000,
            description="Default 5000ms (5s). Lower to 2000ms for faster shutdowns.",
            min_value=1000,
            max_value=20000
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control",
                value_name="WaitToKillServiceTimeout",
                value_type=winreg.REG_SZ,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="boot_fast_startup_control",
        name="Fast Startup / Hiberboot",
        category=TweakCategory.STARTUP_BOOT,
        description="Hybrid shutdown that saves kernel state to disk for faster next boot",
        option=TweakOption(
            name="enabled",
            label="Enable Fast Startup",
            type="checkbox",
            default=True,
            description="Speeds up boot but can cause issues with dual-boot and full Windows Updates"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Session Manager\Power",
                value_name="HiberbootEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="boot_num_processors",
        name="Boot with Multiple Processors",
        category=TweakCategory.STARTUP_BOOT,
        description="Enable multi-processor boot to use all CPU cores during startup (MSCONFIG equivalent)",
        option=TweakOption(
            name="enabled",
            label="Multi-processor boot",
            type="checkbox",
            default=False,
            description="Forces Windows to boot using all available CPU cores instead of a single core"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management",
                value_name="PhysicalAddressExtension",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="boot_app_recovery_interval",
        name="Application Recovery Interval",
        category=TweakCategory.STARTUP_BOOT,
        description="How often (ms) Windows checkpoints application state for crash recovery",
        option=TweakOption(
            name="interval",
            label="Interval (ms)",
            type="spinbox",
            default=60000,
            description="Lower = more frequent checkpoints = more disk I/O; default 60000 (1 min)",
            min_value=5000,
            max_value=300000
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\ApplicationRecovery",
                value_name="PingInterval",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="boot_event_log_max_size",
        name="System Event Log Maximum Size",
        category=TweakCategory.STARTUP_BOOT,
        description="Set the maximum size of the Windows System event log file",
        option=TweakOption(
            name="size",
            label="Max size (KB)",
            type="spinbox",
            default=20480,
            description="Default 20480 KB (20MB). Raise for servers that need long log history.",
            min_value=1024,
            max_value=1048576
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\EventLog\System",
                value_name="MaxSize",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="boot_app_event_log_size",
        name="Application Event Log Maximum Size",
        category=TweakCategory.STARTUP_BOOT,
        description="Set the maximum size of the Windows Application event log file",
        option=TweakOption(
            name="size",
            label="Max size (KB)",
            type="spinbox",
            default=20480,
            description="Raise if applications log frequently and you need history beyond default 20MB",
            min_value=1024,
            max_value=1048576
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\EventLog\Application",
                value_name="MaxSize",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="boot_disable_windows_error_reporting_ui",
        name="Disable Windows Error Reporting UI",
        category=TweakCategory.STARTUP_BOOT,
        description="Suppress the 'Windows is looking for a solution to the problem' dialog",
        option=TweakOption(
            name="enabled",
            label="Disable WER dialog",
            type="checkbox",
            default=False,
            description="Crashes are still logged but no dialog pops up asking to report them"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\Windows Error Reporting",
                value_name="DontShowUI",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="boot_background_apps_on_battery",
        name="Disable Background App Refresh on Battery",
        category=TweakCategory.STARTUP_BOOT,
        description="Stop UWP apps from refreshing in the background when on battery power",
        option=TweakOption(
            name="enabled",
            label="Disable background refresh on battery",
            type="checkbox",
            default=False,
            description="Extends battery life by pausing app updates until plugged in"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows\AppPrivacy",
                value_name="LetAppsRunInBackground",
                value_type=winreg.REG_DWORD,
                enabled_value=2,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="boot_disable_auto_update_relaunch",
        name="Disable App Auto-Relaunch After Update Reboot",
        category=TweakCategory.STARTUP_BOOT,
        description="Prevent Windows from automatically reopening apps after an update restart",
        option=TweakOption(
            name="enabled",
            label="Disable auto-relaunch after update",
            type="checkbox",
            default=False,
            description="After a forced update reboot, Windows won't reopen your previous apps"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon",
                value_name="RestartApps",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="boot_clear_temp_on_startup",
        name="Clear Temp Folder on Startup",
        category=TweakCategory.STARTUP_BOOT,
        description="Automatically delete temporary files at every Windows startup",
        option=TweakOption(
            name="enabled",
            label="Clear temp on startup",
            type="checkbox",
            default=False,
            description="Cleans %TEMP% on boot; frees disk space but slightly increases startup time"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System",
                value_name="ClearTempFilesAtBoot",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
]

# =============================================================================
# NOTIFICATIONS TWEAKS
# =============================================================================

NOTIFICATIONS_TWEAKS = [
    Tweak(
        id="notif_focus_assist_off",
        name="Disable Focus Assist (Do Not Disturb)",
        category=TweakCategory.NOTIFICATIONS,
        description="Turn off Focus Assist so all notifications come through immediately",
        option=TweakOption(
            name="enabled",
            label="Disable Focus Assist",
            type="checkbox",
            default=False,
            description="When enabled, all banners and sounds play without any DND filtering"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\CloudStore\Store\Cache\DefaultAccount\$$windows.data.notifications.quiethourssettings\Current",
                value_name="Data",
                value_type=winreg.REG_BINARY,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="notif_toast_duration",
        name="Toast Notification Duration",
        category=TweakCategory.NOTIFICATIONS,
        description="How long toast notification banners stay on screen before fading",
        option=TweakOption(
            name="duration",
            label="Duration",
            type="dropdown",
            default="5",
            description="Longer duration gives more time to read and act on notifications",
            choices=[
                ("5", "5 seconds (default)"),
                ("7", "7 seconds"),
                ("15", "15 seconds"),
                ("25", "25 seconds"),
                ("30", "30 seconds")
            ]
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Control Panel\Accessibility",
                value_name="MessageDuration",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="notif_disable_all",
        name="Disable All Notifications",
        category=TweakCategory.NOTIFICATIONS,
        description="Suppress all app notifications system-wide via policy",
        option=TweakOption(
            name="enabled",
            label="Disable all notifications",
            type="checkbox",
            default=False,
            description="No banners, no sounds, no Action Center entries from any app"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows\Explorer",
                value_name="DisableNotificationCenter",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="notif_disable_lock_screen",
        name="Disable Notifications on Lock Screen",
        category=TweakCategory.NOTIFICATIONS,
        description="Hide notification content on the lock screen for privacy",
        option=TweakOption(
            name="enabled",
            label="Hide lock screen notifications",
            type="checkbox",
            default=False,
            description="Notifications won't show on the lock screen; reduces privacy exposure"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows\System",
                value_name="DisableLockScreenAppNotifications",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="notif_taskbar_badge",
        name="Show App Badges on Taskbar Buttons",
        category=TweakCategory.NOTIFICATIONS,
        description="Display unread count badges on taskbar app buttons",
        option=TweakOption(
            name="enabled",
            label="Show taskbar badges",
            type="checkbox",
            default=True,
            description="Small number overlays on taskbar icons show unread notifications count"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="TaskbarBadges",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="notif_action_center",
        name="Disable Action Center",
        category=TweakCategory.NOTIFICATIONS,
        description="Remove the Action Center / notification panel entirely",
        option=TweakOption(
            name="enabled",
            label="Disable Action Center",
            type="checkbox",
            default=False,
            description="The bell icon and sliding panel are hidden; notifications are still delivered in background"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Policies\Microsoft\Windows\Explorer",
                value_name="DisableNotificationCenter",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="notif_windows_update_restart",
        name="Suppress Update Restart Notifications",
        category=TweakCategory.NOTIFICATIONS,
        description="Stop Windows Update from showing 'Your device needs to restart' prompts",
        option=TweakOption(
            name="enabled",
            label="Suppress update restart prompts",
            type="checkbox",
            default=False,
            description="You control when to reboot; Windows won't nag you with restart reminders"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate",
                value_name="SetAutoRestartNotificationConfig",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="notif_security_center_alerts",
        name="Disable Windows Security Center Alerts",
        category=TweakCategory.NOTIFICATIONS,
        description="Stop Windows Security Center from showing tray alerts and notifications",
        option=TweakOption(
            name="enabled",
            label="Disable Security Center alerts",
            type="checkbox",
            default=False,
            description="Security features still run — you just won't see alert popups"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows Defender Security Center\Notifications",
                value_name="DisableNotifications",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="notif_system_sounds",
        name="Disable System Notification Sounds",
        category=TweakCategory.NOTIFICATIONS,
        description="Mute the sounds that play for system events (errors, USB connect, etc.)",
        option=TweakOption(
            name="enabled",
            label="Disable system sounds",
            type="checkbox",
            default=False,
            description="Sets the sound scheme to 'No Sounds' — visual notifications still appear"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"AppEvents\Schemes",
                value_name="",
                value_type=winreg.REG_SZ,
                enabled_value=".None",
                disabled_value=".Default"
            )
        ]
    ),
    Tweak(
        id="notif_new_app_alert",
        name="Disable New App Installation Notifications",
        category=TweakCategory.NOTIFICATIONS,
        description="Stop Windows from notifying you when a new app is installed",
        option=TweakOption(
            name="enabled",
            label="Disable new app notifications",
            type="checkbox",
            default=False,
            description="No more 'An app has been installed' balloon tips in the tray"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="EnableBalloonTips",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="notif_driver_install_balloon",
        name="Disable Device Driver Install Balloon",
        category=TweakCategory.NOTIFICATIONS,
        description="Suppress the 'Your device is ready to use' balloon when a driver installs",
        option=TweakOption(
            name="enabled",
            label="Disable driver install balloon",
            type="checkbox",
            default=False,
            description="Reduces tray clutter when frequently plugging in USB devices"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows\DeviceInstall\Settings",
                value_name="DisableBalloonTips",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="notif_low_battery_alert",
        name="Low Battery Notification Level",
        category=TweakCategory.NOTIFICATIONS,
        description="Set the battery percentage that triggers a low battery warning",
        option=TweakOption(
            name="level",
            label="Alert at (% remaining)",
            type="spinbox",
            default=10,
            description="Windows will show a notification when battery drops below this level",
            min_value=1,
            max_value=50
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Power\User\PowerSchemes\{power-plan-guid}\7516b95f-f776-4464-8c53-06167f40cc99\8183ba9a-e910-48da-8769-14ae6dc1170a",
                value_name="ACSettingIndex",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="notif_explorer_balloon_tips",
        name="Disable Explorer Balloon Tip Notifications",
        category=TweakCategory.NOTIFICATIONS,
        description="Suppress File Explorer balloon tips (e.g., 'You have unused desktop icons')",
        option=TweakOption(
            name="enabled",
            label="Disable Explorer balloon tips",
            type="checkbox",
            default=False,
            description="No more 'Did you know…' and similar tips popping up from Explorer"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="EnableBalloonTips",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="notif_network_location_wizard",
        name="Disable Network Location Wizard Notification",
        category=TweakCategory.NOTIFICATIONS,
        description="Stop the 'Do you want to allow your PC to be discoverable?' popup on new networks",
        option=TweakOption(
            name="enabled",
            label="Disable network location wizard",
            type="checkbox",
            default=False,
            description="Silently applies the previous network type without prompting"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Network\NewNetworkWindowOff",
                value_name="",
                value_type=winreg.REG_SZ,
                enabled_value="",
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="notif_printer_install_toast",
        name="Disable Printer Install Toast Notification",
        category=TweakCategory.NOTIFICATIONS,
        description="Suppress the 'Setting up [printer]' toast when a printer driver installs",
        option=TweakOption(
            name="enabled",
            label="Disable printer install toast",
            type="checkbox",
            default=False,
            description="Reduces distraction in shared office/print environments"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Notifications\Settings\Windows.SystemToast.Print",
                value_name="Enabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="notif_store_toast",
        name="Disable Microsoft Store Promotional Notifications",
        category=TweakCategory.NOTIFICATIONS,
        description="Block toast notifications from the Microsoft Store app",
        option=TweakOption(
            name="enabled",
            label="Disable Store notifications",
            type="checkbox",
            default=False,
            description="No more 'Check out these new apps' or sale notifications from the Store"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Notifications\Settings\Microsoft.WindowsStore_8wekyb3d8bbwe!App",
                value_name="Enabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="notif_suggested_apps",
        name="Disable App Suggestion Notifications",
        category=TweakCategory.NOTIFICATIONS,
        description="Stop Windows from suggesting apps to install via notifications",
        option=TweakOption(
            name="enabled",
            label="Disable app suggestions",
            type="checkbox",
            default=False,
            description="Blocks 'Try these apps from the Store' promotional notification cards"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                value_name="SystemPaneSuggestionsEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="notif_onedrive_notification",
        name="Disable OneDrive Sync Notifications",
        category=TweakCategory.NOTIFICATIONS,
        description="Suppress OneDrive sync status and promotional notifications",
        option=TweakOption(
            name="enabled",
            label="Disable OneDrive notifications",
            type="checkbox",
            default=False,
            description="OneDrive still syncs — you just won't see the status toast popups"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Notifications\Settings\Microsoft.SkyDrive.Desktop",
                value_name="Enabled",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
]

# =============================================================================
# DEVELOPER TOOLS TWEAKS
# =============================================================================

DEVELOPER_TWEAKS = [
    Tweak(
        id="dev_developer_mode",
        name="Enable Developer Mode",
        category=TweakCategory.DEVELOPER,
        description="Unlock Windows Developer Mode for sideloading, WinDbg, and dev features",
        option=TweakOption(
            name="enabled",
            label="Enable Developer Mode",
            type="checkbox",
            default=False,
            description="Required for WSL2, sideloading UWP apps, and some dev tools"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock",
                value_name="AllowDevelopmentWithoutDevLicense",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            ),
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock",
                value_name="AllowAllTrustedApps",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="dev_windows_sandbox",
        name="Enable Windows Sandbox",
        category=TweakCategory.DEVELOPER,
        description="Enable the Windows Sandbox optional feature (lightweight VM for testing)",
        option=TweakOption(
            name="enabled",
            label="Enable Windows Sandbox",
            type="checkbox",
            default=False,
            description="Requires Pro/Enterprise and hardware virtualization; adds Sandbox to Start Menu"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Ext",
                value_name="SandboxEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="dev_powershell_execution_policy",
        name="PowerShell Execution Policy",
        category=TweakCategory.DEVELOPER,
        description="Set the machine-wide PowerShell script execution policy",
        option=TweakOption(
            name="policy",
            label="Execution policy",
            type="dropdown",
            default="Restricted",
            description="RemoteSigned is the recommended dev setting — local scripts run freely",
            choices=[
                ("Restricted", "Restricted (default — no scripts)"),
                ("RemoteSigned", "RemoteSigned (local scripts OK)"),
                ("Unrestricted", "Unrestricted (all scripts — ⚠)"),
                ("Bypass", "Bypass (skip all checks — ⚠)")
            ]
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\PowerShell\1\ShellIds\Microsoft.PowerShell",
                value_name="ExecutionPolicy",
                value_type=winreg.REG_SZ,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="dev_rdp_port",
        name="Remote Desktop Port",
        category=TweakCategory.DEVELOPER,
        description="Change the RDP listening port from the default 3389",
        option=TweakOption(
            name="port",
            label="Port number",
            type="spinbox",
            default=3389,
            description="Changing from 3389 reduces automated scan exposure; update firewall rules too",
            min_value=1024,
            max_value=65535
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp",
                value_name="PortNumber",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="dev_rdp_session_timeout",
        name="RDP Session Idle Timeout",
        category=TweakCategory.DEVELOPER,
        description="Automatically disconnect idle Remote Desktop sessions after this many minutes",
        option=TweakOption(
            name="minutes",
            label="Timeout (minutes, 0=never)",
            type="spinbox",
            default=0,
            description="0=never disconnect; useful for unattended servers to free licenses",
            min_value=0,
            max_value=480
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows NT\Terminal Services",
                value_name="MaxIdleTime",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="dev_show_file_operations_details",
        name="Show Detailed File Operation Progress",
        category=TweakCategory.DEVELOPER,
        description="Show the detailed more-info view by default during file copies and moves",
        option=TweakOption(
            name="enabled",
            label="Show detailed progress",
            type="checkbox",
            default=False,
            description="Expands the progress dialog to show speed, items remaining, and time left by default"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\OperationStatusManager",
                value_name="EnthusiastMode",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="dev_wsl_memory_limit",
        name="WSL2 Memory Limit Hint",
        category=TweakCategory.DEVELOPER,
        description="Hint for how much RAM WSL2 can consume (also configurable in .wslconfig)",
        option=TweakOption(
            name="enabled",
            label="Enable WSL memory management hint",
            type="checkbox",
            default=False,
            description="Enables the registry key that lets .wslconfig cap WSL2 memory"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Lxss",
                value_name="LxssManagerEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="dev_hyper_v_hint",
        name="Hyper-V Hypervisor Launch Type",
        category=TweakCategory.DEVELOPER,
        description="Control the Hyper-V hypervisor launch mode",
        option=TweakOption(
            name="enabled",
            label="Enable Hyper-V hypervisor",
            type="checkbox",
            default=False,
            description="Enables virtualization; disabling recovers ~5% CPU overhead but breaks WSL2/Docker"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Virtualization",
                value_name="MinVmVersionForCpuBasedMitigations",
                value_type=winreg.REG_SZ,
                enabled_value="1.0",
                disabled_value=""
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="dev_symbol_path",
        name="Windows Symbol Server Path",
        category=TweakCategory.DEVELOPER,
        description="Set the _NT_SYMBOL_PATH environment variable for debugging tools",
        option=TweakOption(
            name="enabled",
            label="Use Microsoft Symbol Server",
            type="checkbox",
            default=False,
            description="Configures the standard Microsoft public symbol server for WinDbg and similar tools"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
                value_name="_NT_SYMBOL_PATH",
                value_type=winreg.REG_EXPAND_SZ,
                enabled_value=r"srv*C:\Symbols*https://msdl.microsoft.com/download/symbols",
                disabled_value=""
            )
        ]
    ),
    Tweak(
        id="dev_crash_on_ctrl_scroll",
        name="Force BSOD via Keyboard (Debug)",
        category=TweakCategory.DEVELOPER,
        description="Allow Ctrl+ScrollLock×2 to trigger a kernel crash for testing crash dumps",
        option=TweakOption(
            name="enabled",
            label="Enable keyboard crash trigger",
            type="checkbox",
            default=False,
            description="⚠ For testing only — double Scroll Lock while holding Ctrl forces a 0xE2 BSOD"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\kbdhid\Parameters",
                value_name="CrashOnCtrlScroll",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="dev_print_spooler_remote",
        name="Allow Remote Print Spooler Connections",
        category=TweakCategory.DEVELOPER,
        description="Control whether remote clients can connect to this machine's Print Spooler",
        option=TweakOption(
            name="enabled",
            label="Allow remote print spooler",
            type="checkbox",
            default=False,
            description="Disable to mitigate PrintNightmare-class vulnerabilities on non-print-server machines"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows NT\Printers",
                value_name="RegisterSpoolerRemoteRpcEndPoint",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=2
            )
        ]
    ),
    Tweak(
        id="dev_event_log_security_size",
        name="Security Event Log Maximum Size",
        category=TweakCategory.DEVELOPER,
        description="Set the maximum size of the Windows Security audit event log",
        option=TweakOption(
            name="size",
            label="Max size (KB)",
            type="spinbox",
            default=20480,
            description="Raise to 102400 (100MB) for SOC/audit environments",
            min_value=1024,
            max_value=1048576
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\EventLog\Security",
                value_name="MaxSize",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="dev_disable_pchealth",
        name="Disable PC Health Check Telemetry",
        category=TweakCategory.DEVELOPER,
        description="Disable the PC Health Check / Windows Update telemetry reporting agent",
        option=TweakOption(
            name="enabled",
            label="Disable PC Health Check agent",
            type="checkbox",
            default=False,
            description="Stops the MicrosoftEdgeUpdate/PCHealth agent from running in the background"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Diagnostics\DiagTrack",
                value_name="ShowedToastAtLevel",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="dev_disable_error_reporting_queue",
        name="Disable Error Reporting Queue",
        category=TweakCategory.DEVELOPER,
        description="Stop Windows Error Reporting from queuing crash reports for later upload",
        option=TweakOption(
            name="enabled",
            label="Disable WER queue",
            type="checkbox",
            default=False,
            description="Crash reports are discarded immediately instead of being queued"
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
    Tweak(
        id="dev_telnet_client",
        name="Enable Telnet Client",
        category=TweakCategory.DEVELOPER,
        description="Enable the built-in Windows Telnet client for testing TCP connections",
        option=TweakOption(
            name="enabled",
            label="Enable Telnet client",
            type="checkbox",
            default=False,
            description="Installs the optional Telnet feature via registry flag (takes effect after reboot)"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\PackageIndex",
                value_name="TelnetClient",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="dev_windows_insider",
        name="Windows Insider Program Channel",
        category=TweakCategory.DEVELOPER,
        description="Set the Windows Insider preview ring/channel",
        option=TweakOption(
            name="ring",
            label="Insider ring",
            type="dropdown",
            default="Retail",
            description="Choose your preview build frequency",
            choices=[
                ("Retail", "Retail (stable — no preview)"),
                ("ReleasePreview", "Release Preview"),
                ("Beta", "Beta Channel"),
                ("Dev", "Dev Channel (latest features)")
            ]
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\WindowsSelfHost\Applicability",
                value_name="BranchName",
                value_type=winreg.REG_SZ,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="dev_disable_feedback_notify",
        name="Disable Windows Feedback Notifications",
        category=TweakCategory.DEVELOPER,
        description="Stop Windows from asking for feedback via notification popups",
        option=TweakOption(
            name="enabled",
            label="Disable feedback notifications",
            type="checkbox",
            default=False,
            description="Suppresses all Windows feedback request notifications system-wide"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Policies\Microsoft\Windows\DataCollection",
                value_name="DoNotShowFeedbackNotifications",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="dev_long_paths",
        name="Enable Win32 Long Path Support",
        category=TweakCategory.DEVELOPER,
        description="Remove the 260-character MAX_PATH limit for Win32 applications",
        option=TweakOption(
            name="enabled",
            label="Enable long paths (>260 chars)",
            type="checkbox",
            default=False,
            description="Required for deep Python/Node.js/Rust project trees; needs app manifest support"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\FileSystem",
                value_name="LongPathsEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
]

# =============================================================================
# EXPANSION TWEAKS — EXISTING CATEGORIES
# =============================================================================

# --- Taskbar expansions ---
TASKBAR_TWEAKS += [
    Tweak(
        id="taskbar_lock",
        name="Lock Taskbar",
        category=TweakCategory.TASKBAR,
        description="Lock the taskbar so it cannot be moved or resized accidentally",
        option=TweakOption(
            name="enabled",
            label="Lock taskbar",
            type="checkbox",
            default=True,
            description="Prevents dragging the taskbar to another screen edge"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="TaskbarSizeMove",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="taskbar_hide_clock",
        name="Hide Clock from Taskbar",
        category=TweakCategory.TASKBAR,
        description="Remove the clock from the system tray notification area",
        option=TweakOption(
            name="enabled",
            label="Hide clock",
            type="checkbox",
            default=False,
            description="Frees space in the notification area; you can still check time via calendar widget"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer",
                value_name="HideClock",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="taskbar_show_desktop_button",
        name="Show Desktop Button (Peek)",
        category=TweakCategory.TASKBAR,
        description="Show or hide the 'Show desktop' strip at the far right of the taskbar",
        option=TweakOption(
            name="enabled",
            label="Show desktop button",
            type="checkbox",
            default=True,
            description="The thin strip at taskbar's right edge minimises all windows on click"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_CURRENT_USER,
                key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                value_name="TaskbarSd",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
]

# --- System expansions ---
SYSTEM_TWEAKS += [
    Tweak(
        id="system_page_file_size",
        name="Page File Initial Size",
        category=TweakCategory.SYSTEM,
        description="Set a fixed page file initial size in megabytes (prevents resize overhead)",
        option=TweakOption(
            name="size",
            label="Initial size (MB)",
            type="spinbox",
            default=2048,
            description="Setting initial = max size prevents the file from growing/shrinking dynamically",
            min_value=256,
            max_value=65536
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management",
                value_name="PagingFiles",
                value_type=winreg.REG_MULTI_SZ,
                enabled_value=None,
                disabled_value=None
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="system_legacy_boot_menu",
        name="Enable Legacy Boot Menu (F8)",
        category=TweakCategory.SYSTEM,
        description="Restore the classic F8 Advanced Boot Options menu at startup",
        option=TweakOption(
            name="enabled",
            label="Enable legacy F8 boot menu",
            type="checkbox",
            default=False,
            description="Allows booting into Safe Mode via F8; adds ~200ms to every boot"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Session Manager\Configuration Manager",
                value_name="BootGUIEnabled",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="system_kernel_no_auto_reboot",
        name="Disable Auto-Reboot on Kernel Crash",
        category=TweakCategory.SYSTEM,
        description="Keep system running (frozen) after BSOD instead of rebooting",
        option=TweakOption(
            name="enabled",
            label="No auto-reboot on kernel crash",
            type="checkbox",
            default=False,
            description="Allows you to photograph/read the BSOD error before the machine restarts"
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
        id="system_processor_name",
        name="Override Processor Display Name",
        category=TweakCategory.SYSTEM,
        description="Customise the CPU name shown in System Properties and Task Manager",
        option=TweakOption(
            name="enabled",
            label="Use custom processor name",
            type="checkbox",
            default=False,
            description="Changes the display string only — no actual CPU modification"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"HARDWARE\DESCRIPTION\System\CentralProcessor\0",
                value_name="ProcessorNameString",
                value_type=winreg.REG_SZ,
                enabled_value="Custom CPU Name",
                disabled_value=None
            )
        ]
    ),
]

# --- Privacy expansions ---
PRIVACY_TWEAKS += [
    Tweak(
        id="priv_app_diagnostics",
        name="Disable App Diagnostics Access",
        category=TweakCategory.PRIVACY,
        description="Prevent apps from reading diagnostic information from other apps",
        option=TweakOption(
            name="enabled",
            label="Deny app diagnostics",
            type="checkbox",
            default=False,
            description="Blocks the appDiagnostics capability — no app can inspect another app's process info"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\appDiagnostics",
                value_name="Value",
                value_type=winreg.REG_SZ,
                enabled_value="Deny",
                disabled_value="Allow"
            )
        ]
    ),
    Tweak(
        id="priv_contacts_access",
        name="Disable Contacts Access (All Apps)",
        category=TweakCategory.PRIVACY,
        description="Block all apps from reading your Windows Contacts/People data",
        option=TweakOption(
            name="enabled",
            label="Deny contacts access",
            type="checkbox",
            default=False,
            description="Apps can't read your People/Contacts database"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\contacts",
                value_name="Value",
                value_type=winreg.REG_SZ,
                enabled_value="Deny",
                disabled_value="Allow"
            )
        ]
    ),
    Tweak(
        id="priv_documents_access",
        name="Disable Documents Library Access (All Apps)",
        category=TweakCategory.PRIVACY,
        description="Block all apps from accessing your Documents folder without explicit permission",
        option=TweakOption(
            name="enabled",
            label="Deny Documents access",
            type="checkbox",
            default=False,
            description="Only applies to UWP/packaged apps that request the documentsLibrary capability"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\documentsLibrary",
                value_name="Value",
                value_type=winreg.REG_SZ,
                enabled_value="Deny",
                disabled_value="Allow"
            )
        ]
    ),
]

# --- Security expansions ---
SECURITY_TWEAKS += [
    Tweak(
        id="sec_disable_guest",
        name="Disable Guest Account",
        category=TweakCategory.SECURITY,
        description="Disable the built-in Guest user account",
        option=TweakOption(
            name="enabled",
            label="Disable Guest account",
            type="checkbox",
            default=False,
            description="Guest account allows unauthenticated logins; disable on all personal machines"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\SpecialAccounts\UserList",
                value_name="Guest",
                value_type=winreg.REG_DWORD,
                enabled_value=0,
                disabled_value=1
            )
        ]
    ),
    Tweak(
        id="sec_no_anon_sam",
        name="Disable Anonymous SAM Enumeration",
        category=TweakCategory.SECURITY,
        description="Prevent anonymous users from enumerating SAM account names",
        option=TweakOption(
            name="enabled",
            label="Block anonymous SAM enumeration",
            type="checkbox",
            default=False,
            description="Stops unauthenticated users from listing account names via the SAM pipe"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Lsa",
                value_name="RestrictAnonymousSAM",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
    Tweak(
        id="sec_audit_logon_events",
        name="Enable Logon Event Auditing",
        category=TweakCategory.SECURITY,
        description="Write a Security event log entry on every successful and failed logon",
        option=TweakOption(
            name="enabled",
            label="Enable logon auditing",
            type="checkbox",
            default=False,
            description="Useful for detecting unauthorized access attempts; fills Security event log"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Lsa",
                value_name="AuditBaseObjects",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
]

# --- Performance expansions ---
PERFORMANCE_TWEAKS += [
    Tweak(
        id="perf_ntfs_mft_zone",
        name="NTFS MFT Zone Reservation",
        category=TweakCategory.PERFORMANCE,
        description="Reserve a larger portion of the volume for the NTFS Master File Table",
        option=TweakOption(
            name="zone",
            label="MFT zone size",
            type="dropdown",
            default=1,
            description="Larger zone reduces MFT fragmentation on drives with many small files",
            choices=[
                (1, "12.5% (default)"),
                (2, "25%"),
                (3, "37.5%"),
                (4, "50%")
            ]
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\FileSystem",
                value_name="NtfsMftZoneReservation",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="perf_disable_write_combining",
        name="Disable Write Combining",
        category=TweakCategory.PERFORMANCE,
        description="Disable write-combining for display memory (can fix GPU tearing/stutters)",
        option=TweakOption(
            name="enabled",
            label="Disable write combining",
            type="checkbox",
            default=False,
            description="⚠ May reduce GPU performance; useful when write-combining causes display glitches"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers",
                value_name="DisableWriteCombining",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="perf_disable_spectre_perf",
        name="Disable Spectre/Meltdown Mitigations (Performance)",
        category=TweakCategory.PERFORMANCE,
        description="Remove CPU vulnerability mitigations for maximum performance",
        option=TweakOption(
            name="enabled",
            label="Disable CPU mitigations",
            type="checkbox",
            default=False,
            description="⚠ Serious security trade-off — gains 5–15% CPU but exposes timing vulnerabilities"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management",
                value_name="FeatureSettingsOverride",
                value_type=winreg.REG_DWORD,
                enabled_value=3,
                disabled_value=0
            ),
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management",
                value_name="FeatureSettingsOverrideMask",
                value_type=winreg.REG_DWORD,
                enabled_value=3,
                disabled_value=3
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="perf_io_priority_boost",
        name="Foreground I/O Priority Boost",
        category=TweakCategory.PERFORMANCE,
        description="Boost I/O priority for the foreground application",
        option=TweakOption(
            name="enabled",
            label="Boost foreground I/O priority",
            type="checkbox",
            default=False,
            description="Active window gets higher priority for disk reads/writes — snappier app response"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Control\PriorityControl",
                value_name="IRQ8Priority",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
            )
        ]
    ),
]

# --- Gaming expansions ---
GAMING_TWEAKS += [
    Tweak(
        id="game_disable_xbox_accessories",
        name="Disable Xbox Accessories Service",
        category=TweakCategory.GAMING,
        description="Stop the Xbox Accessories background service (used for Xbox controllers/headsets)",
        option=TweakOption(
            name="enabled",
            label="Disable Xbox Accessories",
            type="checkbox",
            default=False,
            description="Frees RAM/CPU for users without Xbox accessories; disable Xbox controller remapping"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SYSTEM\CurrentControlSet\Services\XboxGipSvc",
                value_name="Start",
                value_type=winreg.REG_DWORD,
                enabled_value=4,
                disabled_value=3
            )
        ],
        requires_restart=True
    ),
    Tweak(
        id="game_frame_rate_cap",
        name="Global Frame Rate Cap Hint",
        category=TweakCategory.GAMING,
        description="Set a global frame cap in the NVIDIA/system profile (hint — game must respect it)",
        option=TweakOption(
            name="fps",
            label="Max FPS (0 = unlimited)",
            type="spinbox",
            default=0,
            description="0 = no cap; set to 60/120/144 to reduce heat and power without per-game config",
            min_value=0,
            max_value=360
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
                value_name="MaxFrameRate",
                value_type=winreg.REG_DWORD,
                enabled_value=None,
                disabled_value=None
            )
        ]
    ),
    Tweak(
        id="game_auto_hdr",
        name="Auto HDR",
        category=TweakCategory.GAMING,
        description="Enable Auto HDR to automatically add HDR to DirectX 11/12 games",
        option=TweakOption(
            name="enabled",
            label="Enable Auto HDR",
            type="checkbox",
            default=False,
            description="Requires HDR display; adds HDR highlights to SDR games automatically (Windows 11)"
        ),
        registry_changes=[
            RegistryChange(
                hive=winreg.HKEY_LOCAL_MACHINE,
                key_path=r"SOFTWARE\Microsoft\DirectX",
                value_name="AutoHDREnable",
                value_type=winreg.REG_DWORD,
                enabled_value=1,
                disabled_value=0
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
    NETWORK_TWEAKS +
    POWER_TWEAKS +
    GAMING_TWEAKS +
    PERFORMANCE_TWEAKS +
    SECURITY_TWEAKS +
    PRIVACY_TWEAKS +
    APPS_SERVICES_TWEAKS +
    CONTEXT_MENU_TWEAKS +
    PERSONALIZATION_TWEAKS +
    ACCESSIBILITY_TWEAKS +
    DISPLAY_TWEAKS +
    MOUSE_INPUT_TWEAKS +
    STARTUP_BOOT_TWEAKS +
    NOTIFICATIONS_TWEAKS +
    DEVELOPER_TWEAKS
)

# Group tweaks by category
TWEAKS_BY_CATEGORY = {
    category: [t for t in ALL_TWEAKS if t.category == category]
    for category in TweakCategory
}
