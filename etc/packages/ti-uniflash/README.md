# UniFlash 9.2.0 for Emporium

This package provides the UniFlash 9.2.0 CLI for CC2340R5 and CC2755P10 over XDS110.

| Archive | Platform | Validation |
| --- | --- | --- |
| win32-x64.zip | Windows x64 | Both boards loaded through Emporium. |
| linux-x64.zip | Linux x64 | Archive and dependency checks passed. Hardware provisioning test pending. |
| darwin-arm64.zip | Apple silicon macOS with Rosetta | Archive and dependency checks passed. Hardware provisioning test pending. |

The installer selects the archive using the Node runtime platform and architecture. The darwin-arm64.zip name matches the existing Apple silicon provisioning path. Like the previous archive at that path, it contains Intel x86-64 UniFlash binaries, which run through Rosetta on Apple silicon.

The archives were derived from the working platform-specific UniFlash 9.2.0 trees and trimmed for XDS110. They retain both Emporium target definitions, the shared debug and flash runtime, and the applicable setup files. Unix archives include executable modes and relative library symlinks. The package installer restores those links after ZIP extraction. The archive root is the contents of the ti-uniflash tool directory.

On Linux, if USB permissions have not already been configured, run ./udev_rules.sh from the installed UniFlash directory. It installs the included TI udev rules and reloads udev. Then use Emporium’s normal load workflow with each board.
