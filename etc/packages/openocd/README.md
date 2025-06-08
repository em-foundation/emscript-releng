# Generating the zip file for Open OCD

Suggest the following for generating the zip file:

- Go to Open OCD Downloads page
- Download / install the version desired (usually the latest)
- Note the path to the installed Open OCD binary and scripts folders
- Create a openocd-abridged folder (name as you see fit)
- Copy (recursively) the following files to the openocd-abridged folder
  - openocd.exe or openocd (the binary executable)
  - the scripts folder
- zip up the openocd-abridged folder: `cd openocd-abridged && zip -r ../<zipfile name> *`
