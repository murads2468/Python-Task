
from datetime import datetime
from collections import defaultdict


# Track malformed lines
malformed_count = 0


def read_errors(path):

    global malformed_count
    malformed_count = 0

    with open(path, "r", encoding="utf-8") as file:

        for line_number, line in enumerate(file, start=1):

            line = line.strip()

            if not line:
                malformed_count += 1
                continue

            try:
                parts = line.split("|")

                if len(parts) != 3:
                    raise ValueError("Invalid format")

                timestamp = parts[0].strip()
                level = parts[1].strip()
                message = parts[2].strip()

                # Validate timestamp
                datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

                if not level or not message:
                    raise ValueError("Missing information")

                if level == "ERROR":
                    yield (line_number, timestamp, message)

            except ValueError:
                malformed_count += 1


def summarize_errors(path):

    error_summary = defaultdict(int)

    for line_number, timestamp, message in read_errors(path):

        date = timestamp.split(" ")[0]
        error_summary[date] += 1

    return dict(error_summary)


# Generate sample log file
sample_logs = [
    "2026-11-07 10:30:00 | ERROR | Connection lost",
    "2026-11-07 10:35:00 | INFO | Application started",
    "2026-11-07 11:00:00 | ERROR | Database failed",
    "Invalid log record",
    "2026-11-08 09:00:00 | ERROR | Server timeout"
]

with open("sample.log", "w", encoding="utf-8") as file:

    for log in sample_logs:
        file.write(log + "\n")


# Read errors
print("Error Records:")

for error in read_errors("sample.log"):
    print(error)

print("\nError Summary:")
print(summarize_errors("sample.log"))

print("\nMalformed Lines:", malformed_count)
