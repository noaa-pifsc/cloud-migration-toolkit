sudo apt update
# NOTE:
# The command below installs an older version of rclone,
# which does NOT provide the config_token option later.
sudo apt install fuse3 rclone
# Install the latest version of rclone
sudo curl https://rclone.org/install.sh | sudo bash
mkdir ~/gdrive
rclone config
#!/usr/bin/env bash
set -euo pipefail
umask 077

usage() {
  cat <<'HELP'
Mount Google Drive on a Linux R cloud workstation (run as your RStudio user).

Usage: bash scripts/google_drvie_script.sh [config|mount|unmount|help] [--read-write]
Default action: mount, read-only. --read-write is accepted only for mount.
Environment: GDRIVE_REMOTE (default gdrive:), GDRIVE_MOUNT (default ~/gdrive),
       GDRIVE_CACHE (default ~/.cache/rclone),
       GDRIVE_LOG (default ~/.local/state/rclone/gdrive.log).

Install a current rclone release: https://rclone.org/install/
On Debian/Ubuntu, an administrator can install FUSE with: sudo apt install fuse3
The workstation must expose /dev/fuse and allow FUSE mounts. In a container,
ask your cloud administrator to enable this; installation alone is not enough.

During config, create a remote named gdrive and select storage type drive
(not a numeric menu entry). Use an organization-approved OAuth client ID and
secret; request these from the GCP team through the Jira service portal:
https://apps-st.fisheries.noaa.gov/jira/servicedesk/customer/portal/14
The shared rclone client ID is being retired in 2026.
Choose drive.readonly for reading, or drive for writing existing/new files.
Leave service_account_file blank for user OAuth. Decline advanced config
unless needed. Answer n to browser authentication on the cloud workstation.
On a trusted computer with a browser and preferably the same rclone version,
run the EXACT rclone authorize command displayed by the workstation, then
paste its result directly into the workstation's config_token prompt.
Never put tokens or client secrets in scripts, Git, tickets, or chat.
Choose y at Shared Drive setup to select a Shared Drive, or n for My Drive.
Save the remote and quit config. If using a different name, set GDRIVE_REMOTE.

R example after mounting: list.files(path.expand("~/gdrive"))
For writes, both the OAuth scope and Drive permissions must allow writing.
Close files and verify uploads in the log and Drive before unmounting or
stopping the workstation. Keep the cache until pending uploads are complete.
Mounts must be recreated after workstation restarts; they are not backups.

Docs: https://rclone.org/drive/ and https://rclone.org/remote_setup/
HELP
}

action="${1:-mount}"
if [[ $# -gt 0 ]]; then shift; fi
mount_options=(--read-only)
if [[ $# -gt 0 ]]; then
  if [[ "$action" != mount || "$1" != --read-write || $# -ne 1 ]]; then
    usage >&2
    exit 2
  fi
  mount_options=()
fi

case "$action" in
  help|-h|--help) usage; exit 0 ;;
  config|mount|unmount) ;;
  *) usage >&2; exit 2 ;;
esac

if [[ "$(uname -s)" != Linux ]]; then
  printf 'This helper requires a Linux cloud workstation. See https://rclone.org/commands/rclone_mount/ for other platforms.\n' >&2
  exit 1
fi

mount_point="${GDRIVE_MOUNT:-$HOME/gdrive}"
if [[ "$mount_point" != /* ]]; then
  printf 'GDRIVE_MOUNT must be an absolute path.\n' >&2
  exit 2
fi

if [[ "$action" == unmount ]]; then
  if command -v fusermount3 >/dev/null 2>&1; then
    exec fusermount3 -u "$mount_point"
  fi
  exec fusermount -u "$mount_point"
fi

if ! command -v rclone >/dev/null 2>&1; then
  printf 'Install a current rclone release first: https://rclone.org/install/\n' >&2
  exit 1
fi

if [[ "$action" == config ]]; then
  usage
  exec rclone config
fi

if [[ ! -c /dev/fuse ]] || ! command -v fusermount3 >/dev/null 2>&1; then
  printf 'FUSE3 and access to /dev/fuse are required. Ask your cloud administrator to enable mounting.\n' >&2
  exit 1
fi

remote="${GDRIVE_REMOTE:-gdrive:}"
cache_dir="${GDRIVE_CACHE:-$HOME/.cache/rclone}"
log_file="${GDRIVE_LOG:-$HOME/.local/state/rclone/gdrive.log}"
rclone lsd "$remote" >/dev/null
mkdir -p "$mount_point" "$cache_dir" "$(dirname "$log_file")"
rclone mount "$remote" "$mount_point" \
  "${mount_options[@]}" \
  --vfs-cache-mode writes \
  --cache-dir "$cache_dir" \
  --dir-cache-time 5m \
  --vfs-cache-max-age 1h \
  --log-file "$log_file" \
  --log-level INFO \
  --daemon
printf 'Mounted %s at %s. Log: %s\n' "$remote" "$mount_point" "$log_file"
d) Delete this remote
