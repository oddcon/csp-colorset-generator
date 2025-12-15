# CLS Color Set Generator for Clip Studio Paint

A complete toolkit for creating custom `.cls` color palette files for Clip Studio Paint!

## 📦 What's Included

### 1. **Interactive Web Tool** (`cls_color_generator.html`)
- Beautiful web interface for creating palettes
- Color picker and hex input
- Pre-built presets (Rainbow, Pastel, Grayscale, etc.)
- Live preview of your palette
- One-click download of .cls files

**How to use:**
- Open `cls_color_generator.html` in any web browser
- Add colors using the color picker or hex codes
- Click "Generate & Download .cls File"
- Import the downloaded file into Clip Studio Paint!

### 2. **Python Library** (`cls_generator.py`)
- Full-featured Python library for programmatic generation
- Load existing .cls files
- Batch create multiple palettes

**Python Examples:**

```python
from cls_generator import CLSGenerator

# Create a new palette
palette = CLSGenerator("My Palette")

# Add colors
palette.add_color(255, 0, 0)           # RGB
palette.add_color_from_hex("#00FF00")  # Hex

# Save
palette.save("my_palette.cls")
```

### 3. **Sample Palettes**
- `rainbow.cls` - 7-color rainbow
- `pastels.cls` - 5 soft pastel colors
- `grayscale.cls` - 8 neutral grays

## 🎨 How to Import into Clip Studio Paint

1. Open Clip Studio Paint
2. Go to **Window → Color Set**
3. Click the menu icon (☰) in the Color Set palette
4. Select **Import Color Set**
5. Choose your `.cls` file
6. Done! Your colors are now available

## 🔧 Technical Details

Based on reverse-engineered .cls format from:
https://github.com/Equbuxu/CLSEncoderDecoder

### File Format Structure:

```
Signature:  SLCC + version (256)
Header:     Palette name (ASCII + UTF-8)
Colors:     RGBA values (4 bytes each)
```

### Color Format:
- **RGB**: 0-255 for each channel
- **Alpha**: Use 0 (transparent) or 255 (opaque)
  - CSP treats any non-zero alpha as fully opaque

## 💡 Quick Start Examples

### Web Tool Presets:
- 🌈 **Rainbow** - Classic 7-color spectrum
- 🍬 **Pastel** - Soft, dreamy colors
- ⚫ **Grayscale** - Black to white
- 🌍 **Earth Tones** - Natural browns and beiges
- 💡 **Neon** - Bright, vibrant colors
- 👤 **Skin Tones** - Various skin tone shades

### Python Script Examples:

```python
# Create from a list of hex codes
palette = CLSGenerator("Website Colors")
colors = ["#667eea", "#764ba2", "#f093fb", "#4facfe"]
for hex_code in colors:
    palette.add_color_from_hex(hex_code)
palette.save("website_colors.cls")

# Create programmatically
gradient = CLSGenerator("Blue Gradient")
for i in range(10):
    blue = int(255 * (i / 9))
    gradient.add_color(0, 0, blue)
gradient.save("blue_gradient.cls")

# Load and modify existing palette
existing = load_cls("rainbow.cls")
existing.add_color(255, 255, 255)  # Add white
existing.save("rainbow_plus_white.cls")
```

## 🎯 Use Cases

- **Game Development**: Create consistent color palettes for sprites
- **Web Design**: Match your website's color scheme
- **Art Projects**: Build custom palettes for illustrations
- **Animation**: Organize colors by character or scene
- **Pixel Art**: Create limited color palettes
- **Brand Colors**: Store your brand's color guidelines

## 🚀 Advanced Features

### Python Library Features:
- ✅ Create palettes from scratch
- ✅ Add colors via RGB or hex
- ✅ Load and modify existing .cls files
- ✅ Preview palettes in terminal
- ✅ Batch operations
- ✅ Color validation

### Web Tool Features:
- ✅ Visual color picker
- ✅ Hex code input
- ✅ Pre-built presets
- ✅ Live palette preview
- ✅ Click to remove colors
- ✅ Color count display
- ✅ One-click download

## 📝 File Compatibility

**Works with:**
- ✅ Clip Studio Paint (Windows, Mac, iPad)
- ✅ All CSP versions (Pro, EX)
- ✅ .cls format specification compliant

**Note:** The .cls format is specific to Clip Studio Paint. For other software:
- Photoshop uses .aco (Adobe Color)
- GIMP uses .gpl (GIMP Palette)
- Krita uses .kpl (Krita Palette)

## 🐛 Troubleshooting

**"CSP won't import my file"**
- Make sure the file extension is exactly `.cls`
- Verify you added at least one color
- Try renaming the palette (avoid special characters)

**"Colors look different in CSP"**
- Check your CSP color management settings
- Ensure you're using RGB mode, not CMYK

**"File is too large"**
- .cls files are very small (<1KB for most palettes)
- If unusually large, recreate the palette

## 📚 Resources

- **Format Specification**: https://github.com/Equbuxu/CLSEncoderDecoder
- **Clip Studio Paint**: https://www.clipstudio.net/
- **Color Picker Tools**: https://coolors.co, https://color.adobe.com

## 🤝 Contributing

Feel free to modify and extend these tools! The Python library is fully open and documented.

Ideas for extensions:
- Import from other palette formats
- Generate palettes from images
- Color theory based palette generation
- Palette optimization algorithms

---

Made with 🎨 for digital artists everywhere!

Last Updated: December 2024
