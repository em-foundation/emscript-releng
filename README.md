# emscript-releng

TODO:  Builds for main branch from main branches.

## Setup prior to building

1. Enter the version number for the build into VERSION file (no newline at the end)
2. Update etc/packages/emscript-sdk/CHANGELOG.md as needed
3. Modify the other files in etc/packages/emscript-sdk as needed
4. Commit to and push the dev branch

## Build staging version from dev branches using Github Actions / Workflows

- In a browser, open the Actions page: https://github.com/em-foundation/emscript-releng/actions
- Select `Build emscript-sdk using dev branches` in the Actions left menu
- Click `Run workflow` drop-down arrow on the right
- Select Use workflow from `branch: dev`
- Click `Run workflow` button (after selecting dev branch)

This starts the build.

## Monitor build progress

- Refresh the screen or click on `Build emscript-sdk using dev branches` in left menu

This should show the running build.

- Click on the build to see the jobs running
- Click on the job to see the log details for that job
