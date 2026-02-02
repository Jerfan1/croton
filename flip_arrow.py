#!/usr/bin/env python3
"""
1. Flip the arrow from pointing down to pointing up
2. Move it from below the barbell to above
3. Clean fill the old position
"""

from PIL import Image
import os

ASSETS_DIR = "/Users/jingi/Documents/Coding/strong-lifts/ProgressiveFit/assets"
ICONS = ['icon.png', 'adaptive-icon.png', 'favicon.png', 'splash-icon.png']

def process_icon(img):
    """Flip arrow and move it above the barbell."""
    width, height = img.size
    
    # Arrow coordinates (where it currently is - bottom, pointing down)
    arrow_left = int(width * 0.38)
    arrow_right = int(width * 0.62)
    arrow_old_top = int(height * 0.65)
    arrow_old_bottom = int(height * 0.92)
    
    # Extract the arrow
    arrow_region = img.crop((arrow_left, arrow_old_top, arrow_right, arrow_old_bottom))
    
    # Flip it vertically (so it points up)
    arrow_flipped = arrow_region.transpose(Image.FLIP_TOP_BOTTOM)
    
    # Fill old area by sampling neighboring background colors
    for x in range(arrow_left, arrow_right):
        for y in range(arrow_old_top, arrow_old_bottom):
            # Sample from left and right edges, blend based on x position
            left_sample_x = max(0, arrow_left - 15)
            right_sample_x = min(width - 1, arrow_right + 15)
            
            left_color = img.getpixel((left_sample_x, y))
            right_color = img.getpixel((right_sample_x, y))
            
            t = (x - arrow_left) / (arrow_right - arrow_left)
            blended = tuple(int(left_color[i] * (1 - t) + right_color[i] * t) for i in range(4))
            img.putpixel((x, y), blended)
    
    # New position: above the barbell
    new_top = int(height * 0.12)
    
    # Paste the flipped arrow at new position
    img.paste(arrow_flipped, (arrow_left, new_top), arrow_flipped)
    
    return img

def main():
    for icon_name in ICONS:
        icon_path = os.path.join(ASSETS_DIR, icon_name)
        
        if not os.path.exists(icon_path):
            print(f"Skipping {icon_name} - not found")
            continue
        
        img = Image.open(icon_path).convert('RGBA')
        img = process_icon(img)
        img.save(icon_path, 'PNG')
        print(f"Updated: {icon_name}")
    
    print("\nDone! Arrow now points UP and is ABOVE the barbell")

if __name__ == "__main__":
    main()
