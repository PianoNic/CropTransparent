# Releasing

Releases are cut from GitHub; nothing is bumped by hand.

1. Every PR carries one label. [Release Drafter](../.github/release-drafter.yml) keeps a draft release up to date on each push to `main` and picks the next version from those labels:

   | Label | Bump |
   |---|---|
   | `breaking` | major |
   | `feature`, `enhancement` | minor |
   | `bug`, `refactor` | patch |

   Branches and PR titles are labelled automatically (`feature/…`, `fix/…`, "Add …", "Fix …", "Refactor …").

2. Publishing the draft runs [`release.yaml`](../.github/workflows/release.yaml):
   - **sync-version** writes the tag into `application.properties` and commits `Bumped application.properties to X for release [skip ci]` to `main`.
   - **docker** checks out that commit, marks the build as `production` and pushes a multi-arch image (`linux/amd64`, `linux/arm64`) to Docker Hub and GHCR, tagged `X.Y.Z`, `X.Y`, `X` and `latest` (not for pre-releases).

The version shown in the app's footer comes from that file, so the running image always reports the release it was built from.
