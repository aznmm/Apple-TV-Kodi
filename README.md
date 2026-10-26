# Apple-TV-Kodi

Starter files for hosting a Kodi add-on repository with GitHub Pages.

## Included
- `repository.appletv/addon.xml`: repository installer manifest.
- `addons/repository.appletv/repository.appletv-1.0.0.zip`: installable repository add-on.
- `addons/skin.orchard/skin.orchard-0.2.0.zip`: Orchard skin package supplied by the project owner.
- `addons/addons.xml` and `addons/addons.xml.md5`: initial repository index and checksum.

## Publish with GitHub Pages
1. Copy the contents of this starter folder into the root of `aznmm/Apple-TV-Kodi` (merge folders; do not delete existing project files).
2. In GitHub, open **Settings → Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**, select branch `main` and folder `/ (root)`, then Save.
4. Wait for Pages to publish. Confirm these URLs load:
   - https://aznmm.github.io/Apple-TV-Kodi/addons/addons.xml
   - https://aznmm.github.io/Apple-TV-Kodi/addons/addons.xml.md5
5. On Kodi, enable unknown sources if needed, then use **Add-ons → Install from zip file** and install:
   `https://github.com/aznmm/Apple-TV-Kodi/raw/refs/heads/main/addons/repository.appletv/repository.appletv-1.0.0.zip`
   (On devices where Kodi's file browser cannot download a URL directly, download the ZIP to a reachable location first.)
6. Open **Install from repository → Apple TV Kodi Repository** and install Orchard.

## Important notes
- This is a starter package, not yet tested on your Apple TV/Kodi version.
- The skin package's dependencies and compatibility should be tested on the Kodi version you run.
- Before adding more add-ons, confirm their exact names, IDs, dependencies, Kodi compatibility, and permission/license to redistribute. Prefer linking to their official repositories when redistribution is not allowed.
- Whenever you add/update packages, regenerate `addons.xml` and `addons.xml.md5`; the checksum must change when the index changes.
- Keep the repository URLs in `repository.appletv/addon.xml` aligned with your GitHub Pages URL if the repo name, account, or Pages setup changes.
