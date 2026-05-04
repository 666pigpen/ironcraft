#!/usr/bin/env python3
"""
IronCraft texture generator.
Generates all PNG textures for the Iron Crafting Table block and GUI.
Uses only the Python standard library (zlib for compression).
Run from the project root: python3 generate_textures.py
"""

import os
import struct
import zlib


# ---------------------------------------------------------------------------
# Minimal PNG writer
# ---------------------------------------------------------------------------

def _png_chunk(chunk_type: bytes, data: bytes) -> bytes:
    length = struct.pack('>I', len(data))
    crc = struct.pack('>I', zlib.crc32(chunk_type + data) & 0xFFFFFFFF)
    return length + chunk_type + data + crc


def write_png(path: str, pixels: list, width: int, height: int, mode: str = 'RGBA') -> None:
    """
    Write a PNG file from a flat list of pixel tuples.
    pixels: list of (R,G,B,A) tuples if mode=='RGBA', or (R,G,B) if mode=='RGB'
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

    channels = 4 if mode == 'RGBA' else 3
    color_type = 6 if mode == 'RGBA' else 2  # 6=RGBA, 2=RGB

    # IHDR
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, color_type, 0, 0, 0)

    # Raw image data with filter byte 0 per scanline
    raw_rows = []
    for y in range(height):
        row_bytes = bytearray([0])  # filter byte
        for x in range(width):
            px = pixels[y * width + x]
            for c in range(channels):
                row_bytes.append(px[c])
        raw_rows.append(bytes(row_bytes))

    raw_data = b''.join(raw_rows)
    compressed = zlib.compress(raw_data, 9)

    # Assemble PNG
    signature = b'\x89PNG\r\n\x1a\n'
    png = (
        signature
        + _png_chunk(b'IHDR', ihdr_data)
        + _png_chunk(b'IDAT', compressed)
        + _png_chunk(b'IEND', b'')
    )
    with open(path, 'wb') as f:
        f.write(png)
    print(f"  Written: {path}")


# ---------------------------------------------------------------------------
# Color palette (industrial iron)
# ---------------------------------------------------------------------------

def hex_rgb(h: str) -> tuple:
    h = h.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def rgba(h: str, a: int = 255) -> tuple:
    r, g, b = hex_rgb(h)
    return (r, g, b, a)


# Core colors
C_SURFACE   = rgba('#787878')   # medium gray – main surface
C_LIGHT     = rgba('#b0b4b8')   # light highlight
C_SHADOW    = rgba('#404448')   # dark shadow
C_DARK      = rgba('#282c30')   # very dark accent / edge
C_MID       = rgba('#909490')   # medium mid-tone
C_BRIGHT    = rgba('#c8ccd0')   # brightest highlight
C_RIVET     = rgba('#5a5e62')   # rivet/bolt color
C_GRID_LINE = rgba('#383c40')   # grid line color (carved)
C_GRID_FILL = rgba('#4a4e52')   # carved grid recess fill
C_FRAME     = rgba('#343840')   # border frame


def make_canvas(w: int, h: int, color: tuple) -> list:
    return [color] * (w * h)


def set_pixel(pixels: list, w: int, x: int, y: int, color: tuple) -> None:
    if 0 <= x < w and 0 <= y < len(pixels) // w:
        pixels[y * w + x] = color


def fill_rect(pixels: list, w: int, x0: int, y0: int, x1: int, y1: int, color: tuple) -> None:
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            set_pixel(pixels, w, x, y, color)


def draw_h_line(pixels: list, w: int, x0: int, x1: int, y: int, color: tuple) -> None:
    for x in range(x0, x1 + 1):
        set_pixel(pixels, w, x, y, color)


def draw_v_line(pixels: list, w: int, x: int, y0: int, y1: int, color: tuple) -> None:
    for y in range(y0, y1 + 1):
        set_pixel(pixels, w, x, y, color)


def draw_border(pixels: list, w: int, h: int, x0: int, y0: int, x1: int, y1: int,
                light: tuple, dark: tuple) -> None:
    """Draw a raised-look border with light top/left and dark bottom/right."""
    draw_h_line(pixels, w, x0, x1, y0, light)
    draw_v_line(pixels, w, x0, y0, y1, light)
    draw_h_line(pixels, w, x0, x1, y1, dark)
    draw_v_line(pixels, w, x1, y0, y1, dark)


# ---------------------------------------------------------------------------
# Industrial iron surface pattern (shared by several faces)
# ---------------------------------------------------------------------------

def industrial_iron_surface(w: int = 16, h: int = 16) -> list:
    """
    Base industrial-iron surface: medium gray with subtle rivet/grid pattern.
    Mimics Create mod's industrial iron block aesthetic.
    """
    pixels = make_canvas(w, h, C_SURFACE)

    # Outer frame (1px dark border)
    draw_h_line(pixels, w, 0, w - 1, 0, C_DARK)
    draw_h_line(pixels, w, 0, w - 1, h - 1, C_DARK)
    draw_v_line(pixels, w, 0, 0, h - 1, C_DARK)
    draw_v_line(pixels, w, w - 1, 0, h - 1, C_DARK)

    # Inner highlight (top-left inside the frame)
    draw_h_line(pixels, w, 1, w - 2, 1, C_LIGHT)
    draw_v_line(pixels, w, 1, 1, h - 2, C_LIGHT)

    # Inner shadow (bottom-right inside the frame)
    draw_h_line(pixels, w, 1, w - 2, h - 2, C_SHADOW)
    draw_v_line(pixels, w, w - 2, 1, h - 2, C_SHADOW)

    # Subtle subdivision lines at x=8 and y=8 (very faint)
    for i in range(2, w - 2):
        # horizontal midline – slightly darker
        px = pixels[8 * w + i]
        pixels[8 * w + i] = tuple(max(0, c - 10) if j < 3 else c
                                   for j, c in enumerate(px))
    for j in range(2, h - 2):
        px = pixels[j * w + 8]
        pixels[j * w + 8] = tuple(max(0, c - 10) if k < 3 else c
                                   for k, c in enumerate(px))

    # Corner rivets at (3,3), (3,12), (12,3), (12,12)
    for rx, ry in [(3, 3), (3, 12), (12, 3), (12, 12)]:
        set_pixel(pixels, w, rx, ry, C_DARK)
        set_pixel(pixels, w, rx + 1, ry, C_BRIGHT)
        set_pixel(pixels, w, rx, ry + 1, C_BRIGHT)
        set_pixel(pixels, w, rx - 1, ry, C_SHADOW)
        set_pixel(pixels, w, rx, ry - 1, C_SHADOW)

    return pixels


# ---------------------------------------------------------------------------
# Texture 1: bottom face
# ---------------------------------------------------------------------------

def make_bottom() -> list:
    """Bottom face: plain industrial iron surface."""
    return industrial_iron_surface(16, 16)


# ---------------------------------------------------------------------------
# Texture 2: top face (3x3 crafting grid carved in)
# ---------------------------------------------------------------------------

def make_top() -> list:
    pixels = industrial_iron_surface(16, 16)

    # Draw a 3x3 carved grid across most of the face.
    # Grid cells: 3 cells × 3px wide = 9px, with 2 separators = 11px total
    # Centered: offset = (16 - 11) // 2 = 2
    # Cells start at 2, separator at 5, cell at 6, separator at 9, cell at 10
    # Each cell is 3×3 pixels; lines are 1px

    grid_x0 = 2
    grid_y0 = 2
    cell = 3
    sep = 1

    for row in range(3):
        for col in range(3):
            cx = grid_x0 + col * (cell + sep)
            cy = grid_y0 + row * (cell + sep)
            # Fill cell with dark recessed color
            fill_rect(pixels, 16, cx, cy, cx + cell - 1, cy + cell - 1, C_GRID_FILL)
            # Top/left shadow inside cell
            draw_h_line(pixels, 16, cx, cx + cell - 1, cy, C_DARK)
            draw_v_line(pixels, 16, cx, cy, cy + cell - 1, C_DARK)
            # Bottom/right highlight
            draw_h_line(pixels, 16, cx, cx + cell - 1, cy + cell - 1, C_MID)
            draw_v_line(pixels, 16, cx + cell - 1, cy, cy + cell - 1, C_MID)

    # Separator lines between cells (carved grooves)
    # Vertical separators at x = grid_x0 + cell  and  x = grid_x0 + 2*(cell+sep) - 1
    for col in range(1, 3):
        sx = grid_x0 + col * (cell + sep) - 1
        draw_v_line(pixels, 16, sx, grid_y0, grid_y0 + 3 * cell + 2 * sep - 1, C_GRID_LINE)

    for row in range(1, 3):
        sy = grid_y0 + row * (cell + sep) - 1
        draw_h_line(pixels, 16, grid_x0, grid_x0 + 3 * cell + 2 * sep - 1, sy, C_GRID_LINE)

    return pixels


# ---------------------------------------------------------------------------
# Texture 3: front face (industrial frame + simple tool icon)
# ---------------------------------------------------------------------------

def make_front() -> list:
    pixels = industrial_iron_surface(16, 16)

    # Draw an inner inset panel (sunken area) in the center
    fill_rect(pixels, 16, 3, 3, 12, 12, C_SHADOW)
    draw_border(pixels, 16, 16, 3, 3, 12, 12, C_DARK, C_MID)

    # Simple hammer icon in center of the inset panel (pixel art, 6×8 in the 10×10 area)
    # Hammer head at top, handle going down-right
    # Centered around (7,7) in the inset
    hammer = [
        # (x, y) relative to (4, 4) — drawing within the inset
        # Head (3×2)
        (0, 0), (1, 0), (2, 0),
        (0, 1), (1, 1), (2, 1),
        # Neck
        (1, 2),
        # Handle going diagonally
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 6),
    ]
    for hx, hy in hammer:
        set_pixel(pixels, 16, 4 + hx, 4 + hy, C_BRIGHT)
    # Highlight on head
    set_pixel(pixels, 16, 4, 4, C_LIGHT)

    # Gear/cog suggestion: two dots left and right of the panel center
    set_pixel(pixels, 16, 4, 7, C_MID)
    set_pixel(pixels, 16, 11, 7, C_MID)

    return pixels


# ---------------------------------------------------------------------------
# Texture 4: side face
# ---------------------------------------------------------------------------

def make_side() -> list:
    pixels = industrial_iron_surface(16, 16)

    # Inner inset panel (no tool icon, just industrial framing)
    fill_rect(pixels, 16, 3, 3, 12, 12, C_SHADOW)
    draw_border(pixels, 16, 16, 3, 3, 12, 12, C_DARK, C_MID)

    # A subtle horizontal mid-band to break up the face
    draw_h_line(pixels, 16, 4, 11, 7, C_MID)
    draw_h_line(pixels, 16, 4, 11, 8, C_GRID_LINE)

    # Bolts/rivets inside the panel corners
    for rx, ry in [(4, 4), (4, 11), (11, 4), (11, 11)]:
        set_pixel(pixels, 16, rx, ry, C_RIVET)

    return pixels


# ---------------------------------------------------------------------------
# Texture 5: GUI (256×256, active area 176×166)
# ---------------------------------------------------------------------------

# GUI color palette (slightly different shading for 2D interface)
GUI_BG          = (139, 142, 146, 255)   # #8b8e92 – main background
GUI_PANEL       = (128, 131, 135, 255)   # slightly darker panel
GUI_BORDER_DARK = (55,  57,  61,  255)   # #37393d
GUI_BORDER_MID  = (88,  91,  95,  255)   # #585b5f
GUI_BORDER_LITE = (198, 201, 205, 255)   # #c6c9cd
GUI_SLOT_BG     = (55,  57,  61,  255)   # slot interior dark
GUI_SLOT_LITE   = (198, 201, 205, 255)   # slot top/left highlight
GUI_SLOT_DARK   = (38,  40,  44,  255)   # slot bottom/right shadow
GUI_ARROW_FILL  = (160, 163, 167, 255)   # arrow body
GUI_ARROW_DARK  = (55,  57,  61,  255)   # arrow outline
GUI_TEXT_SHADOW = (55,  57,  61,  255)   # label shadow area
TRANSPARENT     = (0, 0, 0, 0)


def gui_set(pixels, W, x, y, color):
    if 0 <= x < W and 0 <= y < len(pixels) // W:
        pixels[y * W + x] = color


def gui_fill(pixels, W, x0, y0, x1, y1, color):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            gui_set(pixels, W, x, y, color)


def gui_hline(pixels, W, x0, x1, y, color):
    for x in range(x0, x1 + 1):
        gui_set(pixels, W, x, y, color)


def gui_vline(pixels, W, x, y0, y1, color):
    for y in range(y0, y1 + 1):
        gui_set(pixels, W, x, y, color)


def draw_slot(pixels, W, sx, sy):
    """
    Draw a single 18×18 slot at (sx, sy).
    The active area is 16×16 inside a 1px border.
    Vanilla slot: dark top/left, light bottom/right.
    """
    # Slot background
    gui_fill(pixels, W, sx + 1, sy + 1, sx + 16, sy + 16, GUI_SLOT_BG)
    # Top and left edges (dark/shadow – slot looks sunken)
    gui_hline(pixels, W, sx, sx + 17, sy,      GUI_SLOT_DARK)
    gui_vline(pixels, W, sx,          sy, sy + 17, GUI_SLOT_DARK)
    # Bottom and right edges (light highlight)
    gui_hline(pixels, W, sx, sx + 17, sy + 17, GUI_SLOT_LITE)
    gui_vline(pixels, W, sx + 17,     sy, sy + 17, GUI_SLOT_LITE)


def draw_arrow(pixels, W, ax, ay):
    """
    Draw a right-pointing arrow sprite at (ax, ay).
    Arrow is 22×16 px (vanilla dimensions).
    """
    # Arrow body (horizontal bar)
    gui_fill(pixels, W, ax, ay + 5, ax + 21, ay + 10, GUI_ARROW_FILL)

    # Arrowhead (triangle pointing right)
    for i in range(8):
        x_tip = ax + 14 + i
        y0 = ay + 7 - i
        y1 = ay + 8 + i
        if y0 < y1:
            gui_vline(pixels, W, x_tip, y0, y1, GUI_ARROW_FILL)

    # Outline – top
    gui_hline(pixels, W, ax,      ax + 21, ay + 4, GUI_ARROW_DARK)
    # Outline – bottom
    gui_hline(pixels, W, ax,      ax + 21, ay + 11, GUI_ARROW_DARK)
    # Outline – left (tail)
    gui_vline(pixels, W, ax,      ay + 4, ay + 11, GUI_ARROW_DARK)
    # Arrowhead outline
    for i in range(9):
        gui_set(pixels, W, ax + 13 + i, ay + 3 - i, GUI_ARROW_DARK)
        gui_set(pixels, W, ax + 13 + i, ay + 12 + i, GUI_ARROW_DARK)


def make_gui() -> list:
    W, H = 256, 256
    pixels = make_canvas(W, H, TRANSPARENT)

    # Active GUI area: 176×166, starts at (0,0)
    AW, AH = 176, 166

    # --- Background panel ---
    gui_fill(pixels, W, 0, 0, AW - 1, AH - 1, GUI_BG)

    # Outer border (2px raised)
    # Top & left (light)
    gui_hline(pixels, W, 0, AW - 1, 0, GUI_BORDER_LITE)
    gui_hline(pixels, W, 0, AW - 1, 1, GUI_BORDER_MID)
    gui_vline(pixels, W, 0, 0, AH - 1, GUI_BORDER_LITE)
    gui_vline(pixels, W, 1, 0, AH - 1, GUI_BORDER_MID)
    # Bottom & right (dark)
    gui_hline(pixels, W, 0, AW - 1, AH - 1, GUI_BORDER_DARK)
    gui_hline(pixels, W, 0, AW - 1, AH - 2, GUI_BORDER_MID)
    gui_vline(pixels, W, AW - 1, 0, AH - 1, GUI_BORDER_DARK)
    gui_vline(pixels, W, AW - 2, 0, AH - 1, GUI_BORDER_MID)

    # --- Crafting grid area ---
    # 3×3 grid of 18×18 slots, starting at (28, 16)
    # (The menu code uses 30+col*18, 17+row*18 for slot centers, so
    #  slot top-left = 30-1=29 ... but we match vanilla crafting table layout
    #  which puts the grid starting at x=29, y=16)
    GRID_X = 29
    GRID_Y = 16
    for row in range(3):
        for col in range(3):
            draw_slot(pixels, W, GRID_X + col * 18, GRID_Y + row * 18)

    # --- Arrow (crafting -> result) ---
    # Vanilla arrow at ~x=90, y=31 (22×16)
    ARROW_X = 88
    ARROW_Y = 31
    draw_arrow(pixels, W, ARROW_X, ARROW_Y)

    # --- Result slot (18×18, larger visual) ---
    # Vanilla result at x=124, y=35 (our menu uses 124,35)
    RESULT_X = 123
    RESULT_Y = 34
    # Draw a slightly larger framed box for the result (22×22)
    gui_fill(pixels, W, RESULT_X, RESULT_Y, RESULT_X + 23, RESULT_Y + 23, GUI_SLOT_BG)
    gui_hline(pixels, W, RESULT_X, RESULT_X + 23, RESULT_Y,      GUI_SLOT_DARK)
    gui_vline(pixels, W, RESULT_X, RESULT_Y, RESULT_Y + 23,      GUI_SLOT_DARK)
    gui_hline(pixels, W, RESULT_X, RESULT_X + 23, RESULT_Y + 23, GUI_SLOT_LITE)
    gui_vline(pixels, W, RESULT_X + 23, RESULT_Y, RESULT_Y + 23, GUI_SLOT_LITE)

    # --- Player inventory separator line ---
    # Thin horizontal rule separating crafting area from inventory
    INV_SEPARATOR_Y = 80
    gui_hline(pixels, W, 7, AW - 8, INV_SEPARATOR_Y,     GUI_BORDER_DARK)
    gui_hline(pixels, W, 7, AW - 8, INV_SEPARATOR_Y + 1, GUI_BORDER_LITE)

    # --- Player inventory slots: 3 rows × 9 cols at (7, 83) ---
    INV_X = 7
    INV_Y = 83
    for row in range(3):
        for col in range(9):
            draw_slot(pixels, W, INV_X + col * 18, INV_Y + row * 18)

    # --- Hotbar slots: 1 row × 9 cols at (7, 141) ---
    HOTBAR_Y = 141
    for col in range(9):
        draw_slot(pixels, W, INV_X + col * 18, HOTBAR_Y)

    # Subtle hotbar separator
    gui_hline(pixels, W, 7, AW - 8, HOTBAR_Y - 2, GUI_BORDER_DARK)
    gui_hline(pixels, W, 7, AW - 8, HOTBAR_Y - 1, GUI_BORDER_LITE)

    # --- Title label area: subtle darker strip at top ---
    gui_fill(pixels, W, 2, 2, AW - 3, 12, GUI_PANEL)

    # --- "Inventory" label area at inventory section ---
    gui_fill(pixels, W, 2, INV_Y - 12, AW - 3, INV_Y - 3, GUI_PANEL)

    return pixels


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

BLOCK_TEX_DIR = "src/main/resources/assets/ironcraft/textures/block"
GUI_TEX_DIR   = "src/main/resources/assets/ironcraft/textures/gui"


def main():
    print("Generating IronCraft textures...")

    # Block textures (16×16 RGBA)
    write_png(
        os.path.join(BLOCK_TEX_DIR, "iron_crafting_table_bottom.png"),
        make_bottom(), 16, 16, 'RGBA'
    )
    write_png(
        os.path.join(BLOCK_TEX_DIR, "iron_crafting_table_top.png"),
        make_top(), 16, 16, 'RGBA'
    )
    write_png(
        os.path.join(BLOCK_TEX_DIR, "iron_crafting_table_front.png"),
        make_front(), 16, 16, 'RGBA'
    )
    write_png(
        os.path.join(BLOCK_TEX_DIR, "iron_crafting_table_side.png"),
        make_side(), 16, 16, 'RGBA'
    )

    # GUI texture (256×256 RGBA)
    write_png(
        os.path.join(GUI_TEX_DIR, "iron_crafting_table.png"),
        make_gui(), 256, 256, 'RGBA'
    )

    print("Done! All textures generated.")
    print()
    print("Generated files:")
    print(f"  {BLOCK_TEX_DIR}/iron_crafting_table_bottom.png")
    print(f"  {BLOCK_TEX_DIR}/iron_crafting_table_top.png")
    print(f"  {BLOCK_TEX_DIR}/iron_crafting_table_front.png")
    print(f"  {BLOCK_TEX_DIR}/iron_crafting_table_side.png")
    print(f"  {GUI_TEX_DIR}/iron_crafting_table.png")


if __name__ == '__main__':
    main()
