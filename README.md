# NOAA-NMFS Cloud Migration Toolkit
<a href=""><img align="right" src="./screenshots/draft_logo.png" alt="Folder Stats" width=400px></a>
A Collection of lightweight Open Source tools for working with and migrating scientific data to the cloud.

#### Contact: 
- [PIFSC ESD Data Services Team](mailto:nmfs.pic.credinfo@noaa.gov)

### Table of Contents
- Local Tools
    - [Folder Stats Tool](#1-local-folder-stats-tool)
    - [Folder Copy Tool (Google Drive Robocopy Tool)](#2-folder-copy-toolrobocopy)
    - [Local to Google Drive Automated Sync/Backup Tool](#local-to-google-drive-automated-syncbackup-tool)
- Cloud Tools
    - [Data Tracker Tools](#data-tracker-tools)
    - [Data Cleaner Tools](#data-cleaner-tools)
    - [Data Manager Tool](#data-manager-tool)
    - [Cloud Move and Rename Tool](#cloud-move-and-rename-tool)
    - [Bucket Network Folder Mount Tool](#bucket-network-folder-mount-tool)

#### 1. Local Folder Stats Tool

The Folder Stats Tool scans the immediate subdirectories of a selected folder or mapped drive and exports their statistics to a CSV file.

- Recursively calculates folder sizes in TB, GB, and MB.
- Optionally counts files and subfolders.
- Processes top-level folders in parallel.
- Saves the CSV report in the selected folder.

<a href=""><img align="right" src="./screenshots/folder_stats.png" alt="Folder Stats" width=400px></a>
#### Install
Clone the repository and change to its directory:
```
git clone https://github.com/noaa-pifsc/esd-cloud-migration-toolkit.git
cd esd-cloud-migration-toolkit
```

```cmd
pip install -r requirements.txt
```

#### Start the App

```
python folder_stats_2026_multi.py
```

Choose the folder or mapped drive to scan. The tool reports each immediate subfolder and writes a timestamped `*_network_folder_stats.csv` file to the selected location. Enable **Include file/folder count** to calculate counts as well as sizes; leave it unchecked for size-only scanning. Adjust **Number of parallel threads** if needed.

#### 2. Folder Copy Tool(robocopy)

<a href="https://github.com/MichaelAkridge-NOAA/archive-toolbox"><img align="right" src="https://raw.githubusercontent.com/MichaelAkridge-NOAA/archive-toolbox/refs/heads/main/_docs/icons/sfm_toolbox_tool_00.png" alt="File Copy" width=400px></a>

### <a href="https://github.com/MichaelAkridge-NOAA/archive-toolbox">File Copy Tool</a>
File copy tool will copy files and directories from one place to another. 
* It uses a subprocess to call a windows robust file copy command
* The app will skip any existing files in a destination directory
* It will also run multi-threaded for performance
* If a copy process is interrupted, then simply run again since it also has the ability to restart the transfer.
- NOTE: Multiplatform versions available 

<br clear="right"/>


### Local to Google Drive Automated Sync/Backup Tool
- https://github.com/SamuelChiu-PIFSC/Local_Drive_Backup


### Data Tracker Tools
- [Placeholder - PIFSC ESD ARP Google Sheet Migration Tracker]()

### Data Cleaner Tools
### Placeholder

<a href=""><img align="right" src="https://raw.githubusercontent.com/MichaelAkridge-NOAA/archive-toolbox/refs/heads/main/toolbox/cloud/jetstream/_icons/jetstream_logo_400px.png" alt="Folder Stats" width=400px></a>

### Data Manager Tool

- [NOAA Jetstream](https://github.com/MichaelAkridge-NOAA/jetstream) — upload data to Google Cloud Storage.

#### Install
```
pip install noaa-jetstream
```
#### Run Jetstream

```
jetstream
```
<br clear="right"/>

<a href=""><img align="right" src="https://raw.githubusercontent.com/DanWoodrichNOAA/GCS_Move_Rename_Tool/refs/heads/main/doc/images/app_screenshot.png" alt="" width=400px></a>

## Cloud Move and Rename Tool
A small Windows PowerShell/WinForms application for moving or renaming Google Cloud Storage objects without mounting a bucket or downloading and re-uploading data.

- https://github.com/DanWoodrichNOAA/GCS_Move_Rename_Tool/tree/main


## Bucket Network Folder Mount Tool
- https://rclone.org/commands/rclone_mount/
    - https://github.com/winfsp/winfsp


#### License

See [LICENSE.md](./LICENSE.md) for details.

#### Disclaimer

This repository is a scientific product and is not official communication of the National Oceanic and Atmospheric Administration, or the United States Department of Commerce. All NOAA GitHub project code is provided on an “as is” basis and the user assumes responsibility for its use. Any claims against the Department of Commerce or Department of Commerce bureaus stemming from the use of this GitHub project will be governed by all applicable Federal law. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by the Department of Commerce. The Department of Commerce seal and logo, or the seal and logo of a DOC bureau, shall not be used in any manner to imply endorsement of any commercial product or activity by DOC or the United States Government.