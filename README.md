# NOAA-NMFS Cloud Migration Toolkit
<a href=""><img align="right" src="./screenshots/draft_logo.png" alt="Folder Stats" width=400px></a>
A Collection of lightweight Open Source tools for working with and migrating scientific data to the cloud.

#### Contact: 
- [PIFSC ESD Data Services Team](mailto:nmfs.pic.credinfo@noaa.gov)

### Table of Contents
1. [Folder Stats Tool](#1-local-folder-stats-tool)
2. [Cloud Data Tracker Tool](#2-data-tracker-tools)
3. [Cloud Data Cleaner Tool](#3-data-cleaner-tools)
4. [Cloud Data Manager Tool](#4-data-manager-tool)
5. [Cloud Move and Rename Tool](#5-cloud-move-and-rename-tool)
6. [Cloud Bucket Folder Mount Tool](#6-bucket-network-folder-mount-tool)

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


### 2. Data Tracker Tools
- [Placeholder - PIFSC ESD ARP Google Sheet Migration Tracker]()

### 3. Data Cleaner Tools
### Placeholder

<a href=""><img align="right" src="./screenshots/jetstream.png" alt="Folder Stats" width=400px></a>


### 4. Data Manager Tool

- [Jetstream](https://github.com/MichaelAkridge-NOAA/jetstream) — upload data to Google Cloud Storage.

#### Install
```
pip install noaa-jetstream
```
#### Run Jetstream

```
jetstream
```
<a href=""><img align="right" src="https://raw.githubusercontent.com/DanWoodrichNOAA/GCS_Move_Rename_Tool/refs/heads/main/doc/images/app_screenshot.png" alt="" width=400px></a>

## 5. Cloud Move and Rename Tool
A small Windows PowerShell/WinForms application for moving or renaming Google Cloud Storage objects without mounting a bucket or downloading and re-uploading data.

- https://github.com/DanWoodrichNOAA/GCS_Move_Rename_Tool/tree/main


## 6. Bucket Network Folder Mount Tool


#### License

See [LICENSE.md](./LICENSE.md) for details.

#### Disclaimer

This repository is a scientific product and is not official communication of the National Oceanic and Atmospheric Administration, or the United States Department of Commerce. All NOAA GitHub project code is provided on an “as is” basis and the user assumes responsibility for its use. Any claims against the Department of Commerce or Department of Commerce bureaus stemming from the use of this GitHub project will be governed by all applicable Federal law. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by the Department of Commerce. The Department of Commerce seal and logo, or the seal and logo of a DOC bureau, shall not be used in any manner to imply endorsement of any commercial product or activity by DOC or the United States Government.