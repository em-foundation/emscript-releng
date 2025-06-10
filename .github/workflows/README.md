# GitHub Workflows for Em-Script

The build / release process has been boiled down into three main workflows:

1. Building the tools folder npm packages from the etc/packages folder
2. Building a "staging" emscript-sdk from the above npm packages, along with the em-foundation/emscript-content, and em-foundation/emscript-tools repos
3. Merging the "staging" emscript-sdk into the main branch of em-foundation/emscript-sdk repo

## Building tools folder npm packages

This workflow will build the needed tools folder tools based on the artifacts contained in the em-foundation/emscript-releng/etc/packages folder.  At present it builds three tools packages (segger-arm, segger-jlink, ti-uniflash).

When the workflow runs, it will 

- rebuild all three packages
- upload them to the em-foundation/npm-packages resources release

Note:  These tools change rarely.  It is not required that this workflow be run unless some of the artifacts in the etc/packages folder have been updated.

## Building a staging emscript-sdk

This is the most commonly run workflow.  It assembles the pieces from various sources into an emscript-sdk npm package.  It then uploads that package to the em-foundation/npm-packages resources release.

The workflow assembles pieces from:

- The tools built by the prior workflow
- The em-foundation/emscript-content repo
- The em-foundation/emscript-tools repo

When done, the em-foundation/emscript-sdk repo will have an updated staging branch as well.

## Merging the emscript-sdk staging branch into main

This workflow is used to create a "production" version of the emscript-sdk.  This is done by merging the staging branch into the main branch of the repo.
