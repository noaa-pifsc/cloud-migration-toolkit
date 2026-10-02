import os
import platform
import csv
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from gooey import Gooey, GooeyParser

def apply_long_path_prefix(path_str):
    """Enables Windows long path support (>260 chars) on demand."""
    if not path_str or platform.system() != 'Windows':
        return path_str
    
    normalized = os.path.normpath(path_str)
    if not normalized.startswith('\\\\?\\'):
        if normalized.startswith('\\\\'):
            return '\\\\?\\UNC\\' + normalized[2:]
        else:
            return '\\\\?\\' + normalized
    return normalized

def clean_path(path_str):
    """Basic path sanitizer without forcing long path prefixes upfront."""
    if not path_str:
        return path_str
    
    path_str = path_str.strip().strip('"').strip("'")
    
    if len(path_str) == 2 and path_str[1] == ':':
        path_str += '\\'
    
    return os.path.normpath(path_str)

def get_creation_date(stat_info):
    """Handles cross-platform creation date extraction."""
    if platform.system() == 'Windows':
        ctime = stat_info.st_ctime
    else:
        try:
            ctime = stat_info.st_birthtime
        except AttributeError:
            ctime = stat_info.st_mtime
    return datetime.fromtimestamp(ctime).strftime('%Y-%m-%d %H:%M:%S')

def get_folder_stats(path, count_items=True):
    """Single-pass recursive directory calculator."""
    total_size = 0
    num_files = 0
    num_folders = 0

    try:
        with os.scandir(path) as it:
            for entry in it:
                try:
                    if entry.is_dir(follow_symlinks=False):
                        if count_items:
                            num_folders += 1
                            sub_size, sub_files, sub_folders = get_folder_stats(entry.path, count_items=True)
                            total_size += sub_size
                            num_files += sub_files
                            num_folders += sub_folders
                        else:
                            # Fast mode: calculate size only
                            sub_size, _, _ = get_folder_stats(entry.path, count_items=False)
                            total_size += sub_size
                    elif entry.is_file(follow_symlinks=False):
                        if count_items:
                            num_files += 1
                        total_size += entry.stat(follow_symlinks=False).st_size
                except PermissionError:
                    continue
    except PermissionError:
        pass

    return total_size, num_files, num_folders

def process_single_folder(dir_args):
    """Worker task executed across the thread pool."""
    current_src, scan_date, count_items = dir_args
    
    try:
        dir_stat = os.stat(current_src)
        created_date = get_creation_date(dir_stat)
        modified_date = datetime.fromtimestamp(dir_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        created_date = ""
        modified_date = ""

    # Fast single-pass recursion
    total_size, num_files, num_folders = get_folder_stats(current_src, count_items)

    size_mb = round(total_size / (1024 ** 2), 2)
    size_gb = round(total_size / (1024 ** 3), 4)
    size_tb = round(total_size / (1024 ** 4), 4)

    # Leave file and folder count blank if count_items is unchecked
    file_count_val = num_files if count_items else ""
    folder_count_val = num_folders if count_items else ""

    # Clean display path for output log
    display_path = current_src.replace('\\\\?\\UNC\\', '\\\\').replace('\\\\?\\', '')
    print(f"Scanned: {display_path} | Size: {size_gb} GB")

    # CSV Row output in exact requested column order
    return [
        display_path,       # FolderName
        size_tb,            # SizeTB
        size_gb,            # SizeGB
        size_mb,            # SizeMB
        file_count_val,     # File Count
        folder_count_val,   # Folder Count
        created_date,       # Created Date
        modified_date,      # Last Modified Date
        scan_date           # Scan Size_Date
    ]

@Gooey(
    program_name='High-Speed Network Folder Stats v2.1',
    default_size=(800, 600),
    navigation='SIDEBAR'
)
def parse_args():
    parser = GooeyParser(description='Parallel scanner for mapped drives and multi-TB networks.')
    parser.add_argument(
        'SELECT_PATH', 
        widget='DirChooser', 
        type=clean_path, 
        help='Select root folder or drive (e.g. M:\\ or \\\\server\\share)'
    )
    
    parser.add_argument(
        '--count_items', 
        action='store_true', 
        default=False, 
        help='Include file and folder counts in CSV (Slower)'
    )
    
    parser.add_argument(
        '--enable_long_paths', 
        action='store_true', 
        default=False, 
        help='Support Windows long paths >260 chars (Slightly slower)'
    )
    
    parser.add_argument(
        '--max_workers', 
        type=int, 
        default=16, 
        help='Number of parallel threads (Recommended: 16-32)'
    )
    return parser.parse_args()

def main():
    args = parse_args()
    pathvalue = args.SELECT_PATH
    count_items = args.count_items
    enable_long_paths = args.enable_long_paths
    max_workers = args.max_workers

    # Apply long path prefix ONLY if checkbox is explicitly checked
    if enable_long_paths:
        pathvalue = apply_long_path_prefix(pathvalue)

    scan_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_datetime = datetime.now().strftime("%m_%d_%Y_%H%M")
    
    log_file_name = f'{current_datetime}_network_folder_stats.csv'
    output_csv = os.path.join(pathvalue, log_file_name)

    # Header list matching exact target layout
    headers = [
        'FolderName', 
        'SizeTB', 
        'SizeGB', 
        'SizeMB', 
        'File Count', 
        'Folder Count', 
        'Created Date', 
        'Last Modified Date', 
        'Scan Size_Date'
    ]

    clean_display = pathvalue.replace('\\\\?\\UNC\\', '\\\\').replace('\\\\?\\', '')
    clean_output_csv = output_csv.replace('\\\\?\\UNC\\', '\\\\').replace('\\\\?\\', '')

    print(f"Target Path: {clean_display}")
    print(f"Parallel Threads: {max_workers}")
    print(f"Long Path Support: {'Enabled' if enable_long_paths else 'Disabled (Maximum Speed)'}")
    print("Collecting top-level directories...")

    try:
        top_dirs = [
            os.path.join(pathvalue, d) for d in os.listdir(pathvalue) 
            if os.path.isdir(os.path.join(pathvalue, d))
        ]
    except Exception as e:
        print(f"Error accessing directory ({clean_display}): {e}")
        return

    if not top_dirs:
        print("No sub-directories found in the target root.")
        return

    tasks = [(d, scan_date, count_items) for d in top_dirs]

    # Open CSV writer and stream output progressively
    with open(output_csv, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for result in executor.map(process_single_folder, tasks):
                writer.writerow(result)

    print('-------------------------------------------------')
    print('---- Network Scan Complete ----')
    print(f'---- Output saved to: {clean_output_csv} ----')

if __name__ == '__main__':
    main()