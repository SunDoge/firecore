# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]


## [0.6.0]

### Changed

- Use default rules `None` in `adapt`
- Use std logging
- Introduce `naming` and `extract` to `adapter`.
- Temporarily remove config system. I don't know how to config.

## [0.5.0] - 2022-01-25

### Added

- `firecore.adapter.adapt` for input/output name rewriting.

### Changed

- `torch` helper functions are moved to another package.

## [0.4.0] - 2022-01-13

### Added

- `config.from_file` and `config.from_snippet`
- Export `config`
- Export `resolve`
- `firecore.torch.cudnn_utils.setup_cudnn_benchmark()`

### Changed

- Remove `jsonnet_loader` since `rjsonnet` has functional default import callback, please use `firecore.config` instead.

## [0.3.1] - 2022-01-11

### Fixed

- Export `logging`


## [0.3.0] - 2022-01-11

### Added

- Add `resolve` function.

## [0.2.1] - 2022-01-03

### Fixed

- Remove `loguru` from dependencies, use `structlog` intead.


## [0.2.0] - 2022-12-27

### Added 

- Added `torch` namespace.
- Added `AutoExporter` for torch jit functions.
- Added `get_logger` and `init` for logging

### Changed

- Use `structlog` instead of `loguru` for logging

## [0.1.0] - 2022-12-23

### Added

- `@main_fn` for main function.
- `jsonnet_loader` for load jsonnet file or str.
- system functions for `ulimit` and `find_free_port`. 



[unreleased]: https://github.com/olivierlacan/keep-a-changelog/compare/v0.6.0...HEAD
[0.5.0]: https://github.com/olivierlacan/keep-a-changelog/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/olivierlacan/keep-a-changelog/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/olivierlacan/keep-a-changelog/compare/v0.3.1...v0.4.0
[0.3.1]: https://github.com/olivierlacan/keep-a-changelog/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/olivierlacan/keep-a-changelog/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/olivierlacan/keep-a-changelog/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/olivierlacan/keep-a-changelog/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/olivierlacan/keep-a-changelog/releases/tag/v0.0.1

