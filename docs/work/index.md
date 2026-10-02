# Work with Data in the Cloud

Start here if your data is already in a GCS bucket and you need to browse or organize it.

## Browse and Manage Bucket Contents

See [NOAA Jetstream](../tools/external-tools.md#noaa-jetstream) for browsing, moving, renaming, synchronizing, and auditing bucket contents, as well as monitoring uploads. Follow its upstream guide for the operations available in your installed release.

## Move or Rename Objects

The [GCS Move and Rename Tool](../tools/external-tools.md#gcs-move-and-rename-tool) runs on your Windows computer but performs cloud operations without downloading and re-uploading the data locally.

!!! warning "Cloud Objects Are Not Local Files"
    Check destination paths, overwrite behavior, required permissions, and cost warnings before moving or renaming data. Do not assume a move is instantaneous or atomic. Test a small operation first.

Avoid large reorganizations through a mounted drive without checking how the mount handles them.

## Current Scope

This collection covers data transfer, access, and management. It does not yet provide a guide or environment for running analyses, notebooks, or other computing jobs in the cloud.

For local applications, see [Use Cloud Data Locally](../use/index.md).