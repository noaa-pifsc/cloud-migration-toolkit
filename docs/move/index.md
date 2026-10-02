# Move Data to the Cloud

Start here if your data is on a computer, shared drive, or external disk.

## Inventory Your Data

Use [Folder Stats](../tools/folder-stats.md) to estimate subfolder sizes and optionally count files. Identify what needs to move and what should stay local.

## Choose the Destination

Google Drive is for file sharing and collaboration; Google Cloud Storage (GCS) stores objects in buckets for data storage and workflows. They are separate services with different access and setup requirements. Confirm the destination is appropriate for your data and your team's policies.

Before a large transfer, confirm permissions, storage capacity, and likely costs, and try a small representative dataset first.

## Prepare and Transfer

- Use the [File Copy Tool](../tools/external-tools.md#file-copy-tool) when you need to stage files locally or copy to an accessible Google Shared Drive location. It is not a direct Drive or GCS upload client.
- Use [NOAA Jetstream](../tools/external-tools.md#noaa-jetstream) for GCS uploads.
- Review [Local Drive Backup](../tools/external-tools.md#local-drive-backup) for selected code/project files copied to a Google Drive-synced destination. Review its exclusions before use.

Installing a tool does not automatically grant access to cloud data. Follow the selected tool's authentication and permission requirements.

## Verify After Upload

Review transfer logs and failures, compare the expected files with the destination, and use checksum verification where supported.

!!! warning "Keep Your Source Until Verification Is Complete"
    Keep source data until verification and retention requirements are satisfied. A folder-size report alone does not prove a successful transfer, and a completed local copy does not prove a cloud-sync client has finished uploading.

After the transfer, see [Work with Data in the Cloud](../work/index.md) and [Use Cloud Data Locally](../use/index.md).