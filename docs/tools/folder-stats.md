# Folder Stats Quick Start

Folder Stats is a desktop app that scans each immediate subfolder of a selected folder or mapped drive, recursively calculates its size, and saves one CSV row per subfolder. It does not upload data or require a cloud account.

## Before You Start

- A Python installation with `pip`, and a graphical desktop to display the app. If needed, start with the [Python installation guide](https://www.python.org/about/gettingstarted/).
- [Git](https://git-scm.com/downloads) for the clone instructions below. Alternatively, select the **gh-pages** branch on GitHub, use **Code > Download ZIP**, extract it, and open a terminal in the extracted repository folder.
- Permission to read the folders being scanned **and write a report in the selected folder**. The output location is not configurable.

A tested Python-version and operating-system compatibility matrix is not yet documented for Folder Stats. Its desktop interface uses Gooey; installation depends on GUI dependencies being available for your environment.

## Install and Launch

Open a terminal (PowerShell or Command Prompt on Windows, or Anaconda Prompt if you use Anaconda). Use the same Python environment for installation and launch. A dedicated environment is preferable if you already use Python for other projects.

If using Git, run these commands one at a time:

```shell
git clone --branch gh-pages https://github.com/noaa-pifsc/cloud-migration-toolkit.git
cd cloud-migration-toolkit
```

From the repository folder, install the tool's dependencies and start the app:

```shell
python -m pip install -r tools/folder-stats/requirements.txt
python tools/folder-stats/folder_stats_2026_multi.py
```

These commands install and launch **Folder Stats only**. They do not install the documentation site or the external tools.

## Run a Scan

1. Choose the folder or mapped drive you want to scan using the folder chooser.
2. Enable **Include file/folder count** if you need counts. Leave it unchecked for size-only output; counts will show `N/A`.
3. Start with the default **Number of parallel threads** value of **16**. Use a positive whole number; lower it if the scan puts too much load on a shared drive.
4. Click **Start** and wait for **Network Scan Complete** in the output.
5. Open the CSV in the selected folder using a spreadsheet application or text editor.

![Folder Stats desktop interface with folder selection, count option, and parallel thread setting](../assets/screenshots/folder_stats.png){ width="600" }

## Find and Read Your Report

The UTF-8 CSV is saved inside the folder you selected, with a name such as `10_02_2026_1430_network_folder_stats.csv`. The filename uses the scan start time, in `MM_DD_YYYY_HHMM` format.

| CSV Fields | Meaning |
| --- | --- |
| Path | Immediate subfolder being summarized. |
| Created Date, Last Modified Date | Dates for that subfolder, not every file inside it. Creation date may fall back to modification time on some systems. |
| Scan Date | Time the scan started. |
| Size (TB), Size (GB), Size (MB) | Recursive file sizes using powers of 1024, despite the TB/GB/MB labels; these may differ from decimal storage figures. |
| File Count, Folder Count | Recursive counts inside the subfolder, or `N/A` when counting is disabled. The summarized subfolder itself is not included in Folder Count. |

## Limitations to Know

!!! warning "Reports Can Be Incomplete"
    Files directly inside the selected root folder are **not included**. Only its immediate subfolders get report rows. Permission-denied entries can be silently skipped, so a completed scan can still have incomplete totals. Confirm access before using the report for migration planning.

- If there are no immediate subfolders, the app prints **No sub-directories found** and does not create a CSV.
- Two scans of the same folder started within the same minute use the same filename and can overwrite the earlier report. Rename or move a report you need to preserve before scanning again.
- Treat reports as potentially sensitive: they contain filesystem paths. Check them before sharing.

For migration planning, continue to [Move Data to the Cloud](../move/index.md). For questions, see [Help](../help.md).