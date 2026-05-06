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
    ACCESSIBILITY_TWEAKS
)

# Group tweaks by category
TWEAKS_BY_CATEGORY = {
    category: [t for t in ALL_TWEAKS if t.category == category]
    for category in TweakCategory
}
