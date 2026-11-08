"""Generate a small animated GIF of a spaceship clearing a GitHub contribution grid.
Uses GitHub GraphQL with the built-in Actions GITHUB_TOKEN; Pillow is the only dependency.
"""
import json
import os
import random
import urllib.request
from datetime import date, timedelta
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

USERNAME = os.getenv('GH_USERNAME', 'shivamkanala-45')
TOKEN = os.getenv('GH_TOKEN')
OUT = Path('assets/space-shooter.gif')
W, H = 920, 250
BG = '#0D1117'
COLORS = ['#161B22', '#0E4429', '#006D32', '#26A641', '#39D353']


def contributions():
    if not TOKEN:
        raise RuntimeError('GH_TOKEN is required; use secrets.GITHUB_TOKEN in GitHub Actions')
    query = '''query($login:String!) { user(login:$login) { contributionsCollection {
      contributionCalendar { weeks { contributionDays { contributionCount } } }
    } } }'''
    payload = json.dumps({'query': query, 'variables': {'login': USERNAME}}).encode()
    req = urllib.request.Request('https://api.github.com/graphql', data=payload,
        headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json',
                 'User-Agent': 'github-profile-space-shooter'})
    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.load(response)
    if data.get('errors') or not data.get('data', {}).get('user'):
        raise RuntimeError(f'GitHub GraphQL error: {data.get("errors", "user not found")}')
    weeks = data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
    return [[day['contributionCount'] for day in week['contributionDays']] for week in weeks]


def main():
    weeks = contributions()
    # Fit the most recent 52 weeks; pad short/partial weeks to 7 days.
    weeks = weeks[-52:]
    weeks = [[*week, *([0] * (7 - len(week)))] for week in weeks]
    max_count = max((v for week in weeks for v in week), default=0)
    rng = random.Random(45)
    frames = []
    cell, gap, x0, y0 = 12, 3, 72, 70
    total = len(weeks)
    try:
        font = ImageFont.truetype('DejaVuSans.ttf', 16)
        small = ImageFont.truetype('DejaVuSans.ttf', 12)
    except OSError:
        font = ImageFont.load_default()
        small = font
    # Spaceship travels left to right, blasting columns of contributions.
    for frame_no in range(42):
        progress = frame_no / 41
        ship_x = x0 + int(progress * max(total - 1, 1) * (cell + gap))
        ship_y = 48
        im = Image.new('RGB', (W, H), BG)
        d = ImageDraw.Draw(im)
        d.text((x0, 18), f'{USERNAME}  //  CONTRIBUTION DEFENDER', fill='#E6EDF3', font=font)
        d.text((x0, 222), 'GitHub contributions  •  last 52 weeks', fill='#8B949E', font=small)
        for ix, week in enumerate(weeks):
            for iy, count in enumerate(week):
                x, y = x0 + ix * (cell + gap), y0 + iy * (cell + gap)
                level = 0 if count == 0 else min(4, max(1, (count * 4 + max_count - 1) // max(1, max_count)))
                if ix < progress * (total - 1) and count > 0:
                    # Destroyed contribution blocks leave faint traces.
                    color = '#173247'
                else:
                    color = COLORS[level]
                d.rounded_rectangle((x, y, x + cell, y + cell), radius=2, fill=color)
                if ix == int(progress * max(total - 1, 1)) and count > 0:
                    d.line((ship_x + 7, ship_y + 16, x + 6, y + 5), fill='#38BDF8', width=2)
                    for _ in range(2):
                        sx = x + rng.randint(-4, 15)
                        sy = y + rng.randint(-4, 15)
                        d.ellipse((sx, sy, sx + 2, sy + 2), fill='#FDE68A')
        # Pixel-art ship, exhaust and cannon
        d.polygon([(ship_x + 11, ship_y - 8), (ship_x - 9, ship_y + 9),
                   (ship_x + 3, ship_y + 6), (ship_x + 11, ship_y + 11),
                   (ship_x + 19, ship_y + 6), (ship_x + 31, ship_y + 9)], fill='#38BDF8')
        d.ellipse((ship_x + 7, ship_y - 1, ship_x + 15, ship_y + 6), fill='#F8FAFC')
        d.line((ship_x + 11, ship_y + 12, ship_x + 11, ship_y + 23), fill='#F97316', width=4)
        frames.append(im)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=110,
                   loop=0, optimize=True, disposal=2)
    print(f'Wrote {OUT} ({OUT.stat().st_size:,} bytes)')


if __name__ == '__main__':
    main()
