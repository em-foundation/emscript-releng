# SRecord 1.65.0 for EM•porium

This package installs srec_cat, srec_cmp, and srec_info under tools/srecord/bin. The nRF54 FLPR build uses srec_cat to combine its RISC-V application with the VPR launcher. The nRF91 build can also use srec_cat to combine its images.

The three platform archives target Windows x64, Linux x64, and macOS arm64. Linux is built on Ubuntu 22.04. The macOS build targets macOS 13 or later. The native builds omit the optional Libgcrypt-backed hash filters. Intel HEX and binary conversion are covered by the packaging smoke test.

The upstream source is SRecord 1.65.0 at commit 5844fa801cf4e9749202cff86ea1ed67f0cacbbf. Each ZIP carries that source and the build recipe in source/. The source archive SHA-256 is 9e2cc90cf95499edb70c86c339733c2811d243a8b89d6667577cf5945cf5ad51. The executables and library sources carry GPL and LGPL notices. See LICENSE and the notices in the source archive. [Upstream source](https://github.com/sierrafoxtrot/srecord/tree/5844fa801cf4e9749202cff86ea1ed67f0cacbbf)

Run the Build SRecord platform ZIPs workflow when refreshing this package. It builds on each target host, checks the tool versions, and converts an Intel HEX application to binary before merging it with a launcher. Copy the verified platform ZIPs into this directory to publish through the standard tools workflow.
