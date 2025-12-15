#!/usr/bin/env python3
"""
MIT License
Copyright (c) 2021 Equbuxu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

CLS Color Set Generator for Clip Studio Paint
Based on the reverse-engineered format from: https://github.com/Equbuxu/CLSEncoderDecoder

Usage:
    generator = CLSGenerator("My Palette")
    generator.add_color(255, 0, 0, 255)  # Red
    generator.add_color(0, 255, 0, 255)  # Green
    generator.save("my_palette.cls")
"""

import struct
from typing import List, Tuple

class CLSColor:
    """Represents a single color in RGBA format"""
    def __init__(self, r: int, g: int, b: int, a: int = 255):
        """
        Create a color. Alpha should be either 0 (transparent) or 255 (opaque).
        CSP treats any non-zero alpha as fully opaque.
        
        Args:
            r: Red (0-255)
            g: Green (0-255)
            b: Blue (0-255)
            a: Alpha (0 or 255, default 255)
        """
        self.r = max(0, min(255, r))
        self.g = max(0, min(255, g))
        self.b = max(0, min(255, b))
        self.a = max(0, min(255, a))
    
    def __repr__(self):
        return f"CLSColor(R:{self.r}, G:{self.g}, B:{self.b}, A:{self.a})"
    
    def to_hex(self):
        """Return hex representation"""
        return f"#{self.r:02X}{self.g:02X}{self.b:02X}"

class CLSGenerator:
    """Generate .cls files for Clip Studio Paint"""
    
    def __init__(self, name: str = "Custom Palette"):
        """
        Initialize a new color set
        
        Args:
            name: Name of the color set (will appear in CSP)
        """
        self.name = name
        self.colors: List[CLSColor] = []
    
    def add_color(self, r: int, g: int, b: int, a: int = 255):
        """
        Add a color to the palette
        
        Args:
            r: Red (0-255)
            g: Green (0-255)
            b: Blue (0-255)
            a: Alpha (0 or 255, default 255)
        """
        color = CLSColor(r, g, b, a)
        self.colors.append(color)
        return self
    
    def add_color_from_hex(self, hex_color: str, a: int = 255):
        """
        Add a color from hex string
        
        Args:
            hex_color: Hex color like "#FF0000" or "FF0000"
            a: Alpha (0 or 255, default 255)
        """
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            self.add_color(r, g, b, a)
        elif len(hex_color) == 8:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            a = int(hex_color[6:8], 16)
            self.add_color(r, g, b, a)
        return self
    
    def add_colors_from_list(self, colors: List[Tuple[int, int, int]]):
        """
        Add multiple RGB colors from a list
        
        Args:
            colors: List of (R, G, B) tuples
        """
        for r, g, b in colors:
            self.add_color(r, g, b)
        return self
    
    def clear(self):
        """Remove all colors"""
        self.colors = []
        return self
    
    def save(self, filename: str):
        """
        Save the color set to a .cls file
        
        Args:
            filename: Output filename (should end with .cls)
        """
        with open(filename, 'wb') as f:
            # Write signature
            f.write(b'SLCC')
            f.write(struct.pack('<H', 256))  # int16, version marker
            
            # Prepare name strings
            ascii_name = self.name.encode('ascii', errors='replace')
            utf8_name = self.name.encode('utf-8')
            
            # Calculate header length
            header_length = (
                2 +                    # length of ASCII name field (int16)
                len(ascii_name) +      # ASCII name
                4 +                    # zero padding (int32)
                2 +                    # length of UTF-8 name field (int16)
                len(utf8_name)         # UTF-8 name
            )
            
            # Write header
            f.write(struct.pack('<I', header_length))  # int32
            f.write(struct.pack('<H', len(ascii_name)))  # int16
            f.write(ascii_name)
            f.write(struct.pack('<I', 0))  # int32 zero
            f.write(struct.pack('<H', len(utf8_name)))  # int16
            f.write(utf8_name)
            
            # Write colors section header
            f.write(struct.pack('<I', 4))  # int32, number of channels
            f.write(struct.pack('<I', len(self.colors)))  # int32, color count
            
            # Calculate colors data length
            colors_data_length = len(self.colors) * 12  # Each color is 12 bytes
            f.write(struct.pack('<I', colors_data_length))  # int32
            
            # Write each color
            for color in self.colors:
                f.write(struct.pack('<I', 8))  # int32, length of this color block
                f.write(struct.pack('BBBB', color.r, color.g, color.b, color.a))  # RGBA
                f.write(struct.pack('<I', 0))  # int32 trailing zero
        
        print(f"✓ Saved {len(self.colors)} colors to: {filename}")
        return filename
    
    def print_preview(self):
        """Print a preview of all colors"""
        print(f"\n{'='*60}")
        print(f"Color Set: {self.name}")
        print(f"Total Colors: {len(self.colors)}")
        print(f"{'='*60}\n")
        
        for i, color in enumerate(self.colors, 1):
            hex_code = color.to_hex()
            bar = '█' * 5
            print(f"{i:>3}. {hex_code} RGB({color.r:3}, {color.g:3}, {color.b:3}) {bar}")
        
        print(f"\n{'='*60}\n")


def load_cls(filename: str) -> 'CLSGenerator':
    """
    Load a .cls file and return a CLSGenerator object
    
    Args:
        filename: Path to .cls file
    
    Returns:
        CLSGenerator with loaded colors
    """
    with open(filename, 'rb') as f:
        # Read and verify signature
        sig = f.read(4)
        if sig != b'SLCC':
            raise ValueError("Invalid .cls file: wrong signature")
        
        version = struct.unpack('<H', f.read(2))[0]
        
        # Read header
        header_length = struct.unpack('<I', f.read(4))[0]
        
        # Read ASCII name
        ascii_name_len = struct.unpack('<H', f.read(2))[0]
        ascii_name = f.read(ascii_name_len).decode('ascii', errors='replace')
        
        # Skip zero padding
        f.read(4)
        
        # Read UTF-8 name
        utf8_name_len = struct.unpack('<H', f.read(2))[0]
        utf8_name = f.read(utf8_name_len).decode('utf-8', errors='replace')
        
        # Use UTF-8 name (CSP prefers this)
        generator = CLSGenerator(utf8_name or ascii_name)
        
        # Read colors section
        channels = struct.unpack('<I', f.read(4))[0]
        color_count = struct.unpack('<I', f.read(4))[0]
        colors_data_len = struct.unpack('<I', f.read(4))[0]
        
        # Read each color
        for _ in range(color_count):
            block_len = struct.unpack('<I', f.read(4))[0]
            r, g, b, a = struct.unpack('BBBB', f.read(4))
            trailing_zero = struct.unpack('<I', f.read(4))[0]
            
            generator.add_color(r, g, b, a)
    
    print(f"✓ Loaded {len(generator.colors)} colors from: {filename}")
    return generator


# Example usage and presets
if __name__ == "__main__":
    print("CLS Color Set Generator - Examples\n")
    
    # Example 1: Basic RGB colors
    print("Example 1: Creating a basic rainbow palette...")
    rainbow = CLSGenerator("Rainbow")
    rainbow.add_color(255, 0, 0)      # Red
    rainbow.add_color(255, 127, 0)    # Orange
    rainbow.add_color(255, 255, 0)    # Yellow
    rainbow.add_color(0, 255, 0)      # Green
    rainbow.add_color(0, 0, 255)      # Blue
    rainbow.add_color(75, 0, 130)     # Indigo
    rainbow.add_color(148, 0, 211)    # Violet
    rainbow.print_preview()
    rainbow.save("/home/claude/rainbow.cls")
    
    # Example 2: Using hex colors
    print("\nExample 2: Creating a pastel palette from hex codes...")
    pastels = CLSGenerator("Pastel Dreams")
    hex_colors = ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF"]
    for hex_code in hex_colors:
        pastels.add_color_from_hex(hex_code)
    pastels.print_preview()
    pastels.save("/home/claude/pastels.cls")
    
    # Example 3: Grayscale
    print("\nExample 3: Creating a grayscale palette...")
    grays = CLSGenerator("Grayscale")
    for i in range(0, 256, 32):
        grays.add_color(i, i, i)
    grays.print_preview()
    grays.save("/home/claude/grayscale.cls")
