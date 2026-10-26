#!/usr/bin/env python3
"""Rebuild the Kodi repository that GitHub Pages serves from this folder.

Run it after adding or updating an add-on zip in addons/<id>/<id>-<version>.zip:

    python3 tools/update_index.py

It will:
  1. zip the repository add-on from repository.appletv/ into addons/repository.appletv/
  2. write <zip>.sha256 next to every zip (the repository asks Kodi to check these)
  3. copy each add-on's icon/fanart out of its newest zip, so Kodi's repo browser shows them
  4. write addons/addons.xml (newest version of each add-on) and addons/addons.xml.md5
  5. put the repository zip in the site root with an index.html, so Kodi's
     File manager can browse https://aznmm.github.io/Apple-TV-Kodi/ and install it
"""
import glob
import hashlib
import html
import os
import re
import shutil
import zipfile
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADDONS = os.path.join(ROOT, "addons")
REPO_SRC = os.path.join(ROOT, "repository.appletv")
FIXED_TIME = (2020, 1, 1, 0, 0, 0)  # stable timestamps so rebuilding doesn't change the zip


def version_key(version):
    return [int(p) if p.isdigit() else -1 for p in re.split(r"[.\-+~]", version)]


def read_manifest(path):
    root = ET.parse(path).getroot()
    return root.get("id"), root.get("version")


def build_repository_zip():
    addon_id, version = read_manifest(os.path.join(REPO_SRC, "addon.xml"))
    out_dir = os.path.join(ADDONS, addon_id)
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "%s-%s.zip" % (addon_id, version))
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for folder, _, files in sorted(os.walk(REPO_SRC)):
            for name in sorted(files):
                if name.startswith("."):
                    continue
                full = os.path.join(folder, name)
                arc = os.path.join(addon_id, os.path.relpath(full, REPO_SRC))
                info = zipfile.ZipInfo(arc, FIXED_TIME)
                info.compress_type = zipfile.ZIP_DEFLATED
                with open(full, "rb") as f:
                    z.writestr(info, f.read())
    return addon_id, version, out


def read_zip(path):
    with zipfile.ZipFile(path) as z:
        tops = {n.split("/")[0] for n in z.namelist() if "/" in n}
        if len(tops) != 1:
            raise SystemExit("%s: expected one top folder named after the add-on, found %s" % (path, sorted(tops)))
        top = tops.pop()
        text = z.read(top + "/addon.xml").decode("utf-8")
    root = ET.fromstring(text)
    addon_id, version = root.get("id"), root.get("version")
    if addon_id != top:
        raise SystemExit("%s: folder inside the zip is %s but addon.xml says %s" % (path, top, addon_id))
    expected = "%s-%s.zip" % (addon_id, version)
    if os.path.basename(path) != expected:
        raise SystemExit("%s: should be named %s (Kodi looks for that exact name)" % (path, expected))
    if os.path.basename(os.path.dirname(path)) != addon_id:
        raise SystemExit("%s: should be inside addons/%s/" % (path, addon_id))
    return addon_id, version, text, root


def write_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    with open(path + ".sha256", "w") as f:
        f.write(h.hexdigest() + "\n")


def copy_assets(zip_path, addon_id, root):
    assets = root.find("./extension[@point='xbmc.addon.metadata']/assets")
    if assets is None:
        return 0
    copied = 0
    with zipfile.ZipFile(zip_path) as z:
        names = set(z.namelist())
        for el in assets:
            rel = (el.text or "").strip()
            src = "%s/%s" % (addon_id, rel)
            if not rel or src not in names:
                continue
            dst = os.path.join(ADDONS, addon_id, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, "wb") as f:
                f.write(z.read(src))
            copied += 1
    return copied


def strip_declaration(text):
    return re.sub(r"^\s*<\?xml[^>]*\?>\s*", "", text).strip()


def write_site_root(repo_zip):
    name = os.path.basename(repo_zip)
    for old in glob.glob(os.path.join(ROOT, "repository.appletv-*.zip")):
        if os.path.basename(old) != name:
            os.remove(old)
    shutil.copyfile(repo_zip, os.path.join(ROOT, name))
    # Kodi lists a link only when its text is exactly the file name.
    page = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Apple TV Kodi Repository</title>
</head>
<body>
<h1>Apple TV Kodi Repository</h1>
<p>In Kodi: Settings &gt; File manager &gt; Add source, enter this page's address, then
Settings &gt; Add-ons &gt; Install from zip file &gt; pick this source &gt; install:</p>
<a href="{href}">{text}</a>
</body>
</html>
""".format(href=html.escape(name), text=html.escape(name))
    with open(os.path.join(ROOT, "index.html"), "w") as f:
        f.write(page)
    open(os.path.join(ROOT, ".nojekyll"), "w").close()


def main():
    repo_id, repo_version, repo_zip = build_repository_zip()
    newest = {}
    zips = sorted(glob.glob(os.path.join(ADDONS, "*", "*.zip")))
    for path in zips:
        addon_id, version, text, root = read_zip(path)
        write_sha256(path)
        if addon_id not in newest or version_key(version) > version_key(newest[addon_id][0]):
            newest[addon_id] = (version, text, root, path)
    entries, assets = [], 0
    for addon_id in sorted(newest):
        version, text, root, path = newest[addon_id]
        assets += copy_assets(path, addon_id, root)
        entries.append(strip_declaration(text))
    xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<addons>\n' + "\n".join(entries) + "\n</addons>\n"
    ET.fromstring(xml.encode("utf-8"))
    with open(os.path.join(ADDONS, "addons.xml"), "w", encoding="utf-8") as f:
        f.write(xml)
    with open(os.path.join(ADDONS, "addons.xml.md5"), "w") as f:
        f.write(hashlib.md5(xml.encode("utf-8")).hexdigest() + "\n")
    write_site_root(repo_zip)
    print("Indexed %d add-ons from %d zips (%d artwork files copied):" % (len(newest), len(zips), assets))
    for addon_id in sorted(newest):
        print("  %s %s" % (addon_id, newest[addon_id][0]))


if __name__ == "__main__":
    main()
