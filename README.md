# Cloud Migration Toolkit
> ⚠️ **Note: Under Active Development**
<a href=""><img align="right" src="./screenshots/draft_logo.png" alt="Folder Stats" width=400px></a>

Lightweight tools and practical starting points for moving scientific data to the cloud, managing it there, and accessing it from your computer.

### Contents

- [Move Data to the Cloud](#move-data-to-the-cloud)
- [Work with Data in the Cloud](#work-with-data-in-the-cloud)
- [Use Cloud Data Locally](#use-cloud-data-locally)
- [Choose a Tool](#choose-a-tool)
    - [Folder Stats Quick Start](tools/folder-stats/README.md)
    - [External Tools](#external-tools)
    - [Planned Tools](#planned-tools)
- [Help](#help)
- [License](#license)
- [Disclaimer](#disclaimer)

## Move Data to the Cloud

Start here if your data is on a computer, shared drive, or external disk.

1. **Inventory your data.** Use [Folder Stats](tools/folder-stats/README.md) to estimate subfolder sizes and optionally count files. Identify what needs to move and what should stay local.
2. **Choose the destination.** Google Drive is for file sharing and collaboration; Google Cloud Storage (GCS) stores objects in buckets for data storage and workflows. They are separate services with different access and setup requirements. Confirm the destination is appropriate for your data and your team's policies.
3. **Prepare and transfer.** Use the custom [File Copy Tool](#file-copy-tool) or [RoboCopy](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/robocopy) when you need to stage files locally or moving to Google Shared Drive. Use [NOAA Jetstream](#noaa-jetstream) for GCS uploads, or review [Local Drive Backup](#local-drive-backup) for selected code/project files copied to a Google Drive-synced destination.
4. **Verify after Upload.** Review transfer logs and failures, compare the expected files with the destination, and use checksum verification where supported. Keep source data until verification and retention requirements are satisfied. A folder-size report alone does not prove a successful transfer.

Before a large transfer, confirm permissions, storage capacity, and likely costs, and try a small representative dataset first.

## Work with Data in the Cloud

Start here if your data is already in a GCS bucket or Google Drive and you need to browse, organize, or access it from an R cloud workstation.

- **Browse, Move, rename, sync, aduit bucket contents and monitor uploads:** see [NOAA Jetstream](#noaa-jetstream).
- **Simple Move or rename cloud objects:** see the [GCS Move and Rename Tool](#gcs-move-and-rename-tool). It runs on your Windows computer but performs cloud operations without downloading and re-uploading the data locally.

Cloud objects do not always behave like files on a local disk. Check destination paths, overwrite behavior, required permissions, and cost warnings before moving or renaming data; do not assume a move is instantaneous or atomic. Avoid large reorganizations through a mounted drive without checking how the mount handles them.

### Mount a GCS Bucket on an R Cloud Workstation

Use the [NMFS Open Science CloudComputingSetup R resources](https://github.com/nmfs-opensci/CloudComputingSetup/tree/main/R) for bucket mounting and R read/write examples. The `mount_bucket.R` file contains **shell commands to run in the workstation terminal**, despite its extension; `mount_bucket_folder.sh` demonstrates mounting a selected bucket folder with `gcsfuse --only-dir`.

Review the scripts before running them and replace the example bucket, folder, and mount point with your own. Confirm bucket IAM permissions and the workstation's approved authentication method. The examples use `gcloud auth application-default login --no-launch-browser`; Google Drive OAuth is separate and does not grant bucket access. Installing Cloud Storage FUSE may require an administrator, and containerized workstations must permit FUSE mounts.

After mounting, R can read paths under the mount point, for example `list.files(path.expand("~/my_gcs_bucket"))`. Cloud Storage FUSE is not a full local filesystem: check [its semantics and limitations](https://cloud.google.com/storage/docs/cloud-storage-fuse/overview) before writing or running workloads with frequent small-file access. Mounts need to be recreated after a workstation restart.

### Mount Google Drive on an R Cloud Workstation

Follow the [rclone Google Drive guide](https://rclone.org/drive/) and [headless authentication instructions](https://rclone.org/remote_setup/). This repository includes a [Linux Google Drive mounting helper](scripts/google_drvie_script.sh); run it in the workstation terminal as the same user that runs RStudio, **not with sudo**.

1. Install a current [rclone release](https://rclone.org/install/) and have an administrator install FUSE3 if needed (`sudo apt install fuse3` on Debian/Ubuntu). The workstation must expose `/dev/fuse` and allow FUSE mounts; ask the cloud administrator if mounting is blocked.
2. Obtain an organization-approved OAuth client ID and secret from the GCP team through the [Jira service portal](https://apps-st.fisheries.noaa.gov/jira/servicedesk/customer/portal/14). Do not rely on rclone's shared client ID, which upstream says is being retired in 2026.
3. Run the helper's `config` action. Create a remote named `gdrive`, choose storage type `drive` by name, and select `drive.readonly` for reading or `drive` for reading/writing. Leave the service-account file blank for user OAuth. Answer **no** to browser authentication on the cloud workstation. On a trusted computer with a browser and preferably the same rclone version, run the **exact** `rclone authorize` command shown by the workstation and paste its result directly into `config_token`. Select a Shared Drive when prompted if that is your destination, then save and quit.
4. Mount and test a small file. The helper defaults to read-only; writing requires both the `drive` OAuth scope and appropriate Drive permissions.

```bash
bash scripts/google_drvie_script.sh config
bash scripts/google_drvie_script.sh mount
```

In R, use `list.files(path.expand("~/gdrive"))` or read a known file beneath that path. To enable writes and later unmount:

```bash
bash scripts/google_drvie_script.sh unmount
bash scripts/google_drvie_script.sh mount --read-write
# Close files and verify that pending uploads have finished before unmounting.
bash scripts/google_drvie_script.sh unmount
```

The helper supports `GDRIVE_REMOTE`, `GDRIVE_MOUNT`, `GDRIVE_CACHE`, and `GDRIVE_LOG` overrides; run its `help` action for defaults. Logs go to `~/.local/state/rclone/gdrive.log`, and writes are cached locally. Ensure enough cache disk space, retain the cache until uploads finish, and verify output in Drive before stopping the workstation. Keep tokens, client secrets, and the rclone configuration out of Git, tickets, and chat. Google Docs/Sheets are exported formats rather than ordinary mounted files; check rclone's limitations. A mount is neither a backup nor a guaranteed offline copy.

**Current scope:** this collection covers data transfer, access, management, and links to R cloud-workstation mounting examples. It does not provision a computing environment or provide a complete analysis workflow.

## Use Cloud Data Locally

Start here if you want to use cloud data with applications on your computer.

| Approach | When It Helps | Keep in Mind |
| --- | --- | --- |
| Mount cloud storage as a drive/folder | Browse and access cloud files through local applications; see [rclone Mount](#rclone-mount). | Uncached access needs a network connection. Application compatibility and write behavior depend on caching and configuration. |
| Download a local copy | Work offline or repeatedly process the same files. | You need local disk space; your copy does not automatically receive cloud changes. |
| Synchronize copies | Keep selected local and cloud locations aligned using a configured sync tool. | Check direction, exclusions, and deletion rules. Sync can propagate unwanted changes and is not a backup by itself. |

A mount is not a full offline copy or a backup. Reads, writes, and repeated scans can generate cloud requests and transfer costs. For offline work, explicitly download the files you need; do not rely on a mount's cache. See the upstream tool documentation for download and sync setup.

## Choose a Tool

**Included** means the tool is in this repository. **External** means follow the linked project's setup instructions separately.

| I Need To... | Tool / Setup | Data Location | Availability |
| --- | --- | --- | --- |
| Estimate subfolder sizes and counts | [Folder Stats](tools/folder-stats/README.md) | Local folder or mapped drive | Included |
| Copy or stage folders | [File Copy Tool](#file-copy-tool) | Local or accessible filesystem paths | External |
| Schedule selected code/project backups | [Local Drive Backup](#local-drive-backup) | Local to a synced folder, such as Google Drive | External |
| Upload data and browse buckets | [NOAA Jetstream](#noaa-jetstream) | Local to GCS; also offers Drive transfers | External |
| Move or rename GCS objects | [GCS Move and Rename Tool](#gcs-move-and-rename-tool) | Within/between GCS buckets | External; Windows |
| Access cloud storage as a local drive | [rclone Mount](#rclone-mount) | Cloud accessed locally | External |
| Mount a GCS bucket for R cloud work | [CloudComputingSetup R Resources](#cloudcomputingsetup-r-resources) | GCS accessed from a cloud workstation | External |
| Mount Google Drive for R cloud work | [Google Drive Mounting Helper](scripts/google_drvie_script.sh) and [setup guide](#mount-google-drive-on-an-r-cloud-workstation) | Drive accessed from a Linux cloud workstation | Included helper; external rclone/FUSE3 |

## Tool Details
### Folder Stats Quick Start

See the [Folder Stats Quick Start guide](tools/folder-stats/README.md) for installation, launch, and scan instructions.

## External Tools
These projects are not bundled here. Use their own documentation for current releases, supported platforms, installation, authentication, and troubleshooting. Installing a tool does not automatically grant access to cloud data.

### File Copy Tool

**Use for:** copying files and directories between accessible filesystem locations, including staging data before an upload.

The Archive Toolbox's Windows robocopy-based tool supports parallel copying, skipping existing destination files, and restarting interrupted transfers. The project also lists multiplatform variants; choose the version appropriate for your system. Skipping an existing file is not proof that its contents match the source. This is not, by itself, a direct Google Drive or GCS upload client.

**Setup:** [Archive Toolbox documentation](https://github.com/MichaelAkridge-NOAA/archive-toolbox).

### Local Drive Backup

**Use for:** scheduled copies of selected code/project files to a synced destination, such as a folder managed by Google Drive for Desktop.

The primary setup uses Windows batch scripts, robocopy, and Task Scheduler; the project also provides a Bash/rsync alternative. Configure source and destination paths and ensure your destination's cloud-sync client is connected.

**Important:** the documented exclusions include `*.csv`, `*.jpg`, logs, Git folders, and environment/dependency folders. Review and adapt exclusions before use. The default configuration is **not a complete backup of scientific datasets**, and a completed local copy does not prove the cloud sync has finished.

**Setup:** [Local Drive Backup documentation](https://github.com/SamuelChiu-PIFSC/Local_Drive_Backup).

### NOAA Jetstream

**Use for:** GCS uploads, upload-job monitoring, and bucket browsing/analysis. The project also offers Google Drive transfers with separate OAuth setup.

The upstream guide lists Python 3.9 or newer on Windows 10 or later, macOS, or Linux. GCS features require the Google Cloud SDK, an authenticated account, and permissions on the target bucket. Follow the upstream prerequisites before installing:

```shell
python -m pip install noaa-jetstream
jetstream
```

Jetstream starts a local web dashboard and normally opens your browser. Keep the launch terminal open while using it; press `Ctrl+C` there to stop it.

**Setup:** [NOAA Jetstream documentation](https://github.com/MichaelAkridge-NOAA/jetstream), including authentication and Google Drive setup links.

### GCS Move and Rename Tool

**Use for:** moving or renaming GCS objects through a Windows PowerShell/WinForms interface without mounting a bucket or transferring the data through your computer.

Requires the Google Cloud CLI (`gcloud`) on your system, authentication, and permissions to list/read/create/delete affected objects and retrieve bucket metadata. The app provides cost warnings and operation logs. Review source and destination paths and test a small operation first.

**Setup:** [GCS Move and Rename Tool documentation and release link](https://github.com/DanWoodrichNOAA/GCS_Move_Rename_Tool/tree/main).

### rclone Mount

**Use for:** exposing cloud storage as a drive or folder that local applications can access.

rclone mount supports Windows, macOS, Linux, and FreeBSD, with platform-specific filesystem dependencies. On Windows, install **WinFsp** as well as rclone. Configure and test the cloud connection using the upstream guide before mounting it.

Check the guide's **Limitations** and **VFS File Caching** sections before editing files through a mount. Many applications need write caching; pending writes must finish uploading before you treat them as safely stored in the cloud. Consider read-only access when you only need to inspect data.

**Setup:** [rclone mount documentation](https://rclone.org/commands/rclone_mount/), [Google Drive configuration](https://rclone.org/drive/), and [WinFsp for Windows](https://github.com/winfsp/winfsp). For a Linux R cloud workstation, see [Mount Google Drive on an R Cloud Workstation](#mount-google-drive-on-an-r-cloud-workstation) and the included [mounting helper](scripts/google_drvie_script.sh).

### CloudComputingSetup R Resources

**Use for:** setting up bucket access and mounting GCS storage on an R cloud workstation.

The NMFS Open Science collection includes bucket-mounting scripts, R read/write examples, GitHub setup, and package-install examples. Review and customize the example paths and authentication before use. Bucket permissions and a workstation that permits FUSE mounts are required; these resources do not automatically grant access or provision a workstation.

**Setup:** [CloudComputingSetup R resources](https://github.com/nmfs-opensci/CloudComputingSetup/tree/main/R) and the [bucket-mounting guidance above](#mount-a-gcs-bucket-on-an-r-cloud-workstation).

## Planned Tools

These entries are not available through this collection yet:

- **Migration Tracker:** PIFSC ESD ARP Google Sheet migration tracker; access/setup link pending.
- **Data Cleaner:** tool and setup details pending.

## Help

For toolkit questions or suggestions for the collection, contact the [PIFSC ESD Data Services Team](mailto:nmfs.pic.credinfo@noaa.gov). Include the tool name, operating system, what you tried, and a sanitized error message. Do not send passwords, authentication tokens, or sensitive paths/data.

For external-tool issues, start with that project's documentation and issue tracker.

#### License

See [LICENSE.md](./LICENSE.md) for details.

#### Disclaimer

This repository is a scientific product and is not official communication of the National Oceanic and Atmospheric Administration, or the United States Department of Commerce. All NOAA GitHub project code is provided on an “as is” basis and the user assumes responsibility for its use. Any claims against the Department of Commerce or Department of Commerce bureaus stemming from the use of this GitHub project will be governed by all applicable Federal law. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by the Department of Commerce. The Department of Commerce seal and logo, or the seal and logo of a DOC bureau, shall not be used in any manner to imply endorsement of any commercial product or activity by DOC or the United States Government.
