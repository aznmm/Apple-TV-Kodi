# Apple-TV-Kodi

A Kodi add-on repository, published with GitHub Pages, for the Orchard skin (an Apple TV style skin for Kodi 21) and other add-ons. Once the repository is installed, Kodi installs and updates everything in it by itself.

Site: https://aznmm.github.io/Apple-TV-Kodi/

## Install on a Kodi device (once per device)

1. **Allow add-ons from outside the official repository**: Settings → System → Add-ons → **Unknown sources** → On → Yes.
2. **Add this site as a source**: Settings → File manager → **Add source** → `<None>` → type `https://aznmm.github.io/Apple-TV-Kodi/` → OK. Name it `Orchard` → OK.
3. **Install the repository**: Settings → Add-ons → **Install from zip file** → `Orchard` → `repository.appletv-1.0.1.zip`.
4. **Install the skin**: Settings → Add-ons → **Install from repository** → **Apple TV Kodi Repository** → Look and feel → Skin → **Orchard** → Install. Say **Yes** to switch skins, then **Yes** to keep it.

Kodi checks the repository for updates on its own. To check right away: Settings → Add-ons → My add-ons → right-click (long-press) Apple TV Kodi Repository → Check for updates.

## Publishing a new or updated add-on

1. Put the zip in `addons/<add-on id>/<add-on id>-<version>.zip`, for example `addons/skin.orchard/skin.orchard-0.3.0.zip`. Kodi looks for exactly that name, so the version must match the `version` in the add-on's `addon.xml`, and the zip must contain one folder named after the add-on id.
2. Run:

   ```bash
   python3 tools/update_index.py
   ```

3. Commit and push everything it changed, including the new `.sha256` files.

The script rebuilds the repository add-on from `repository.appletv/`, writes a `.sha256` checksum next to every zip (the repository tells Kodi to check them, and installs fail without them), copies each add-on's icon and fanart out of its zip for Kodi's repository browser, writes `addons/addons.xml` with the newest version of each add-on plus its `.md5`, and puts the repository zip and an `index.html` in the site root so Kodi's File manager can browse the site.

Older versions can stay in `addons/<id>/`; Kodi offers the newest one.

## What's where

| Path | What |
|---|---|
| `index.html`, `repository.appletv-*.zip` | What Kodi sees when it browses the site (generated) |
| `repository.appletv/` | Source of the repository add-on: `addon.xml` and its icon. Bump its version when you change it |
| `addons/addons.xml`, `addons/addons.xml.md5` | The repository index Kodi reads (generated) |
| `addons/<id>/` | Each add-on's zips, their `.sha256` checksums, and artwork |
| `tools/update_index.py` | Regenerates everything marked generated |
| `.nojekyll` | Tells GitHub Pages to publish the files as they are |

## Before adding other add-ons

Only host add-ons you made or are allowed to redistribute, and check each one's id, dependencies and Kodi version. For someone else's add-on, it's usually better to point Kodi at that author's own repository.
