import csv
import json
from pathlib import Path


def parseCpuEnergy():
    """ Reads and parses JSON objects from a log file, handling multi-line JSON. """
    data = []
    HEADERS = [
        "duration_seconds", "cpu0_package_joules", "cpu0_dram_joules", 
        "cpu1_package_joules", "cpu1_dram_joules", "video", "library"
    ]
    energy_path = Path("energy")

    for dir_path in energy_path.iterdir():  # Iterate through subfolders

        if dir_path.is_dir():
            video = dir_path.name.replace(".avi", "")

            for file_path in dir_path.iterdir():  # Iterate through files
                library = file_path.stem.replace(video, "").replace(".avi", "")

                k = 0

                with file_path.open('r') as f:
                    values = {"video": video, "library": library}
                    for line in f:
                        key, _, value = line.strip().partition('=')
                        if key == "" and k != 0:
                            data.append([values.get(h, '') for h in HEADERS]) # Append the extracted values
                            values = {"video": video, "library": library}
                        else:
                            if key in HEADERS:
                                values[key] = value
                            k = k + 1

    # Write to CSV
    with open("energy.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)  
        writer.writerows(data)

    print("✅ Energy CSV file  has been created successfully.")


def parse_json_objects(file_path):
    """ Reads and parses JSON objects from a log file, handling multi-line JSON. """
    json_objects = []
    buffer = ""

    with file_path.open("r", encoding="utf-8") as file:
        for line in file:
            buffer += line.strip()  # Accumulate lines
            if buffer.endswith("}"):  # Assume JSON objects end with '}'
                try:
                    json_objects.append(json.loads(buffer))
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}\nProblematic JSON: {buffer}")
                buffer = ""  # Reset buffer after parsing
    
    return json_objects

        
def parseResult():
    """ Reads and parses JSON objects from a log file, handling multi-line JSON. """
    # Define CSV headers
    HEADERS = [
        "compute_time", "download_size", "download_time", 
         "upload_size", "upload_time", "video", "library"
    ]

    # Read and parse the JSON log file
    json_objects = parse_json_objects(Path("result.txt"))

    # Write to CSV file
    with Path("result.csv").open("w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=HEADERS)
        writer.writeheader()

        for obj in json_objects:
            writer.writerow({
                key: obj.get(key, "") for key in HEADERS[:-2]  # Fetch existing keys
            } | {  # Special handling for transformed fields
                "video": obj.get("video", "").replace(".avi", ""),
                "library": obj.get("library", "")
            })

    print("✅ Result CSV file  has been created successfully.")


if __name__ == '__main__':

    parseResult()

    parseCpuEnergy()
