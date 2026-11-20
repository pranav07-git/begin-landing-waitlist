import math
import random

random.seed(42)

def bezier_pt(p0, p1, p2, p3, t):
    it = 1 - t
    x = it**3 * p0[0] + 3 * it**2 * t * p1[0] + 3 * it * t**2 * p2[0] + t**3 * p3[0]
    y = it**3 * p0[1] + 3 * it**2 * t * p1[1] + 3 * it * t**2 * p2[1] + t**3 * p3[1]
    return (x, y)

def bezier_tangent(p0, p1, p2, p3, t):
    it = 1 - t
    dx = 3 * it**2 * (p1[0] - p0[0]) + 6 * it * t * (p2[0] - p1[0]) + 3 * t**2 * (p3[0] - p2[0])
    dy = 3 * it**2 * (p1[1] - p0[1]) + 6 * it * t * (p2[1] - p1[1]) + 3 * t**2 * (p3[1] - p2[1])
    return math.degrees(math.atan2(dy, dx))

def make_leaf(cx, cy, angle_deg, length, width, fill="#070809", opacity=1.0):
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    tip_x = cx + length * cos_a
    tip_y = cy + length * sin_a
    side_rad1 = math.radians(angle_deg - 45)
    side_rad2 = math.radians(angle_deg + 45)
    cp1_x = cx + width * math.cos(side_rad1) + (length * 0.42) * cos_a
    cp1_y = cy + width * math.sin(side_rad1) + (length * 0.42) * sin_a
    cp2_x = cx + width * math.cos(side_rad2) + (length * 0.42) * cos_a
    cp2_y = cy + width * math.sin(side_rad2) + (length * 0.42) * sin_a
    # leaf spine line
    spine = f'<path d="M {cx:.1f},{cy:.1f} L {tip_x:.1f},{tip_y:.1f}" stroke="#161b24" stroke-width="0.75" stroke-opacity="0.6"/>'
    leaf = f'<path d="M {cx:.1f},{cy:.1f} Q {cp1_x:.1f},{cp1_y:.1f} {tip_x:.1f},{tip_y:.1f} Q {cp2_x:.1f},{cp2_y:.1f} {cx:.1f},{cy:.1f} Z" fill="{fill}" fill-opacity="{opacity}"/>'
    return f'{leaf}\n{spine}'

def make_tapered_branch(p0, p1, p2, p3, start_w, end_w, steps=25, fill="#070809"):
    # Generates a smooth polygon tapering from start_w to end_w along cubic bezier
    pts_left = []
    pts_right = []
    for i in range(steps + 1):
        t = i / steps
        pt = bezier_pt(p0, p1, p2, p3, t)
        ang = bezier_tangent(p0, p1, p2, p3, t)
        norm_ang = math.radians(ang + 90)
        w = (start_w * (1 - t) + end_w * t) / 2.0
        
        dx = w * math.cos(norm_ang)
        dy = w * math.sin(norm_ang)
        
        pts_left.append((pt[0] - dx, pt[1] - dy))
        pts_right.append((pt[0] + dx, pt[1] + dy))
        
    pts_poly = pts_left + list(reversed(pts_right))
    d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts_poly) + " Z"
    return f'<path d="{d}" fill="{fill}"/>'

def make_tendril(start_pt, curl_dir=1, scale=1.0, stroke="#070809", stroke_w=2.2):
    x, y = start_pt
    p1 = (x + 18 * curl_dir * scale, y + 25 * scale)
    p2 = (x + 32 * curl_dir * scale, y + 50 * scale)
    p3 = (x + 22 * curl_dir * scale, y + 75 * scale)
    p4 = (x + 8 * curl_dir * scale, y + 85 * scale)
    p5 = (x + 2 * curl_dir * scale, y + 80 * scale)
    p6 = (x + 10 * curl_dir * scale, y + 74 * scale)
    d = f"M {x:.1f},{y:.1f} C {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f} {p3[0]:.1f},{p3[1]:.1f} C {p4[0]:.1f},{p4[1]:.1f} {p5[0]:.1f},{p5[1]:.1f} {p6[0]:.1f},{p6[1]:.1f}"
    return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{stroke_w}" stroke-linecap="round" stroke-opacity="0.95"/>'

def generate_vines_svg():
    elements = []
    
    # 1. TOP-LEFT CORNER VINES
    # Deep shadow branches first (background layer)
    tl_curves_bg = [
        ((-30, -30), (120, 80), (280, 160), (450, 150), 32, 10, "#030405", 0.9),
        ((180, 120), (220, 240), (200, 360), (160, 480), 16, 4, "#030405", 0.85),
        ((-20, 180), (80, 280), (110, 420), (70, 560), 18, 5, "#030405", 0.85),
    ]
    for p0, p1, p2, p3, sw, ew, col, op in tl_curves_bg:
        elements.append(make_tapered_branch(p0, p1, p2, p3, sw, ew, steps=20, fill=col))
    
    # Foreground primary branches
    tl_curves = [
        ((-40, -40), (160, 60), (340, 110), (560, 90), 40, 12, "#090c10", 1.0),
        ((220, 85), (280, 190), (320, 280), (260, 410), 22, 6, "#090c10", 1.0),
        ((350, 105), (420, 170), (480, 220), (540, 200), 15, 4, "#0e131a", 1.0),
        ((-20, 110), (90, 190), (130, 320), (110, 460), 24, 7, "#090c10", 1.0),
        ((110, 460), (90, 560), (130, 640), (95, 740), 9, 3, "#0e131a", 1.0),
        ((120, -20), (240, 40), (380, 50), (480, 25), 18, 5, "#090c10", 1.0),
    ]
    for p0, p1, p2, p3, sw, ew, col, op in tl_curves:
        elements.append(make_tapered_branch(p0, p1, p2, p3, sw, ew, steps=25, fill=col))
        
        # Add leaves along branches
        num_leaves = int(sw * 1.2)
        for i in range(num_leaves):
            t = random.uniform(0.08, 0.95)
            pt = bezier_pt(p0, p1, p2, p3, t)
            tang = bezier_tangent(p0, p1, p2, p3, t)
            side = 1 if i % 2 == 0 else -1
            ang = tang + side * random.uniform(50, 95)
            length = random.uniform(22, 48)
            width = length * random.uniform(0.38, 0.52)
            fill_col = random.choice(["#070809", "#0c1015", "#121720"])
            elements.append(make_leaf(pt[0], pt[1], ang, length, width, fill=fill_col))
            
    # Add tendrils on top-left
    tl_tendrils = [
        ((260, 410), 1, 1.2),
        ((160, 480), -1, 1.0),
        ((95, 740), -1, 0.9),
        ((540, 200), 1, 1.1),
        ((480, 25), 1, 0.8),
        ((320, 280), -1, 1.0),
    ]
    for pt, cdir, sc in tl_tendrils:
        elements.append(make_tendril(pt, curl_dir=cdir, scale=sc, stroke="#0c1015"))
        # small leaf at end of tendril
        elements.append(make_leaf(pt[0] + 15 * cdir * sc, pt[1] + 65 * sc, 90 + cdir * 30, 18 * sc, 8 * sc, fill="#070809"))

    # 2. TOP-RIGHT CORNER VINES
    tr_curves_bg = [
        ((1950, -30), (1800, 80), (1640, 160), (1470, 150), 32, 10, "#030405", 0.9),
        ((1740, 120), (1700, 240), (1720, 360), (1760, 480), 16, 4, "#030405", 0.85),
        ((1940, 180), (1840, 280), (1810, 420), (1850, 560), 18, 5, "#030405", 0.85),
    ]
    for p0, p1, p2, p3, sw, ew, col, op in tr_curves_bg:
        elements.append(make_tapered_branch(p0, p1, p2, p3, sw, ew, steps=20, fill=col))

    tr_curves = [
        ((1960, -40), (1760, 60), (1580, 110), (1360, 90), 40, 12, "#090c10", 1.0),
        ((1700, 85), (1640, 190), (1600, 280), (1660, 410), 22, 6, "#090c10", 1.0),
        ((1570, 105), (1500, 170), (1440, 220), (1380, 200), 15, 4, "#0e131a", 1.0),
        ((1940, 110), (1830, 190), (1790, 320), (1810, 460), 24, 7, "#090c10", 1.0),
        ((1810, 460), (1830, 560), (1790, 640), (1825, 740), 9, 3, "#0e131a", 1.0),
        ((1800, -20), (1680, 40), (1540, 50), (1440, 25), 18, 5, "#090c10", 1.0),
    ]
    for p0, p1, p2, p3, sw, ew, col, op in tr_curves:
        elements.append(make_tapered_branch(p0, p1, p2, p3, sw, ew, steps=25, fill=col))
        
        num_leaves = int(sw * 1.2)
        for i in range(num_leaves):
            t = random.uniform(0.08, 0.95)
            pt = bezier_pt(p0, p1, p2, p3, t)
            tang = bezier_tangent(p0, p1, p2, p3, t)
            side = 1 if i % 2 == 0 else -1
            ang = tang + side * random.uniform(50, 95)
            length = random.uniform(22, 48)
            width = length * random.uniform(0.38, 0.52)
            fill_col = random.choice(["#070809", "#0c1015", "#121720"])
            elements.append(make_leaf(pt[0], pt[1], ang, length, width, fill=fill_col))
            
    tr_tendrils = [
        ((1660, 410), -1, 1.2),
        ((1760, 480), 1, 1.0),
        ((1825, 740), 1, 0.9),
        ((1380, 200), -1, 1.1),
        ((1440, 25), -1, 0.8),
        ((1600, 280), 1, 1.0),
    ]
    for pt, cdir, sc in tr_tendrils:
        elements.append(make_tendril(pt, curl_dir=cdir, scale=sc, stroke="#0c1015"))
        elements.append(make_leaf(pt[0] + 15 * cdir * sc, pt[1] + 65 * sc, 90 + cdir * 30, 18 * sc, 8 * sc, fill="#070809"))

    # 3. BOTTOM-LEFT CORNER VINES (Subtle low climbing foliage)
    bl_curves = [
        ((-30, 1110), (90, 1030), (220, 960), (360, 990), 28, 8, "#090c10", 1.0),
        ((140, 1000), (190, 920), (240, 850), (210, 780), 14, 4, "#0e131a", 1.0),
        ((-20, 980), (60, 920), (110, 830), (80, 750), 16, 4, "#090c10", 1.0),
    ]
    for p0, p1, p2, p3, sw, ew, col, op in bl_curves:
        elements.append(make_tapered_branch(p0, p1, p2, p3, sw, ew, steps=20, fill=col))
        for i in range(int(sw * 0.9)):
            t = random.uniform(0.1, 0.92)
            pt = bezier_pt(p0, p1, p2, p3, t)
            tang = bezier_tangent(p0, p1, p2, p3, t)
            side = 1 if i % 2 == 0 else -1
            ang = tang + side * random.uniform(50, 90)
            length = random.uniform(20, 38)
            elements.append(make_leaf(pt[0], pt[1], ang, length, length * 0.45, fill="#0c1015"))

    # 4. BOTTOM-RIGHT CORNER VINES (Subtle low climbing foliage)
    br_curves = [
        ((1950, 1110), (1830, 1030), (1700, 960), (1560, 990), 28, 8, "#090c10", 1.0),
        ((1780, 1000), (1730, 920), (1680, 850), (1710, 780), 14, 4, "#0e131a", 1.0),
        ((1940, 980), (1860, 920), (1810, 830), (1840, 750), 16, 4, "#090c10", 1.0),
    ]
    for p0, p1, p2, p3, sw, ew, col, op in br_curves:
        elements.append(make_tapered_branch(p0, p1, p2, p3, sw, ew, steps=20, fill=col))
        for i in range(int(sw * 0.9)):
            t = random.uniform(0.1, 0.92)
            pt = bezier_pt(p0, p1, p2, p3, t)
            tang = bezier_tangent(p0, p1, p2, p3, t)
            side = 1 if i % 2 == 0 else -1
            ang = tang + side * random.uniform(50, 90)
            length = random.uniform(20, 38)
            elements.append(make_leaf(pt[0], pt[1], ang, length, length * 0.45, fill="#0c1015"))

    content = "\n".join(elements)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" class="w-full h-full pointer-events-none" style="display:block;">
  <g>
{content}
  </g>
</svg>"""
    return svg

def generate_clouds_svg():
    # Billowing clouds using pure SVG gradients without heavy filter blurs for ultra-smooth 120fps performance
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" class="w-full h-full pointer-events-none" style="display:block;">
  <defs>
    <!-- Deep obsidian atmospheric gradients -->
    <linearGradient id="cloud-grad-bottom" x1="0%" y1="100%" x2="0%" y2="0%">
      <stop offset="0%" stop-color="#070809" stop-opacity="0.98"/>
      <stop offset="50%" stop-color="#0a0d12" stop-opacity="0.80"/>
      <stop offset="80%" stop-color="#121720" stop-opacity="0.30"/>
      <stop offset="100%" stop-color="#121720" stop-opacity="0"/>
    </linearGradient>

    <radialGradient id="cloud-grad-bl" cx="0%" cy="100%" r="85%">
      <stop offset="0%" stop-color="#070809" stop-opacity="0.98"/>
      <stop offset="45%" stop-color="#0b0e14" stop-opacity="0.85"/>
      <stop offset="75%" stop-color="#151b26" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#151b26" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="cloud-grad-br" cx="100%" cy="100%" r="85%">
      <stop offset="0%" stop-color="#070809" stop-opacity="0.98"/>
      <stop offset="45%" stop-color="#0b0e14" stop-opacity="0.85"/>
      <stop offset="75%" stop-color="#151b26" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#151b26" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="cloud-grad-tl" cx="0%" cy="0%" r="75%">
      <stop offset="0%" stop-color="#070809" stop-opacity="0.94"/>
      <stop offset="40%" stop-color="#0b0e14" stop-opacity="0.75"/>
      <stop offset="70%" stop-color="#151b26" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#151b26" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="cloud-grad-tr" cx="100%" cy="0%" r="75%">
      <stop offset="0%" stop-color="#070809" stop-opacity="0.94"/>
      <stop offset="40%" stop-color="#0b0e14" stop-opacity="0.75"/>
      <stop offset="70%" stop-color="#151b26" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#151b26" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- Ambient mist in corners & bottom -->
  <g>
    <!-- Top-left mist -->
    <ellipse cx="140" cy="110" rx="420" ry="280" fill="url(#cloud-grad-tl)"/>
    <!-- Top-right mist -->
    <ellipse cx="1780" cy="110" rx="420" ry="280" fill="url(#cloud-grad-tr)"/>
    <!-- Bottom-left cloud bank -->
    <ellipse cx="180" cy="980" rx="600" ry="380" fill="url(#cloud-grad-bl)"/>
    <!-- Bottom-right cloud bank -->
    <ellipse cx="1740" cy="980" rx="600" ry="380" fill="url(#cloud-grad-br)"/>
    <!-- Center bottom fog horizon -->
    <ellipse cx="960" cy="1080" rx="950" ry="260" fill="url(#cloud-grad-bottom)"/>
  </g>

  <!-- Multi-layered cloud curves with organic bezier profiles -->
  <g>
    <!-- Bottom Left billows -->
    <path d="M -60,1100 C -40,920 80,860 180,880 C 240,820 380,800 460,870 C 520,840 620,870 660,940 C 720,960 780,1020 800,1100 Z" fill="url(#cloud-grad-bl)"/>
    <!-- Bottom Right billows -->
    <path d="M 1980,1100 C 1960,920 1840,860 1740,880 C 1680,820 1540,800 1460,870 C 1400,840 1300,870 1260,940 C 1200,960 1140,1020 1120,1100 Z" fill="url(#cloud-grad-br)"/>
    <!-- Top Left soft puff -->
    <path d="M -60,-40 C 60,-30 180,10 240,90 C 310,60 410,90 440,170 C 400,240 280,280 180,270 C 80,310 -30,280 -60,220 Z" fill="url(#cloud-grad-tl)" opacity="0.88"/>
    <!-- Top Right soft puff -->
    <path d="M 1980,-40 C 1860,-30 1740,10 1680,90 C 1610,60 1510,90 1480,170 C 1520,240 1640,280 1740,270 C 1840,310 1950,280 1980,220 Z" fill="url(#cloud-grad-tr)" opacity="0.88"/>
  </g>

  <!-- Rolling cloud crest along bottom edge -->
  <path d="M -40,1080 Q 240,970 520,1020 T 1080,1000 T 1640,1010 T 1960,1080 L 1960,1120 L -40,1120 Z" fill="#070809" opacity="0.96"/>
</svg>"""
    return svg

def generate_combined_svg(vines_svg, clouds_svg):
    vines_core = vines_svg[vines_svg.find("<g>"):vines_svg.rfind("</svg>")]
    clouds_defs = clouds_svg[clouds_svg.find("<defs>"):clouds_svg.find("</defs>") + 7]
    clouds_body = clouds_svg[clouds_svg.find("</defs>") + 7:clouds_svg.rfind("</svg>")]
    
    combined = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" class="w-full h-full pointer-events-none" style="display:block;">
{clouds_defs}

  <!-- Atmospheric clouds layer -->
{clouds_body}

  <!-- Dark silhouetted foliage and tree vines -->
{vines_core}
</svg>"""
    return combined

vines = generate_vines_svg()
with open("corner-vines.svg", "w", encoding="utf-8") as f:
    f.write(vines)
print("Saved corner-vines.svg, size:", len(vines))

clouds = generate_clouds_svg()
with open("corner-clouds.svg", "w", encoding="utf-8") as f:
    f.write(clouds)
print("Saved corner-clouds.svg, size:", len(clouds))

combined = generate_combined_svg(vines, clouds)
with open("corner-frame-combined.svg", "w", encoding="utf-8") as f:
    f.write(combined)
print("Saved corner-frame-combined.svg, size:", len(combined))
