# Verification

The skill's required frontmatter and naming pass the bundled skill validator. Studio JavaScript passes a syntax check.

The builder decoded all four Circuit PNGs, checked chunk checksums, dimensions, filter data, visible pixels, and real transparency. Source PNGs are copied without image manipulation. Tests rejected escaping file paths, escaping symlinks, remote image URLs, duplicate IDs, duplicate filenames, opaque/empty artwork, and an existing output target.

Browser tests restored a saved project after reloading, including its new brand, headline, featured product, format, background, size, and product count. Adding two PNGs expanded the collection to six. Invalid schema imports preserved the current collection. The browser-saved project format was readable by the builder. Standalone loading with network requests blocked passed, and the 390-pixel mobile viewport had no horizontal overflow.

The package includes no API key, environment files, personal machine paths, browser downloads, or rejected generations. Local skill installation is verified from disk. ChatGPT import and plugin installation are provided as setup paths; neither was performed in another account, and public directory publication was not requested.

Image generation, editing quality, subscription availability, and external-action permissions depend on the host tools and account. These checks verify the local package and its behavior, not universal host compatibility.
