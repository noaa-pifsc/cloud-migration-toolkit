# NOAA-NMFS Cloud Migration Toolkit
<a href=""><img align="right" src="./screenshots/draft_logo.png" alt="Folder Stats" width=400px></a>
Lightweight tools and practical starting points for moving scientific data to the cloud, managing it there, and accessing it from your computer.

- https://noaa-pifsc.github.io/cloud-migration-toolkit/

## User Guide

Read the [Cloud Migration Toolkit guide](https://noaa-pifsc.github.io/cloud-migration-toolkit/) for detailed procedures, tool setup, and limitations.

| Task | Guide |
| --- | --- |
| Move data to the cloud | [Move](https://noaa-pifsc.github.io/cloud-migration-toolkit/move/) |
| Browse and organize cloud data | [Work](https://noaa-pifsc.github.io/cloud-migration-toolkit/work/) |
| Access cloud data from local applications | [Use](https://noaa-pifsc.github.io/cloud-migration-toolkit/use/) |
| Choose and set up a tool | [Tools](https://noaa-pifsc.github.io/cloud-migration-toolkit/tools/) |

The Markdown source is in [docs](docs/index.md), so the guide can also be read in the repository before the site is published.

## Publishing the Guide

Keep the site source and [documentation workflow](.github/workflows/docs.yml) on `gh-pages`. Pull requests targeting that branch build the site without deploying; pushes to `gh-pages` publish it through GitHub Actions.

Set **Settings > Pages > Source > GitHub Actions**, not **Deploy from a branch**. If the `github-pages` environment restricts deployment branches, allow `gh-pages`. Manual workflow runs require the workflow to also exist on the repository's default branch; select `gh-pages` for deployment.

## Help

For toolkit questions or suggestions for the collection, contact the [PIFSC ESD Data Services Team](mailto:nmfs.pic.credinfo@noaa.gov). Include the tool name, operating system, what you tried, and a sanitized error message. Do not send passwords, authentication tokens, or sensitive paths/data.

For external-tool issues, start with that project's documentation and issue tracker.

## License

See [LICENSE.md](./LICENSE.md) for details.

## Disclaimer

This repository is a scientific product and is not official communication of the National Oceanic and Atmospheric Administration, or the United States Department of Commerce. All NOAA GitHub project code is provided on an “as is” basis and the user assumes responsibility for its use. Any claims against the Department of Commerce or Department of Commerce bureaus stemming from the use of this GitHub project will be governed by all applicable Federal law. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by the Department of Commerce. The Department of Commerce seal and logo, or the seal and logo of a DOC bureau, shall not be used in any manner to imply endorsement of any commercial product or activity by DOC or the United States Government.