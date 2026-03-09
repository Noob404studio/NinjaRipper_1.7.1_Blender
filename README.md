# NinjaRipper_1.7.1_Blender

Updated Blender importer for NinjaRipper 1.7.1  
**Now compatible with Blender 5.0+**

Original addon only worked with Blender 2.79.  
This is a modernized/fixed version that brings .rip import support to current Blender releases.

## Features
- Imports meshes (.rip files) ripped with NinjaRipper 1.7.1
- Supports vertex positions, normals, UVs, vertex colors (when present)
- Material slot creation (basic)
- Works with Blender 5.0
- No longer requires ancient 2.79 Python API

## Installation

1. Download this repository as ZIP or clone it
2. In Blender go to **Edit → Preferences → Add-ons → Install…**
3. Select the `tools/blender_ninjaripper_importer/blender-import-ninjaripper-master/import-ninja.py` file
4. Enable the addon: search for **NinjaRipper** or **Import: Ninja Ripper**

## Usage

1. File → Import → Ninja Ripper (.rip)
2. Select your .rip file
3. Adjust import options if needed (usually defaults work fine)

## Notes & Limitations
- Only tested with NinjaRipper 1.7.1 output
- Complex materials/textures usually need manual reconnection after import
- Some very old .rip files from NinjaRipper ≤ 1.4 may have compatibility issues
- No animation/bone support (static meshes only)

## Credits
- Original NinjaRipper tool & 2.79 importer by blackninja
- Blender 5.0 port & fixes by **Noob404studio**

Feel free to report issues or submit fixes via pull requests, I will add you to the credits list.
