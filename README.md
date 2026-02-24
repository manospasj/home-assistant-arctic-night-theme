# Arctic Night Theme for Home Assistant

[![Open in HACS](https://img.shields.io/badge/Available%20in-HACS-41BDF5?logo=home-assistant&logoColor=white)](https://my.home-assistant.io/redirect/hacs_repository/?owner=manospasj&repository=home-assistant-arctic-night-theme&category=theme)

A sleek, high-contrast dark theme for Home Assistant featuring frost-blue accents, built on the [Catppuccin Frappe](https://github.com/catppuccin/catppuccin#-palette) color palette.

## Preview

| Color | Hex | Role |
|-------|-----|------|
| Base | `303446` | Card background |
| Mantle | `292c3c` | Primary background |
| Crust | `232634` | Sidebar / header |
| Blue | `8caaee` | Accent / primary |
| Text | `c6d0f5` | Primary text |

## Installation

### HACS (recommended)

1. Open **HACS** in your Home Assistant instance
2. Click the **three-dot menu** (top right) > **Custom repositories**
3. Paste this repository URL, select **Theme** as the category, and click **Add**
4. Search for "Arctic Night" and click **Download**
5. Restart Home Assistant

### Manual

1. Copy `themes/arctic-night.yaml` into your Home Assistant `config/themes/` directory
2. Add the following to your `configuration.yaml` (if not already present):
   ```yaml
   frontend:
     themes: !include_dir_merge_named themes
   ```
3. Restart Home Assistant

### Activating the theme

- **Per user**: Go to your **Profile** (bottom left in the sidebar) and select **Arctic Night** under **Theme**
- **Globally**: Go to **Developer Tools** > **Actions**, call `frontend.set_theme` with `name: Arctic Night`

## Color Palette

Based on Catppuccin Frappe with **blue** (`8caaee`) as the primary accent color, giving the UI a frost-blue arctic feel.

### Accent & Semantic Colors

| Purpose | Color | Hex |
|---------|-------|-----|
| Primary / Accent | Blue | `8caaee` |
| Error | Red | `e78284` |
| Warning | Yellow | `e5c890` |
| Success | Green | `a6d189` |
| Info | Blue | `8caaee` |

### Surface Colors

| Layer | Color | Hex |
|-------|-------|-----|
| Crust (darkest) | Sidebar, header | `232634` |
| Mantle | Page background | `292c3c` |
| Base | Card background | `303446` |
| Surface 0 | Elevated surfaces | `414559` |
| Surface 1 | Higher surfaces | `51576d` |
| Surface 2 | Highest surfaces | `626880` |

## Credits

- Color palette: [Catppuccin](https://github.com/catppuccin/catppuccin) (Frappe variant)
- Theme structure inspired by [catppuccin/home-assistant](https://github.com/catppuccin/home-assistant)
