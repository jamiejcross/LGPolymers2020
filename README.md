# LG Polymers 2020 — styrene release simulation

Interactive 3D reconstruction of the 7 May 2020 styrene release at the LG Polymers
plant, Visakhapatnam, with the modelled plume and AEGL exposure zones draped over
terrain and a satellite basemap.

**Live:** https://jamiejcross.github.io/LGPolymers2020/

## Why this repository is split

The original build is a single self-contained `.html` of ~23 MB. ~21 MB of that is
one base64-encoded JPEG basemap on a single line, which makes the evidentiary
content — the physics, the source term, the exposure-ring radii and their citations
— effectively impossible to read or diff. This repository separates the two:

| file | what it is |
|---|---|
| [`index.html`](index.html) | **Evidentiary core** (~2.5 MB). Source term, AEGL-3/2/1 ring radii and provenance (`plume`), terrain, building/road geometry, heat-susceptibility data, and all simulation code. Reviewable and diffable. |
| [`satellite.jpg`](satellite.jpg) | The 16 MB satellite basemap, decoded from base64 to a normal image. Loaded by `index.html` at runtime. |
| [`split.py`](split.py) | Produces the two files above from the original build. |
| [`rebuild.py`](rebuild.py) | Reassembles them into one self-contained `.html`. |

The source term and exposure model live in the `plume` block of the
`<script id="model-data">` JSON in `index.html`: the M6 styrene tank coordinates,
the FLEXPART-WRF / ALOHA ring radii (AEGL-3 ~430 m, AEGL-2 ~1100 m, AEGL-1 ~2900 m),
and the plume bearing — each carrying its source citation (Karmakar et al. 2025,
DOI 10.21203/rs.3.rs-8163344/v1; HPCR 2020; JMC report to the NGT, 28.05.2020).

## Rebuilding the single-file version

```bash
python3 rebuild.py
```

Writes `lg_polymers_release_sim_complete.html` and verifies its MD5 against the
original build — the reconstruction is byte-for-byte identical, so the split is
provably lossless. The resulting file runs offline (it still pulls proj4 and
geotiff from their CDNs, as the original did).

## Provenance

- Modelling: Karmakar et al. 2025 (DOI 10.21203/rs.3.rs-8163344/v1), drawing on HPCR 2020.
- Reported harm and response: JMC report to the NGT, 28.05.2020; HPCR 2020.
- Elevation: Copernicus GLO-30 © ESA. Imagery: Esri / Maxar / Earthstar Geographics.
