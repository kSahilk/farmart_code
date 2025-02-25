import sys
import mmap
import os

def extract_logs(log_file, date):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"output_{date}.txt")

    try:
        with open(log_file, "r") as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                with open(output_file, "w") as out:
                    for line in iter(mm.readline, b""):
                        try:
                            line_str = line.decode("utf-8").strip()
                            if line_str.startswith(date):
                                out.write(line_str + "\n")
                        except UnicodeDecodeError:
                            continue  # Skip invalid lines
        print(f"Logs for {date} saved to {output_file}")
    except (OSError, ValueError) as e:
        print(f"Error processing log file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_logs.py <log_file> <YYYY-MM-DD>")
        sys.exit(1)

    log_file = sys.argv[1].strip()
    date = sys.argv[2].strip()

    if not os.path.exists(log_file):
        print(f"Error: Log file '{log_file}' not found.")
        sys.exit(1)

    extract_logs(log_file, date)