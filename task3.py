from pathlib import Path
import sys

file_path = Path("log_file.txt")

def handle_errors(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Error: File not found.")
        except OSError as error:
            print(f"Error reading file: {error}")
        except KeyError as error:
            print(f"Missing key in log entry: {error}")
        except TypeError as error:
            print(f"Invalid data format: {error}")
        except Exception as error:
            print(f"Unexpected error: {error}")

        return []

    return inner


def parse_log_line(line: str) -> dict:
    parts = line.strip().split(maxsplit=3)

    if len(parts) < 4:
        return {}

    date, time, level, message = parts

    return {
        "date": date,
        "time": time,
        "level": level,
        "message": message
    }


@handle_errors
def load_logs(file_path: Path) -> list:
    logs = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            log_entry = parse_log_line(line)

            if log_entry:
                logs.append(log_entry)

    return logs


@handle_errors
def filter_logs_by_level(logs: list, level: str) -> list:
    return [
        log for log in logs
        if log["level"].lower() == level.lower()
    ]


@handle_errors
def count_logs_by_level(logs: list) -> dict:
    log_counts = {}

    for log in logs:
        level = log["level"]
        log_counts[level] = log_counts.get(level, 0) + 1

    return log_counts


def display_log_counts(counts: dict):
    print(f"{'Рівень логування':<17} | {'Кількість'}")
    print("-" * 30)

    for level, count in counts.items():
        print(f"{level:<17} | {count}")


def display_filtered_logs(logs: list, level: str):
    print(f"\nДеталі логів для рівня '{level.upper()}':")

    if not logs:
        print("No logs found.")
        return

    for log in logs:
        print(f"{log['date']} {log['time']} - {log['message']}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python task3.py <path_to_log_file> [log_level]")
        return

    file_path = Path(sys.argv[1])

    logs = load_logs(file_path)

    if not logs:
        print("No logs to analyze.")
        return

    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if len(sys.argv) == 3:
        level = sys.argv[2]
        filtered_logs = filter_logs_by_level(logs, level)
        display_filtered_logs(filtered_logs, level)


if __name__ == "__main__":
    main()