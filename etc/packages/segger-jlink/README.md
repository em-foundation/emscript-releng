# Generating the zip file for Segger JLink

Suggest the following for generating the zip file:

- Go to Segger JLink Downloads page
- Download / install the version desired (usually the latest)
- Note the path to the installed SEGGER/JLink_Vxxx folder
- Create a segger-jlink-abridged folder (name as you see fit)
- Copy (recursively) the following files from the SEGGER/JLink_Vxxx folder to the segger-jlink-abridged folder
  - JLinkExe or JLink.exe
- zip up the segger-jlink-abridged folder: `cd segger-jlink-abridged && zip -r ../<zipfile name> *`
