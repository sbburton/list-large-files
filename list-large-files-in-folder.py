import os
import csv
import sys
from heapq import nlargest
from tqdm import tqdm  # install with: pip install tqdm

def get_largest_files_to_csv(directory: str, top_n: int = 100, min_size_mb: float = 0.0):
    """
    Search a directory (recursively), find the top N largest files
    above a given size threshold, show a progress bar, and write results to CSV.
    """
    min_size_bytes = min_size_mb * 1024 * 1024
    total_files = sum(len(files) for _, _, files in os.walk(directory))
    file_sizes = []

    with tqdm(total=total_files, desc="Scanning files", unit="file") as pbar:
        for root, _, files in os.walk(directory):
            for file in files:
                try:
                    full_path = os.path.join(root, file)
                    size = os.path.getsize(full_path)
                    if size >= min_size_bytes:
                        file_sizes.append((size, full_path))
                except (PermissionError, FileNotFoundError):
                    pass
                finally:
                    pbar.update(1)

    largest_files = nlargest(top_n, file_sizes, key=lambda x: x[0])
    csv_path = os.path.join(directory, "largest_files.csv")

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Size (bytes)", "Size (MB)", "File Path"])
        for size, path in largest_files:
            writer.writerow([size, round(size / (1024 * 1024), 2), path])

    tqdm.write(f"✅ CSV saved to: {csv_path}")
    return csv_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python find_largest_files.py <directory> [top_n] [min_size_mb]")
        sys.exit(1)

    directory = sys.argv[1]
    top_n = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    min_size_mb = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0

    get_largest_files_to_csv(directory, top_n, min_size_mb)
