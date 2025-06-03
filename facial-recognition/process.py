import json
import csv

def preprocess_json_objects(content):
    """Ensure proper JSON object formatting."""
    content = content.strip()
    if not content:
        return []
    
    # Split the content into separate JSON objects
    objects = []
    obj_start, bracket_count = 0, 0
    
    for i, char in enumerate(content):
        if char == '{':
            if bracket_count == 0:
                obj_start = i
            bracket_count += 1
        elif char == '}':
            bracket_count -= 1
            if bracket_count == 0:
                objects.append(content[obj_start:i+1])
    
    return objects


def add(input_file, output_file ):
    data = []

    with open(input_file, 'r') as file:
        content = file.read()
    
    json_objects = preprocess_json_objects(content)

    for obj in json_objects:
        entry = json.loads(obj)
        process, pull, push = 0.0, 0.0, 0.0
        
        for key, value in entry.items():
            if isinstance(value, dict):
                process += value.get("process", 0)
                pull += value.get("pull", 0)
                push += value.get("push", 0)
                
        entry["body"]["process"] = process
        entry["body"]["pull"] = pull
        entry["body"]["push"] = push
        data.append(entry)
        
    with open(output_file, 'w') as file:
        for entry in data:
            file.write(json.dumps(entry, indent=4) + '\n')
            

def toCSV(input_file, output_file ):

    data = []

    # Read the entire content of the file
    with open(input_file, 'r') as file:
        content = file.read()
    
    # Process JSON objects
    json_objects = preprocess_json_objects(content)

    for obj in json_objects:
        try:
            # Load JSON object
            entry = json.loads(obj)
            data.append(entry)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON object: {e}")
            print(f"Problematic JSON object: {obj}")
            continue
    
    # Define the CSV file headers
    headers = ["chunkdir", "schema", "expe", "video", "process", "pull", "push"]

    # Open the CSV file for writing
    with open('result.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()

        # Replace field names where schema matches
        for entry in data:
            writer.writerow({
                    "chunkdir": entry["chunkdir"],
                    "schema": entry["schema"],
                    "expe": entry["expe"],
                    "video": entry["video"],
                    "process": entry["process"],
                    "pull": entry["pull"],
                    "push": entry["push"],

                })
         

# Usage
input_file = 'result.txt'
output_file = 'finalresult.txt'
csv_file = 'result.csv' 

add(input_file, output_file)

toCSV(output_file, csv_file)

