# NOAA-NMFS Cloud Migration Toolkit

Lightweight tools and practical starting points for moving scientific data to the cloud, managing it there, and accessing it from your computer.

## Choose Your Task

| I Need To... | Start Here |
| --- | --- |
| Move data from a computer, shared drive, or external disk | [Move Data to the Cloud](move/index.md) |
| Browse or organize data already in cloud storage | [Work with Data in the Cloud](work/index.md) |
| Access cloud data using applications on my computer | [Use Cloud Data Locally](use/index.md) |
| Find the right tool for a task | [Choose a Tool](tools/index.md) |
| Estimate local subfolder sizes and counts | [Folder Stats Quick Start](tools/folder-stats.md) |

## Standard Workflow

1. Inventory the source data and decide what needs to move.
2. Confirm the destination, access permissions, storage capacity, and likely costs.
3. Test the transfer with a small representative dataset.
4. Transfer the data and review failures and verification results.
5. Keep the source until verification and retention requirements are satisfied.
6. Choose how to manage cloud data and access it from your computer.

!!! warning "Verify Before Removing Source Data"
    A folder-size report alone does not prove a successful transfer. Review logs, compare the expected files with the destination, and use checksum verification where supported.

## What Is Included

[Folder Stats](tools/folder-stats.md) is included in this repository. Other tools have their own installation, authentication, and support requirements; see [External Tools](tools/external-tools.md).

This collection covers data transfer, access, and management. It does not yet provide a guide or environment for running analyses, notebooks, or other computing jobs in the cloud.

For questions about the toolkit, see [Help](help.md).