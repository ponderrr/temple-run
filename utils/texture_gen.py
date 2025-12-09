"""
Procedural Texture Generator
Generates simple textures for the game assets to avoid API rate limits.
"""

from PIL import Image, ImageDraw
import random
import math
import os

ASSETS_DIR = 'assets'

def ensure_assets_dir():
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR)

def generate_track_texture():
    """Generate a stone paved path texture."""
    size = 512
    img = Image.new('RGB', (size, size), (100, 100, 100))
    draw = ImageDraw.Draw(img)
    
    # Draw stones
    rows = 8
    cols = 4
    w = size // cols
    h = size // rows
    
    for r in range(rows):
        for c in range(cols):
            x = c * w
            y = r * h
            
            # Randomize color slightly
            shade = random.randint(80, 120)
            color = (shade, shade, shade)
            
            # Draw stone with gap
            gap = 4
            draw.rectangle([x + gap, y + gap, x + w - gap, y + h - gap], fill=color)
            
    img.save(os.path.join(ASSETS_DIR, 'track_texture.png'))
    print("Generated track_texture.png")

def generate_wall_texture():
    """Generate a mossy stone wall texture."""
    size = 256
    img = Image.new('RGB', (size, size), (80, 80, 80))
    pixels = img.load()
    
    for x in range(size):
        for y in range(size):
            # Noise
            noise = random.randint(-20, 20)
            r = max(0, min(255, 80 + noise))
            g = max(0, min(255, 80 + noise))
            b = max(0, min(255, 80 + noise))
            
            # Moss
            if random.random() < 0.1:
                g = max(0, min(255, g + 50))
                
            pixels[x, y] = (r, g, b)
            
    img.save(os.path.join(ASSETS_DIR, 'wall_texture.png'))
    print("Generated wall_texture.png")

def generate_wood_texture():
    """Generate a wood grain texture."""
    size = 256
    img = Image.new('RGB', (size, size), (139, 69, 19))
    pixels = img.load()
    
    for x in range(size):
        for y in range(size):
            # Wood grain noise
            grain = math.sin(x * 0.1 + y * 0.02) * 20
            noise = random.randint(-10, 10)
            
            r = max(0, min(255, 139 + int(grain) + noise))
            g = max(0, min(255, 69 + int(grain) + noise))
            b = max(0, min(255, 19 + int(grain) + noise))
            
            pixels[x, y] = (r, g, b)
            
    img.save(os.path.join(ASSETS_DIR, 'wood_texture.png'))
    print("Generated wood_texture.png")

def generate_metal_texture():
    """Generate a rusted metal texture."""
    size = 256
    img = Image.new('RGB', (size, size), (100, 100, 110))
    pixels = img.load()
    
    for x in range(size):
        for y in range(size):
            noise = random.randint(-30, 30)
            
            # Rust spots
            if random.random() < 0.05:
                r = 150 + noise
                g = 50 + noise
                b = 50 + noise
            else:
                r = 100 + noise
                g = 100 + noise
                b = 110 + noise
                
            pixels[x, y] = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
            
    img.save(os.path.join(ASSETS_DIR, 'metal_texture.png'))
    print("Generated metal_texture.png")

def generate_orb_texture():
    """Generate a glowing orb texture."""
    size = 128
    img = Image.new('RGB', (size, size), (0, 0, 0))
    pixels = img.load()
    
    center = size // 2
    max_dist = size // 2
    
    for x in range(size):
        for y in range(size):
            dx = x - center
            dy = y - center
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist < max_dist:
                # Radial gradient
                intensity = 1.0 - (dist / max_dist)
                r = int(255 * intensity)
                g = int(215 * intensity) # Gold
                b = int(0 * intensity)
                pixels[x, y] = (r, g, b)
            else:
                pixels[x, y] = (0, 0, 0)
                
    img.save(os.path.join(ASSETS_DIR, 'orb_texture.png'))
    print("Generated orb_texture.png")

if __name__ == '__main__':
    ensure_assets_dir()
    generate_track_texture()
    generate_wall_texture()
    generate_wood_texture()
    generate_metal_texture()
    generate_orb_texture()
