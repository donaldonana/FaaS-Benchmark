import os
import json
import csv


def csv_save(output, headers, data) -> None:
    """_summary_

    Args:
        output (string): _description_
        headers (list): _description_
        data (dict): _description_
    """
    with open(output, 'w', newline='') as csvfile:
        file = csv.DictWriter(csvfile, fieldnames=headers)
        file.writeheader()

        for item in data:
            file.writerow({
                key : val for key, val in list(item.items())
            })
            
    print(f"{output}.csv succesfully save")



def process_cpu_energy_meter(output, headers, directory) -> None:
     
    data, item = [], {}
    
    # for each subfolder in Energy folder (1Mb.JPEG)
    for dir in os.listdir("result/energy"):
        dir_path = os.path.join("result/energy", dir)
        schema = dir

        # for each file in the subfolder (pillow1Mb.JPEG.txt)
        for file in os.listdir(dir_path):  
            file_path = os.path.join(dir_path, file)
            text = file.replace(".txt", "")

            with open(file_path, 'r') as file:
                lines = file.readlines()
                
            for line in lines:
                line = line.strip()
                if line:
                    key, val = line.split('=')
                    item[key] = val
                else:
                    if item:
                        item["schema"], item["text"] = schema, text
                        data.append(item)
                        item = {}
                        
    csv_save(output, headers, data)
    

def preprocess_json_objects(content):
    """Ensure proper JSON object formatting."""
    content = content.strip()
    if not content:
        return []
    
    # Split the content into separate JSON objects
    objects = []
    obj_start = 0
    bracket_count = 0
    
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

    # Replace field names where schema matches
    for entry in data:
        entry = entry["body"]
        total_process, total_pull, total_push = 0.0, 0.0, 0.0
        for key, value in entry.items():
    	    	if isinstance(value, dict):
                    total_process += value.get("process", 0)
                    total_pull += value.get("pull", 0)
                    total_push += value.get("push", 0)
        entry["process"] = total_process
        entry["pull"] = total_pull
        entry["push"] = total_push

    # Write the modified data to a new file
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
    headers = ["schema", "text", "process", "pull", "push"]

    # Open the CSV file for writing
    with open('result/result.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()

        # Replace field names where schema matches
        for entry in data:
            entry = entry["body"]
            writer.writerow({
                "schema": entry["schema"],
                "text": entry["text"].replace(".txt", ""),
                "process": entry["process"],
                "pull": entry["pull"],
                "push": entry["push"],
            })
         

if __name__ == "__main__":
    
    # Usage
    input_file = 'result/result.txt'
    output_file = 'result/finalresult.txt'
    csv_file = 'result/result.csv' 

    add(input_file, output_file)

    toCSV(output_file, csv_file)

    headers = [
        'duration_seconds', 
        'cpu0_package_joules',
        'cpu0_core_joules', 
        'cpu0_dram_joules',
        'schema',
        'text',
        'cpu_count'
    ]    
     
    
    process_cpu_energy_meter("result/energy.csv", headers, "energy")



