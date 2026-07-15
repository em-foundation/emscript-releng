# emscript-releng

## Setup prior to building

1. Enter the version number for the build into VERSION file (no newline at the end)
2. Update etc/packages/emscript-sdk/CHANGELOG.md as needed
3. Modify the other files in etc/packages/emscript-sdk as needed
4. Commit to and push the dev (default) branch

## Build staging version from dev branches using Github Actions / Workflows

- In a browser, open the Actions tab: https://github.com/em-foundation/emscript-releng/actions
- Select `Build emscript-sdk staging from dev` in the Actions left menu
- Click `Run workflow`  on the right
- Click `Run workflow` button

This starts the build.  At the end, the build will tag all the associated repositories

## Monitor build progress

After a few seconds, the running build should appear in the browser window.

- Click on the build status line to see the jobs running
- Click on the build job to see the log details for that job

## Merge emscript-sdk staging into main

When satisfied with the staging branch as the definitive branch for the given VERSION:

- In a browser, open the Actions tab: https://github.com/em-foundation/emscript-releng/actions
- Select `Merge emscript-sdk main from staging` in the Actions left menu
- Click `Run workflow`  on the right
- Click `Run workflow` button

This will squash-merge staging into main on emscript-sdk.  Then it will merge main back into staging for proper continuity.  Then it will tag the main branch with the official tag for the VERSION.
