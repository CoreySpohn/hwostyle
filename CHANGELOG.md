# Changelog

## [1.1.0](https://github.com/CoreySpohn/hwostyle/compare/v1.0.0...v1.1.0) (2026-04-21)


### Features

* Add paper style and refactor into multiple files for matainability ([f74bd8e](https://github.com/CoreySpohn/hwostyle/commit/f74bd8eaf572b0c034e7987e966f3b8debe0b251))


### Bug Fixes

* Add tol-colors as a dependency ([e15bd90](https://github.com/CoreySpohn/hwostyle/commit/e15bd90cfdf1bc96df7af59124e195ca191c4ba4))
* Remove tight layout as default ([e2ca7f4](https://github.com/CoreySpohn/hwostyle/commit/e2ca7f489971ea247ae0867bb827fe95e81fdc10))

## 1.0.0 (2026-03-02)


### Features

* Initial setup ([fa40f01](https://github.com/CoreySpohn/hwostyle/commit/fa40f01a6dc3f3e4d9011ade329011d5f212b852))

## 0.1.0 (Unreleased)

### Features

- Dual-mode style system: `use("dark")` for talks, `use("light")` for papers
- Color palette with 6 named colors (cyan, pink, yellow, green, red, purple)
- Semantic colormap registry (`cmaps.intensity`, `cmaps.residual`, etc.)
- Context managers `dark()` and `light()` that auto-restore previous mode
- Custom brand colormaps: `hwo_intensity`, `hwo_diverging`
