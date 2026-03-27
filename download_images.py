#!/usr/bin/env python3
"""
Run this once to download all trip guide images.
Then commit the 'images' folder to GitHub alongside index.html.

Usage:  python3 download_images.py
Needs:  pip install requests   (or: pip3 install requests)
"""
import os, time, json, urllib.request, urllib.parse

BOT_UA = 'TripGuide/1.0 (https://github.com/example/tripguide; bot@example.com)'
CDN_UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

FILENAMES = [
    ('Grand_Canyon_view_from_Pima_Point_2010.jpg',                          900),  # 00
    ('Valley of Fire State Park, Nevada (9181446112).jpg',                  900),  # 01
    ('Valley of fire - Fire Wave.jpg',                                       700),  # 02
    ('Valley of Fire White Domes area 8.jpg',                               700),  # 03
    ('Oatman-Oatman Main Street.jpg',                                        900),  # 04
    ('Cathedral Rock - Sedona AZ-1.jpg',                                     900),  # 05
    ('Cathedral Rock - Sedona AZ-1.jpg',                                     700),  # 06
    ('West_Fork_of_Oak_Creek_Canyon.jpg',                                    700),  # 07
    ("Devil's Bridge Trail, Sedona, Arizona - panoramio (38).jpg",          700),  # 08
    ('Panorama of rock formation near Sedona 2013.jpg',                     900),  # 09
    ('Mogollon Rim Panorama.jpg',                                            900),  # 10
    ('Grand_Canyon_view_from_Pima_Point_2010.jpg',                          900),  # 11
    ('USA 09983 Grand Canyon Luca Galuzzi 2007.jpg',                        700),  # 12
    ('Le Grand Canyon 2016 Desert View Watchtower (6).JPG',                 700),  # 13
    ('USA 10187 Horseshoe Bend Luca Galuzzi 2007.jpg',                      900),  # 14
    ('Upper Antelope Canyon Heart Formation 2013.jpg',                      700),  # 15
    ('Lower Antelope Canyon 478.jpg',                                        700),  # 16
    ('Monument Valley Arizona Panoramic.jpg',                               900),  # 17
    ('Goosenecks State Park, Utah, Image of the Day DVIDS860656.jpg',       700),  # 18
    ('Monument_Valley_01.jpg',                                               700),  # 19
    ('Kodachrome Basin Utah.jpg',                                            900),  # 20
    ('Bryce_Canyon_Amphitheater_Hoodoos_Panorama.jpg',                      900),  # 21
    ("Thor's Hammer (Bryce Canyon National Park) (14713013206).jpg",        700),  # 22
    ('Sunrise Point Bryce Canyon November 2018 002.jpg',                    700),  # 23
]

def get_thumb_url(fname, width):
    title = 'File:' + fname
    params = urllib.parse.urlencode({
        'action': 'query',
        'titles': title,
        'prop': 'imageinfo',
        'iiprop': 'url',
        'iiurlwidth': width,
        'format': 'json',
    })
    api_url = 'https://commons.wikimedia.org/w/api.php?' + params
    req = urllib.request.Request(api_url, headers={'User-Agent': BOT_UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read())
    pages = data['query']['pages']
    page = next(iter(pages.values()))
    return page['imageinfo'][0]['thumburl']

os.makedirs('images', exist_ok=True)

ok, fail = 0, 0
for i, (fname, width) in enumerate(FILENAMES):
    dest = f"images/{i:02d}.jpg"
    if os.path.exists(dest):
        print(f"  {i:02d}  already exists — skipping")
        ok += 1
        continue
    try:
        url = get_thumb_url(fname, width)
        req = urllib.request.Request(url, headers={'User-Agent': CDN_UA})
        with urllib.request.urlopen(req, timeout=20) as r:
            img = r.read()
        with open(dest, 'wb') as f:
            f.write(img)
        print(f"  {i:02d}  OK  {len(img)//1024}KB  {dest}")
        ok += 1
    except Exception as e:
        print(f"  {i:02d}  FAIL  {e}")
        fail += 1
    time.sleep(5)

print(f"\nDone: {ok} downloaded, {fail} failed")
print("Now commit the 'images' folder to GitHub alongside index.html")
