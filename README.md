# fofus-storage

FOFUS public asset storage on GitHub (creator's law 29 Oct: save Railway
storage by hosting product media + generated assets here).

## Layout
- `products/<sku>/`     — store product media: `thumb.webp` (thumbnail), `model.stl`
- `designai/<model_ref>/` — designai generated assets: `thumb.webp`, `model.glb|stl`
- `thumbs/`             — shared/generated thumbnails

## Serving law
Serve through raw URLs (browsers + <img>/<a> work directly):
`https://raw.githubusercontent.com/reventer-bus/fofus-storage/main/<path>`

## Blob laws
- Only blobs < 95 MB (GitHub hard cap 100 MB; keep margin).
- NEVER git-LFS (bandwidth quota breaks raw serving).
- No customer PII, no quote uploads (jobs.db data stays on Railway, expires there).
- Thumbnails: webp, ≤ 60 KB target; STLs binary.

## Uploader
`tools/put.py <local-file> <repo-path>` commits + pushes, then prints the raw URL.
