# GitHub Workflows for emscript Tools

## Building tools folder npm packages

This workflow will build the needed tools folder tools based on the artifacts contained in the em-foundation/emscript-releng/etc/packages folder.  At present it builds three tools packages (segger-arm, segger-jlink, ti-uniflash).

When the workflow runs, it will 

- rebuild all three packages
- upload them to the em-foundation/npm-packages resources release

Note:  These tools change rarely.  It is not required that this workflow be run unless some of the artifacts in the etc/packages folder have been updated.
