# Arctic Night Theme for Home Assistant

[![Open in HACS](https://img.shields.io/badge/Available%20in-HACS-41BDF5?logo=home-assistant&logoColor=white)](https://my.home-assistant.io/redirect/hacs_repository/?owner=manospasj&repository=home-assistant-arctic-night-theme&category=theme)

A sleek, high-contrast dark theme for Home Assistant featuring frost-blue accents, built on the [Catppuccin Frappe](https://github.com/catppuccin/catppuccin#-palette) color palette.

## Preview

| Color | Hex | Role |
|-------|-----|------|
| Base | <code>&#35;303446</code> | Card background |
| Mantle | <code>&#35;292c3c</code> | Primary background |
| Crust | <code>&#35;232634</code> | Sidebar / header |
| Blue | <code>&#35;8caaee</code> | Accent / primary |
| Text | <code>&#35;c6d0f5</code> | Primary text |

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

Based on Catppuccin Frappe with **blue** (<code>&#35;8caaee</code>) as the primary accent color, giving the UI a frost-blue arctic feel.

### Accent & Semantic Colors

| Purpose | Color | Hex |
|---------|-------|-----|
| Primary / Accent | Blue | <code>&#35;8caaee</code> |
| Error | Red | <code>&#35;e78284</code> |
| Warning | Yellow | <code>&#35;e5c890</code> |
| Success | Green | <code>&#35;a6d189</code> |
| Info | Blue | <code>&#35;8caaee</code> |

### Surface Colors

| Layer | Color | Hex |
|-------|-------|-----|
| Crust (darkest) | Sidebar, header | <code>&#35;232634</code> |
| Mantle | Page background | <code>&#35;292c3c</code> |
| Base | Card background | <code>&#35;303446</code> |
| Surface 0 | Elevated surfaces | <code>&#35;414559</code> |
| Surface 1 | Higher surfaces | <code>&#35;51576d</code> |
| Surface 2 | Highest surfaces | <code>&#35;626880</code> |

## Credits

- Color palette: [Catppuccin](https://github.com/catppuccin/catppuccin) (Frappe variant)
- Theme structure inspired by [catppuccin/home-assistant](https://github.com/catppuccin/home-assistant)
