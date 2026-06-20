#!/usr/bin/env python3
"""Split the self-contained simulation into a reviewable core + externalised asset.

Input : lg_polymers_release_sim_v34.html  (the original, self-contained build)
Output: index.html      -- evidentiary core (physics, source term, geometry, code)
        satellite.jpg    -- the 16 MB satellite basemap, decoded from base64

The only two differences between index.html and the original are:
  1. the satellite base64 value inside <script id="model-data"> is emptied, and
  2. the one line that loaded it is repointed to fetch ./satellite.jpg .
Both edits are reversed exactly by rebuild.py, which reproduces the original
byte-for-byte (md5-verified).
"""
import base64, hashlib, re, sys, pathlib

SRC   = "lg_polymers_release_sim_v34.html"
CORE  = "index.html"
ASSET = "satellite.jpg"

# --- the two reversible anchors, shared with rebuild.py -----------------------
ORIG_LOADER = "loadSatTexture(D.satellite, tex => { dayTex = tex; applySatTexture(); });"
EXT_LOADER  = ("fetch('satellite.jpg').then(r=>r.blob()).then(b=>{const fr=new FileReader();"
               "fr.onload=()=>loadSatTexture(fr.result.split(',')[1],"
               "tex=>{dayTex=tex;applySatTexture();});fr.readAsDataURL(b);});")

def main():
    html = pathlib.Path(SRC).read_text()

    m = re.search(r'"satellite": "([A-Za-z0-9+/=]+)"', html)
    if not m:
        sys.exit("could not locate satellite base64 payload")
    b64 = m.group(1)

    # 1. write the decoded JPEG asset
    raw = base64.b64decode(b64)
    if raw[:3] != b"\xff\xd8\xff":
        sys.exit("decoded payload is not a JPEG")
    pathlib.Path(ASSET).write_bytes(raw)

    # 2. build the core: empty the payload, repoint the loader
    core = html.replace('"satellite": "' + b64 + '"', '"satellite": ""', 1)
    if ORIG_LOADER not in core:
        sys.exit("could not locate the satellite loader line")
    core = core.replace(ORIG_LOADER, EXT_LOADER, 1)
    pathlib.Path(CORE).write_text(core)

    print(f"wrote {ASSET}  ({len(raw):,} bytes, md5 {hashlib.md5(raw).hexdigest()})")
    print(f"wrote {CORE}   ({len(core.encode()):,} bytes)")
    print(f"original md5: {hashlib.md5(html.encode()).hexdigest()}")

if __name__ == "__main__":
    main()
