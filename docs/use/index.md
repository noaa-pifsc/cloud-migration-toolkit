# Use Cloud Data Locally

Start here if you want to use cloud data with applications on your computer.

## Choose an Access Method

| Approach | When It Helps | Keep in Mind |
| --- | --- | --- |
| Mount cloud storage as a drive/folder | Browse and access cloud files through local applications; see [rclone Mount](../tools/external-tools.md#rclone-mount). | Uncached access needs a network connection. Application compatibility and write behavior depend on caching and configuration. |
| Download a local copy | Work offline or repeatedly process the same files. | You need local disk space; your copy does not automatically receive cloud changes. |
| Synchronize copies | Keep selected local and cloud locations aligned using a configured sync tool. | Check direction, exclusions, and deletion rules. Sync can propagate unwanted changes and is not a backup by itself. |

## Mounting and Offline Work

A mount is not a full offline copy or a backup. Reads, writes, and repeated scans can generate cloud requests and transfer costs.

For offline work, explicitly download the files you need; do not rely on a mount's cache. See the upstream tool documentation for download and sync setup.

## Writing and Synchronizing Safely

!!! warning "Review Writes and Deletion Rules"
    Many applications need write caching when using a mount. Pending writes must finish uploading before you treat them as safely stored in the cloud. Synchronization can propagate deletions and other unwanted changes; confirm its direction, exclusions, and deletion rules before running it.

Consider read-only access when you only need to inspect data. Review the [rclone Mount](../tools/external-tools.md#rclone-mount) prerequisites and limitations before configuring a mount.