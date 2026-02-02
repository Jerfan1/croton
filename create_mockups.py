#!/usr/bin/env python3
"""
App Store Screenshot Generator
Creates 6.5" display mockups (1284 x 2778 pixels) with iPhone frame and marketing text.
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Paths
BASE_DIR = "/Users/jingi/Documents/Coding/strong-lifts"
MOCKUP_PATH = os.path.join(BASE_DIR, "iPhone 17.png")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "Screenshots")
OUTPUT_DIR = os.path.join(BASE_DIR, "AppStore_Screenshots")

# App Store 6.5" display dimensions
OUTPUT_WIDTH = 1284
OUTPUT_HEIGHT = 2778

# Screenshot configs: (filename_suffix, headline, subheadline)
SCREENSHOT_CONFIGS = [
    ("19.12.24", "4 Ways to\nProgress", "Not just linear"),
    ("19.17.29", "Ready When\nYou Are", "No nonsense. Just lift."),
    ("19.14.14", "Built-in\nRest Timer", "Tap. Rest. Repeat."),
    ("19.15.43", "Log Sets in\nOne Tap", "Simple set tracking"),
    ("19.18.11", "Choose Your\nProgram", "Or build your own"),
    ("19.18.50", "100+ Exercises\nBuilt In", "Everything you need"),
    ("19.22.46", "See Your\nGains", "Track your progress"),
]

# Colors - warm cream/beige background
BACKGROUND_COLOR = (253, 250, 243)  # Warm cream/beige
TEXT_COLOR = (17, 24, 39)  # Dark gray (#111827)
SUBTEXT_COLOR = (82, 82, 91)  # Darker gray for better readability
BUBBLE_COLOR = (255, 253, 250)  # Very slightly warm white bubble
BUBBLE_SHADOW = (0, 0, 0, 15)  # Very subtle shadow

def get_rounded_font(size):
    """Get a rounded, friendly font."""
    font_paths = [
        "/System/Library/Fonts/Supplemental/Avenir Next Rounded.ttc",
        "/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf",
        "/Library/Fonts/SF-Pro-Rounded-Bold.otf",
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/Supplemental/Avenir.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    
    return ImageFont.load_default()

def get_regular_font(size):
    """Get a regular font for subheadlines."""
    font_paths = [
        "/System/Library/Fonts/Supplemental/Avenir Next.ttc",
        "/Library/Fonts/SF-Pro-Display-Regular.otf",
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    
    return ImageFont.load_default()

def draw_rounded_rectangle(draw, coords, radius, fill, outline=None):
    """Draw a rounded rectangle."""
    x1, y1, x2, y2 = coords
    draw.rounded_rectangle(coords, radius=radius, fill=fill, outline=outline)

def create_mockup(screenshot_path, headline, subheadline, output_path):
    """Create a single App Store mockup."""
    
    # Create output canvas with softer background
    canvas = Image.new('RGB', (OUTPUT_WIDTH, OUTPUT_HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(canvas)
    
    # Load mockup frame
    mockup = Image.open(MOCKUP_PATH).convert('RGBA')
    
    # Load screenshot
    screenshot = Image.open(screenshot_path).convert('RGBA')
    
    # Mockup size - leave room for text
    max_mockup_height = int(OUTPUT_HEIGHT * 0.82)
    mockup_scale = max_mockup_height / mockup.height
    new_mockup_width = int(mockup.width * mockup_scale)
    new_mockup_height = int(mockup.height * mockup_scale)
    
    mockup_resized = mockup.resize((new_mockup_width, new_mockup_height), Image.LANCZOS)
    
    # Scale screenshot to fit inside the mockup frame
    screen_width = int(new_mockup_width * 0.885)
    screen_height = int(new_mockup_height * 0.955)
    
    screenshot_resized = screenshot.resize((screen_width, screen_height), Image.LANCZOS)
    
    # Position mockup centered horizontally, near bottom
    mockup_x = (OUTPUT_WIDTH - new_mockup_width) // 2
    mockup_y = OUTPUT_HEIGHT - new_mockup_height - 15
    
    # Position screenshot inside mockup
    screen_x = mockup_x + (new_mockup_width - screen_width) // 2
    screen_y = mockup_y + int(new_mockup_height * 0.022)
    
    # Paste screenshot first (behind the frame)
    canvas.paste(screenshot_resized, (screen_x, screen_y), screenshot_resized)
    
    # Paste mockup frame on top
    canvas.paste(mockup_resized, (mockup_x, mockup_y), mockup_resized)
    
    # Text settings - clean
    headline_font = get_rounded_font(125)
    subheadline_font = get_regular_font(54)
    
    # Calculate text dimensions
    headline_lines = headline.split('\n')
    total_headline_height = 0
    line_heights = []
    line_widths = []
    for line in headline_lines:
        line_bbox = draw.textbbox((0, 0), line, font=headline_font)
        h = line_bbox[3] - line_bbox[1]
        w = line_bbox[2] - line_bbox[0]
        line_heights.append(h)
        line_widths.append(w)
        total_headline_height += h + 12
    
    sub_bbox = draw.textbbox((0, 0), subheadline, font=subheadline_font)
    subheadline_height = sub_bbox[3] - sub_bbox[1]
    subheadline_width = sub_bbox[2] - sub_bbox[0]
    
    # BIGGER gap between headline and subheadline
    gap_between = 55
    
    total_text_height = total_headline_height + gap_between + subheadline_height
    text_area_height = mockup_y
    text_start_y = (text_area_height - total_text_height) // 2 + 20
    
    # Draw text bubble/card behind text
    bubble_padding_x = 60
    bubble_padding_y = 35
    max_line_width = max(line_widths + [subheadline_width])
    
    bubble_x1 = (OUTPUT_WIDTH - max_line_width) // 2 - bubble_padding_x
    bubble_y1 = text_start_y - bubble_padding_y
    bubble_x2 = (OUTPUT_WIDTH + max_line_width) // 2 + bubble_padding_x
    bubble_y2 = text_start_y + total_text_height + bubble_padding_y
    
    # Draw white bubble with rounded corners
    draw_rounded_rectangle(
        draw,
        (bubble_x1, bubble_y1, bubble_x2, bubble_y2),
        radius=30,
        fill=BUBBLE_COLOR
    )
    
    # Draw headline centered
    line_y = text_start_y
    for i, line in enumerate(headline_lines):
        line_width = line_widths[i]
        draw.text(
            ((OUTPUT_WIDTH - line_width) // 2, line_y),
            line,
            font=headline_font,
            fill=TEXT_COLOR
        )
        line_y += line_heights[i] + 12
    
    # Draw subheadline with bigger gap
    subheadline_y = line_y + gap_between - 12
    draw.text(
        ((OUTPUT_WIDTH - subheadline_width) // 2, subheadline_y),
        subheadline,
        font=subheadline_font,
        fill=SUBTEXT_COLOR
    )
    
    # Save
    canvas.save(output_path, 'PNG', quality=95)
    print(f"Created: {output_path}")

def main():
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Find and process each screenshot
    screenshots = sorted([f for f in os.listdir(SCREENSHOTS_DIR) if f.endswith('.png')])
    
    for i, (time_suffix, headline, subheadline) in enumerate(SCREENSHOT_CONFIGS):
        # Find matching screenshot
        matching = [s for s in screenshots if time_suffix in s]
        if not matching:
            print(f"Warning: No screenshot found for {time_suffix}")
            continue
        
        screenshot_path = os.path.join(SCREENSHOTS_DIR, matching[0])
        output_filename = f"{i+1:02d}_{headline.replace(chr(10), '_').replace(' ', '_')}.png"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        create_mockup(screenshot_path, headline, subheadline, output_path)
    
    print(f"\nDone! Screenshots saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
