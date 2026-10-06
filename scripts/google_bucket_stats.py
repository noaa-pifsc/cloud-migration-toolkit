import subprocess
import sys
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd

MAX_WORKERS = 16  # Number of parallel workers

def format_gcs_path(path_input):
    """Clean and normalize input path into valid GCS format (bucket root or subpath)."""
    path = path_input.strip()
    if not path.startswith("gs://"):
        path = f"gs://{path.lstrip('/')}"
    if not path.endswith("/"):
        path += "/"
    return path

def get_subfolders(prefix):
    """Fetch immediate top-level subfolder paths."""
    print(f"Listing subfolders under {prefix} ...")
    cmd = ["gcloud", "storage", "ls", prefix]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    
    clean_prefix = prefix.rstrip('/')
    
    # Filter only directory paths (ending with '/') and exclude root path itself
    folders = [
        line.strip() for line in result.stdout.splitlines() 
        if line.strip().endswith('/') and line.strip().rstrip('/') != clean_prefix
    ]
    return folders

def calculate_folder_size(folder_path):
    """Worker task: Runs 'gcloud storage du -s' for a single subfolder."""
    cmd = ["gcloud", "storage", "du", "-s", folder_path]
    res = subprocess.run(cmd, capture_output=True, text=True)
    
    if res.returncode == 0 and res.stdout:
        for line in res.stdout.splitlines():
            line = line.strip()
            # Regex captures digits (\d+) and path (gs://...) even if no space exists between them
            match = re.match(r'^(\d+)\s*(gs://.*)$', line)
            if match:
                bytes_size = int(match.group(1))
                actual_path = match.group(2)
                
                # Calculate size units
                mib = round(bytes_size / (1024 ** 2), 2)
                gib = round(bytes_size / (1024 ** 3), 4)
                tib = round(bytes_size / (1024 ** 4), 4)
                
                return {
                    'Folder_Path': actual_path,
                    'Size (TiB)': tib,
                    'Size (GiB)': gib,
                    'Size (MiB)': mib,
                    'Bytes': bytes_size
                }
    return None

def main():
    # Prompt supports both bucket roots and deeper subpaths
    user_input = input("Enter bucket name or GCS path (e.g., 'nmfs-dev-uc1-pifsc' or 'nmfs_odp_pifsc/PIFSC/ESD/ARP'): ")
    if not user_input.strip():
        print("No path provided. Exiting.")
        return

    root_gcs_path = format_gcs_path(user_input)

    try:
        subfolders = get_subfolders(root_gcs_path)
    except Exception as e:
        print(f"Error accessing path {root_gcs_path}: {e}", file=sys.stderr)
        return

    if not subfolders:
        print(f"No subfolders found under {root_gcs_path}.")
        return

    print(f"Found {len(subfolders)} top-level subfolders. Starting {MAX_WORKERS} parallel workers...\n")

    results = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_folder = {
            executor.submit(calculate_folder_size, folder): folder 
            for folder in subfolders
        }

        for future in as_completed(future_to_folder):
            try:
                data = future.result()
                if data:
                    results.append(data)
                    # Stream live output showing TiB and GiB
                    print(f"[{data['Size (TiB)']:>7.4f} TiB | {data['Size (GiB)']:>8.2f} GiB]  {data['Folder_Path']}", flush=True)
            except Exception as e:
                folder_name = future_to_folder[future]
                print(f"Error scanning {folder_name}: {e}", file=sys.stderr)

    if not results:
        print("No subfolders processed.")
        return

    # Process DataFrame and sort from largest to smallest unit in headers
    df = pd.DataFrame(results)
    column_order = ['Folder_Path', 'Size (TiB)', 'Size (GiB)', 'Size (MiB)', 'Bytes']
    df = df[column_order].sort_values(by='Bytes', ascending=False)

    # Generate timestamped output filename (YYYYMMDD_HHMMSS)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv = f"top_level_folder_stats_{timestamp}.csv"
    
    # Save to CSV
    df.to_csv(output_csv, index=False)
    print(f"\nCompleted! Saved stats for {len(df)} folders to {output_csv}")

if __name__ == "__main__":
    main()