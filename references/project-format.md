# Portable project format

Version 1 uses JSON with `schemaVersion: 1`, `name`, `brand`, `kicker`, `headline`, `tagline`, and an `assets` array. Each asset has a unique lowercase `id`, a display `name`, a `.png` basename `filename`, and either `file` or `dataURL`. File paths are relative to the manifest and must resolve inside its folder; symlinks that escape are rejected. Data URLs must be base64 PNGs. Do not put instructions or credentials in metadata.

```json
{
  "schemaVersion": 1,
  "name": "My collection",
  "brand": "MY BRAND",
  "kicker": "PRODUCT COLLECTION",
  "headline": "Your campaign headline.",
  "tagline": "Your campaign tagline.",
  "assets": [
    {"id": "hero", "name": "Hero", "filename": "hero.png", "file": "hero.png"}
  ]
}
```

Collections support 1–32 assets, at most 15 MB and 16 million pixels per PNG, and at most 80 MB of decoded image data overall. PNGs need an alpha channel and visible artwork. Opaque uploads may be previewed with a warning, but must not be reported as verified transparent assets. Browser-saved projects use embedded `dataURL` values and optional `settings`: `layout`, `arrangement`, `product`, `placement`, `theme`, `scale`, and `checker`. Validate these against the studio's known values.

Create a new project directory for a new collection. Preserve source images and prior project versions; rebuild to a fresh HTML filename. The studio's **Save project** button downloads portable `.studio.json`; browser changes are otherwise temporary. Use **Open project** to restore the collection and settings. Product-image editing happens with the host's image tool, then revised PNGs can be added locally.
