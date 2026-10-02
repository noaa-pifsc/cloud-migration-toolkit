# External Tools

These projects are not bundled here. Use their own documentation for current releases, supported platforms, installation, authentication, and troubleshooting. Installing a tool does not automatically grant access to cloud data.

## File Copy Tool

**Use for:** copying files and directories between accessible filesystem locations, including staging data before an upload.

The Archive Toolbox's Windows robocopy-based tool supports parallel copying, skipping existing destination files, and restarting interrupted transfers. The project also lists multiplatform variants; choose the version appropriate for your system. Skipping an existing file is not proof that its contents match the source. This is not, by itself, a direct Google Drive or GCS upload client.

**Setup:** [Archive Toolbox documentation](https://github.com/MichaelAkridge-NOAA/archive-toolbox).

## Local Drive Backup

**Use for:** scheduled copies of selected code/project files to a synced destination, such as a folder managed by Google Drive for Desktop.

The primary setup uses Windows batch scripts, robocopy, and Task Scheduler; the project also provides a Bash/rsync alternative. Configure source and destination paths and ensure your destination's cloud-sync client is connected.

!!! warning "Review Backup Exclusions"
    The documented exclusions include `*.csv`, `*.jpg`, logs, Git folders, and environment/dependency folders. Review and adapt exclusions before use. The default configuration is **not a complete backup of scientific datasets**, and a completed local copy does not prove the cloud sync has finished.

**Setup:** [Local Drive Backup documentation](https://github.com/SamuelChiu-PIFSC/Local_Drive_Backup).

## NOAA Jetstream

**Use for:** GCS uploads, upload-job monitoring, and bucket browsing/analysis. The project also offers Google Drive transfers with separate OAuth setup.

The upstream guide lists Python 3.9 or newer on Windows 10 or later, macOS, or Linux. GCS features require the Google Cloud SDK, an authenticated account, and permissions on the target bucket. Follow the upstream prerequisites before installing:

```shell
python -m pip install noaa-jetstream
jetstream
```

Jetstream starts a local web dashboard and normally opens your browser. Keep the launch terminal open while using it; press `Ctrl+C` there to stop it.

**Setup:** [NOAA Jetstream documentation](https://github.com/MichaelAkridge-NOAA/jetstream), including authentication and Google Drive setup links.

## GCS Move and Rename Tool

**Use for:** moving or renaming GCS objects through a Windows PowerShell/WinForms interface without mounting a bucket or transferring the data through your computer.

Requires the Google Cloud CLI (`gcloud`) on your system, authentication, and permissions to list/read/create/delete affected objects and retrieve bucket metadata. The app provides cost warnings and operation logs. Review source and destination paths and test a small operation first.

**Setup:** [GCS Move and Rename Tool documentation and release link](https://github.com/DanWoodrichNOAA/GCS_Move_Rename_Tool/tree/main).

## rclone Mount

**Use for:** exposing cloud storage as a drive or folder that local applications can access.

rclone mount supports Windows, macOS, Linux, and FreeBSD, with platform-specific filesystem dependencies. On Windows, install **WinFsp** as well as rclone. Configure and test the cloud connection using the upstream guide before mounting it.

Check the guide's **Limitations** and **VFS File Caching** sections before editing files through a mount. Many applications need write caching; pending writes must finish uploading before you treat them as safely stored in the cloud. Consider read-only access when you only need to inspect data.

**Setup:** [rclone mount documentation](https://rclone.org/commands/rclone_mount/) and [WinFsp for Windows](https://github.com/winfsp/winfsp).