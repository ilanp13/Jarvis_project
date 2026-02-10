#!/usr/bin/env python3
"""
Generate Jarvis-style animation frames (Iron Man AI aesthetic).
Creates a glowing blue arc reactor / orb animation with rotating rings.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFilter

# Frame config - match existing deus frames
WIDTH, HEIGHT = 470, 360
NUM_FRAMES = 601
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jarvis_frames_transparent")

# Colors (RGBA)
CORE_COLOR = (100, 200, 255)       # Light cyan core
RING_COLOR = (60, 160, 255)        # Blue ring
OUTER_RING_COLOR = (40, 120, 220)  # Darker blue outer ring
GLOW_COLOR = (80, 180, 255)        # Glow
ACCENT_COLOR = (140, 220, 255)     # Bright accent
DIM_ACCENT = (30, 90, 180)         # Dim blue for subtle elements


def draw_arc_segment(draw, cx, cy, radius, start_angle, end_angle, width, color_rgba):
    """Draw an arc segment."""
    bbox = [cx - radius, cy - radius, cx + radius, cy + radius]
    draw.arc(bbox, start_angle, end_angle, fill=color_rgba, width=width)


def draw_ring_segments(draw, cx, cy, radius, rotation, num_segments, gap_degrees, width, color_rgba):
    """Draw evenly spaced arc segments forming a broken ring."""
    segment_degrees = (360 / num_segments) - gap_degrees
    for i in range(num_segments):
        start = rotation + i * (360 / num_segments)
        end = start + segment_degrees
        draw_arc_segment(draw, cx, cy, radius, start, end, width, color_rgba)


def draw_tick_marks(draw, cx, cy, radius, rotation, num_ticks, tick_len, color_rgba):
    """Draw small radial tick marks around a circle."""
    for i in range(num_ticks):
        angle = math.radians(rotation + i * (360 / num_ticks))
        x1 = cx + (radius - tick_len) * math.cos(angle)
        y1 = cy + (radius - tick_len) * math.sin(angle)
        x2 = cx + radius * math.cos(angle)
        y2 = cy + radius * math.sin(angle)
        draw.line([(x1, y1), (x2, y2)], fill=color_rgba, width=1)


def lerp(a, b, t):
    return a + (b - a) * t


def pulse(frame, period, min_val=0.0, max_val=1.0):
    """Sinusoidal pulse between min and max."""
    t = (math.sin(2 * math.pi * frame / period) + 1) / 2
    return lerp(min_val, max_val, t)


def generate_frame(frame_idx):
    """Generate a single Jarvis animation frame."""
    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = WIDTH // 2, HEIGHT // 2

    # Pulsing values
    core_pulse = pulse(frame_idx, 90, 0.6, 1.0)
    ring1_pulse = pulse(frame_idx, 120, 0.5, 1.0)
    ring2_pulse = pulse(frame_idx, 150, 0.4, 0.9)
    glow_pulse = pulse(frame_idx, 80, 0.3, 0.8)

    # Rotation angles (degrees)
    rot_inner = (frame_idx * 1.2) % 360
    rot_mid = -(frame_idx * 0.8) % 360
    rot_outer = (frame_idx * 0.5) % 360
    rot_ticks = (frame_idx * 0.3) % 360

    # === Layer 1: Outer glow (drawn on separate image for blur) ===
    glow_img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)

    glow_alpha = int(60 * glow_pulse)
    glow_r = 130
    glow_draw.ellipse(
        [cx - glow_r, cy - glow_r, cx + glow_r, cy + glow_r],
        fill=(*GLOW_COLOR, glow_alpha)
    )
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(radius=40))
    img = Image.alpha_composite(img, glow_img)
    draw = ImageDraw.Draw(img)

    # === Layer 2: Outer ring segments (radius ~120) ===
    r_outer = 120
    alpha_outer = int(180 * ring2_pulse)
    draw_ring_segments(draw, cx, cy, r_outer, rot_outer, 6, 15, 2, (*OUTER_RING_COLOR, alpha_outer))

    # Tick marks on outer ring
    tick_alpha = int(120 * ring2_pulse)
    draw_tick_marks(draw, cx, cy, r_outer + 8, rot_ticks, 36, 5, (*DIM_ACCENT, tick_alpha))

    # === Layer 3: Middle ring segments (radius ~90) ===
    r_mid = 90
    alpha_mid = int(200 * ring1_pulse)
    draw_ring_segments(draw, cx, cy, r_mid, rot_mid, 4, 20, 3, (*RING_COLOR, alpha_mid))

    # Small dots at segment endpoints on middle ring
    segment_deg = (360 / 4) - 20
    for i in range(4):
        start_a = rot_mid + i * 90
        end_a = start_a + segment_deg
        for angle_deg in [start_a, end_a]:
            angle = math.radians(angle_deg)
            dx = cx + r_mid * math.cos(angle)
            dy = cy + r_mid * math.sin(angle)
            dot_alpha = int(220 * ring1_pulse)
            draw.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=(*ACCENT_COLOR, dot_alpha))

    # === Layer 4: Inner ring (radius ~55) ===
    r_inner = 55
    alpha_inner = int(220 * ring1_pulse)
    draw_ring_segments(draw, cx, cy, r_inner, rot_inner, 3, 30, 2, (*RING_COLOR, alpha_inner))

    # === Layer 5: Core glow ===
    core_glow_img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    core_glow_draw = ImageDraw.Draw(core_glow_img)

    core_glow_r = 40
    core_glow_alpha = int(100 * core_pulse)
    core_glow_draw.ellipse(
        [cx - core_glow_r, cy - core_glow_r, cx + core_glow_r, cy + core_glow_r],
        fill=(*CORE_COLOR, core_glow_alpha)
    )
    core_glow_img = core_glow_img.filter(ImageFilter.GaussianBlur(radius=20))
    img = Image.alpha_composite(img, core_glow_img)
    draw = ImageDraw.Draw(img)

    # === Layer 6: Core circle ===
    core_r = 20
    core_alpha = int(240 * core_pulse)
    draw.ellipse(
        [cx - core_r, cy - core_r, cx + core_r, cy + core_r],
        fill=(*CORE_COLOR, core_alpha)
    )

    # Inner core bright spot
    spot_r = 8
    spot_alpha = int(255 * core_pulse)
    draw.ellipse(
        [cx - spot_r, cy - spot_r, cx + spot_r, cy + spot_r],
        fill=(200, 240, 255, spot_alpha)
    )

    # === Layer 7: Thin connecting lines from core to inner ring ===
    num_lines = 6
    line_alpha = int(80 * core_pulse)
    for i in range(num_lines):
        angle = math.radians(rot_inner + i * (360 / num_lines))
        x_end = cx + r_inner * math.cos(angle)
        y_end = cy + r_inner * math.sin(angle)
        draw.line([(cx, cy), (x_end, y_end)], fill=(*DIM_ACCENT, line_alpha), width=1)

    # === Layer 8: Floating particles ===
    num_particles = 8
    for i in range(num_particles):
        p_angle = math.radians((frame_idx * 0.7 + i * 45) % 360)
        p_radius = 100 + 20 * math.sin(frame_idx * 0.05 + i)
        px = cx + p_radius * math.cos(p_angle)
        py = cy + p_radius * math.sin(p_angle)
        p_alpha = int(150 * pulse(frame_idx + i * 30, 60, 0.2, 1.0))
        p_size = 2
        draw.ellipse([px - p_size, py - p_size, px + p_size, py + p_size],
                      fill=(*ACCENT_COLOR, p_alpha))

    return img


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Generating {NUM_FRAMES} Jarvis frames at {WIDTH}x{HEIGHT}...")

    for i in range(NUM_FRAMES):
        frame = generate_frame(i)
        filename = f"frame_{i + 1:04d}.png"
        frame.save(os.path.join(OUTPUT_DIR, filename), "PNG")

        if (i + 1) % 100 == 0 or i == 0:
            print(f"  Generated {i + 1}/{NUM_FRAMES} frames")

    print(f"Done! Frames saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
