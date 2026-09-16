# Generation VII Persistent Toolcache

Generation VII decompilation sessions must not rebuild or reinstall the reverse-engineering toolchain from upstream on every ChatGPT/session environment.

## Storage model

Each of the six target repositories owns a GitHub Release tagged:

`toolcache-2026-09-16`

The release contains a prebuilt Linux x86_64 archive and its SHA-256 checksum. Large third-party binaries live in Release assets rather than ordinary Git blobs. The repository tracks only the hydrator, workflow, manifests, analysis source, and documentation.

### Alola repositories

- PocketMonsters-Sun-Decompilation
- PocketMonsters-Moon-Decompilation
- PocketMonsters-UltraSun-Decompilation
- PocketMonsters-UltraMoon-Decompilation

Asset:

`gen7-3ds-toolcache-linux-x86_64.tar.gz`

Bundle contents include the repository-approved 3DS tooling/runtime set: ctrtool, makerom, 3dstool, Ghidra, a portable JDK 21 runtime, and Azahar.

### Let's Go repositories

- PocketMonsters-LetsGoPikachu-Decompilation
- PocketMonsters-LetsGoEevee-Decompilation

Asset:

`gen7-switch-toolcache-linux-x86_64.tar.gz`

Bundle contents include the repository-approved Switch tooling/runtime set: hactool, Ghidra, a portable JDK 21 runtime, and Eden.

## Session rule

A fresh session may need to materialize bytes into its ephemeral filesystem, but it must not redo package installation, clone upstream tool repositories, or compile the toolchain.

For a target repository run:

```bash
python3 tools/use_toolcache.py
source .tools/env.sh
```

`tools/setup_toolchain.sh` is retained as a compatibility wrapper and performs the same hydration operation. It no longer installs packages or builds upstream tools.

The hydrator:

1. locates the target repository's own GitHub Release,
2. downloads the matching prebuilt archive and checksum,
3. verifies SHA-256,
4. safely extracts it to the ignored `.tools/` directory,
5. skips work when `.tools/.toolcache-version` already matches.

The central `tools/setup_generation_vii_toolchains.sh` script clones/updates the six repositories if needed and hydrates their prebuilt caches. It does not compile the toolchains.

## Rebuild rule

Only GitHub Actions rebuilds the durable cache. Each target repository owns `.github/workflows/toolcache.yml`, which builds the approved open-source tooling and publishes the result to the fixed Release tag. This is maintenance work, not session bootstrap work.

## Exclusions

No ROM/cartridge images, title keys, console keys, firmware, decrypted proprietary game executables, or other proprietary game payloads are included in these toolcache releases.
