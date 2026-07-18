# emscript-releng

## USE TO BUILD TOOLS ONLY

N.B.  We now use this repo exclusively to run the `build-tools-npm-from-etc-packages.yml` workflow.

## How this works

The workflow here will trigger based on pushes to the `dev` branch of the repo, or via manual trigger.

Once triggered, the workflow will compose npm packages suitable for `npm install` installation using a `.tgz` file.  It will then upload any new `.tgz` files to the `em-foundation/npm-packages` repo's `resources` release artifacts.  See https://github.com/em-foundation/npm-packages/releases/tag/resources for the current artifacts.

All of the source material for the npm packages is contained in the `etc/packages` folder in this repo.

## Adding a new tool

For each tool (aka package) that needs to be built, and ultimately uploaded to the npm-packages release:

Create a folder for the given tool in the `etc/packages` folder in this repo -- e.g. segger-arm

In that folder, deposit six files:

| Filename | Description |
| -------- | ----------- |
| README.md | A file that describes how to build the various zip files (see below)
| LICENSE | A file containing the license for the given package |
| VERSION | A file containing the version number for the package.  This can be a combination of the tools version and the version being uploaded to npm-packages.  Note that a given version number's tool will only be uploaded to npm-packages once.  Hence the version much change any time that a new upload is desired. |
| darwin-arm64.zip | The zip file for Mac's |
| linux-x64.zip | The zip file for Linux |
| win32-x64.zip | The zip file for Windows |

The zip file should contain a zip of the files needed in the package once installed (e.g. binaries, libraries, etc).

The workflow will add a `package.json` file and an `install.js` script to the `.tgz` package file (in addition to the three zip files).

## Update the workflow to include any new tools

After the folder is created with the six files, if you are adding a new tool / package, then modify the `.github/workflows/build-tools-npm-from-etc-packages.yml` file as follows:

On about line 29 of the yml file, modify the for loop to add the new tool / package's name (separated by a space from the other tool names):

```
for name in segger-arm segger-jlink ti-uniflash <new-toolname>
```

## The etc/packages/template folder

There is a special folder `etc/packages/template` that contains an installation script, and a package.json file that will be used by the generated npm package.

## Install with npm install

When installing with `npm install`, the `install.js` script will run and will determine which of the three operating systems to use, then will unzip all the files for that operating system into the appropriate place in the `node_modules` folder.

## OBSOLETE

We no longer use emscript-releng to build emscript.  In fact, the emscript-sdk has been deprecated in its entirety.
