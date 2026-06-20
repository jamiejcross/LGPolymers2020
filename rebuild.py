#!/usr/bin/env python3
"""Reassemble the reviewable core + externalised asset into one runnable .html.

Input : index.html      -- evidentiary core
        satellite.jpg    -- the satellite basemap
Output: lg_polymers_release_sim_complete.html  -- self-contained, runs offline

This reverses split.py exactly. The output is byte-for-byte identical to the
original build; the md5 assertion below proves it. Run:  python3 rebuild.py
"""
import base64, hashlib, sys, pathlib

CORE   = "index.html"
ASSET  = "satellite.jpg"
OUT    = "lg_polymers_release_sim_complete.html"

# md5 of the original self-contained build (lg_polymers_release_sim_v34.html)
ORIGINAL_MD5 = "e58dbac6f537aec22f4ec87aba1e839b"

# the two reversible anchors, shared with split.py
ORIG_LOADER = "loadSatTexture(D.satellite, tex => { dayTex = tex; applySatTexture(); });"
EXT_LOADER  = ("fetch('satellite.jpg').then(r=>r.blob()).then(b=>{const fr=new FileReader();"
               "fr.onload=()=>loadSatTexture(fr.result.split(',')[1],"
               "tex=>{dayTex=tex;applySatTexture();});fr.readAsDataURL(b);});")

def main():
    core = pathlib.Path(CORE).read_text()
    b64  = base64.b64encode(pathlib.Path(ASSET).read_bytes()).decode()

    if '"satellite": ""' not in core:
        sys.exit("core is missing the empty satellite slot")
    if EXT_LOADER not in core:
        sys.exit("core is missing the external loader line")

    html = core.replace('"satellite": ""', '"satellite": "' + b64 + '"', 1)
    html = html.replace(EXT_LOADER, ORIG_LOADER, 1)

    pathlib.Path(OUT).write_text(html)
    digest = hashlib.md5(html.encode()).hexdigest()
    print(f"wrote {OUT}  ({len(html.encode()):,} bytes, md5 {digest})")
    if digest == ORIGINAL_MD5:
        print("md5 matches the original build — exact reconstruction verified.")
    else:
        sys.exit(f"WARNING: md5 mismatch (expected {ORIGINAL_MD5})")

if __name__ == "__main__":
    main()
