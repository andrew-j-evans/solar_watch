from PIL import Image
import math
import ephem
from datetime import datetime, timezone, timedelta


# --- Configuration ---
BACKGROUND = "Images/WatchBackground.png"
OUTPUT     = "output.png"
PLANET_SCALE = 0.15

CST = timezone(timedelta(hours=-5))

PLANETS = [
    {"name": "Sun",      "radius": 0,   "scale": 0.36},
    {"name": "Mercury",  "radius": 70,  "scale": 0.19},
    {"name": "Venus",    "radius": 118, "scale": 0.2},
    {"name": "Earth",    "radius": 217, "scale": 0.37},
    {"name": "Mars",     "radius": 319, "scale": 0.3},
    {"name": "Jupiter",  "radius": 404, "scale": 0.4},
    {"name": "Saturn",   "radius": 436, "scale": 0.28},
    {"name": "Triangle", "radius": 524, "scale": 0.67},
]

EPHEM_BODIES = {
    "Sun":     ephem.Sun,
    "Mercury": ephem.Mercury,
    "Venus":   ephem.Venus,
    "Mars":    ephem.Mars,
    "Jupiter": ephem.Jupiter,
    "Saturn":  ephem.Saturn,
}

# --- Star configuration ---
STAR_TARGET_DATE  = datetime(2026, 7, 7, tzinfo=CST)
STAR_TARGET_DATE  = datetime(2026, 6, 10, 2, 50, tzinfo=CST)

STAR_PLANET       = "Earth"
STAR_SCALE        = 0.45
STAR_ROTATION_OFFSET = 180  # extra degrees on top of pointing inward (tweak this)


def get_planet_angle(name, dt=None):
    if name == "Sun":
        return 0

    if name == "Triangle":
        if dt is None:
            dt = datetime.now(CST)
            print(dt)
        hours = dt.hour + dt.minute / 60.0
        return (270 + hours * 15) % 360

    if dt is None:
        dt = datetime.now(CST)

    ephem_date = ephem.Date(dt.strftime("%Y/%m/%d %H:%M:%S"))

    if name == "Earth":
        sun = ephem.Sun()
        sun.compute(ephem_date, epoch=ephem.J2000)
        lon = math.degrees(sun.hlong) + 180
    else:
        body = EPHEM_BODIES[name]()
        body.compute(ephem_date, epoch=ephem.J2000)
        lon = math.degrees(body.hlong) + 180

    return lon % 360


def get_star_angle(target_date, planet=STAR_PLANET):
    return get_planet_angle(planet, target_date)


def get_inward_rotation(angle, offset=0):
    """Points image toward center, plus an optional fixed offset in degrees."""
    return -(angle - 90) + offset


def place_planets(background_path, planets, planet_scale, output_path, dt=None):
    if dt is None:
        dt = datetime.now(CST)

    print(f"Rendering positions for: {dt.strftime('%Y-%m-%d %H:%M CST')}")

    bg = Image.open(background_path).convert("RGBA")
    cx, cy = bg.width // 2, bg.height // 2

    # --- Calculate star position (don't paste yet) ---
    star_angle   = get_star_angle(STAR_TARGET_DATE, STAR_PLANET)
    earth_radius = next(p["radius"] for p in planets if p["name"] == STAR_PLANET) + 4
    star_img     = Image.open("Images/Star.png").convert("RGBA")
    sw = int(star_img.width  * STAR_SCALE)
    sh = int(star_img.height * STAR_SCALE)
    star_img     = star_img.resize((sw, sh), Image.LANCZOS)
    star_rotation = get_inward_rotation(star_angle, offset=STAR_ROTATION_OFFSET)
    star_img     = star_img.rotate(star_rotation, resample=Image.BICUBIC, expand=True)
    sw, sh       = star_img.size
    star_rad     = math.radians(star_angle)
    sx = int(cx + earth_radius * math.cos(star_rad) - sw / 2)
    sy = int(cy + earth_radius * math.sin(star_rad) - sh / 2)
    print(f"  {'Star':8s} angle={star_angle:6.1f}°  rotation={star_rotation:.1f}°  pos=({sx}, {sy})")

    # --- Place planets ---
    for p in planets:
        img = Image.open(f"Images/{p['name']}.png").convert("RGBA")

        scale = p.get("scale", planet_scale)
        w = int(img.width  * scale)
        h = int(img.height * scale)
        img = img.resize((w, h), Image.LANCZOS)

        angle = get_planet_angle(p["name"], dt)

        if p["name"] == "Triangle":
            rotation = get_inward_rotation(angle)
            img = img.rotate(rotation, resample=Image.BICUBIC, expand=True)
            w, h = img.size

        rad = math.radians(angle)
        x = int(cx + p["radius"] * math.cos(rad) - w / 2)
        y = int(cy + p["radius"] * math.sin(rad) - h / 2)

        bg.paste(img, (x, y), img)
        print(f"  {p['name']:8s} angle={angle:6.1f}°  pos=({x}, {y})")

    # --- Paste star on top ---
    bg.paste(star_img, (sx, sy), star_img)

    bg.save(output_path)
    print(f"Saved to {output_path}")


# --- Run ---
place_planets(BACKGROUND, PLANETS, PLANET_SCALE, OUTPUT)