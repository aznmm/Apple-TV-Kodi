#!/usr/bin/env python3
"""Regenerate addons/addons.xml and addons/addons.xml.md5 from add-on ZIPs."""
import hashlib, os, zipfile, xml.etree.ElementTree as ET
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADDONS = os.path.join(ROOT, "addons")
entries = []
for dirname in sorted(os.listdir(ADDONS)):
    folder = os.path.join(ADDONS, dirname)
    if not os.path.isdir(folder) or dirname == "__pycache__":
        continue
    for filename in sorted(os.listdir(folder)):
        if not filename.lower().endswith(".zip"):
            continue
        zpath = os.path.join(folder, filename)
        with zipfile.ZipFile(zpath) as z:
            candidates = [n for n in z.namelist() if n.count("/") == 1 and n.endswith("/addon.xml")]
            if not candidates:
                raise SystemExit(f"No root addon.xml found in {zpath}")
            root = ET.fromstring(z.read(candidates[0]))
            entries.append(ET.tostring(root, encoding="unicode"))
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<addons>\n' + "\n".join(entries) + "\n</addons>\n"
ET.fromstring(xml)
with open(os.path.join(ADDONS, "addons.xml"), "w", encoding="utf-8") as f: f.write(xml)
with open(os.path.join(ADDONS, "addons.xml.md5"), "w", encoding="utf-8") as f:
    f.write(hashlib.md5(xml.encode("utf-8")).hexdigest() + "\n")
print(f"Indexed {len(entries)} add-ons.")
