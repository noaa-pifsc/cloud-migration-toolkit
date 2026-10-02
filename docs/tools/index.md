# Choose a Tool

**Included** means the tool is in this repository. **External** means follow the linked project's setup instructions separately.

| I Need To... | Tool / Setup | Data Location | Availability |
| --- | --- | --- | --- |
| Estimate subfolder sizes and counts | [Folder Stats](folder-stats.md) | Local folder or mapped drive | Included |
| Copy or stage folders | [File Copy Tool](external-tools.md#file-copy-tool) | Local or accessible filesystem paths | External |
| Schedule selected code/project backups | [Local Drive Backup](external-tools.md#local-drive-backup) | Local to a synced folder, such as Google Drive | External |
| Upload data and browse buckets | [NOAA Jetstream](external-tools.md#noaa-jetstream) | Local to GCS; also offers Drive transfers | External |
| Move or rename GCS objects | [GCS Move and Rename Tool](external-tools.md#gcs-move-and-rename-tool) | Within/between GCS buckets | External; Windows |
| Access cloud storage as a local drive | [rclone Mount](external-tools.md#rclone-mount) | Cloud accessed locally | External |

## Included Local Tools

Folder Stats source and its own dependency file are in [tools/folder-stats](https://github.com/noaa-pifsc/cloud-migration-toolkit/tree/gh-pages/tools/folder-stats). Use the [quickstart](folder-stats.md) for installation and a first scan. Installing Folder Stats does not install the external tools.

## Planned Tools

These entries are not available through this collection yet:

- **Migration Tracker:** PIFSC ESD ARP Google Sheet migration tracker; access/setup link pending.
- **Data Cleaner:** tool and setup details pending.