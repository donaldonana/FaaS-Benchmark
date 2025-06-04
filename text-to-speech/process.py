import os
import json
import csv
from collections import defaultdict



def csv_save(output:str, headers:list, data:dict) -> True:
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
            
    print(f"{output} succesfully save")
    
    return True


def compute_totals(entry:dict)->dict:
    """Compute total values for 'process', 'pull', and 'push' times
    for each function in a DAG
    """
    totals = {"process": 0.0, "pull": 0.0, "push": 0.0}
    
    for value in entry.values():
        if isinstance(value, dict):
            for key in totals:
                totals[key] += value.get(key, 0.0)
    
    entry.update(totals)
    
    return entry


def add(input_file:str)->list:
    """Main function to load, process, and write JSON data."""
    with open(input_file, 'r') as file:
        content = file.read()
    
    json_objects = preprocess_json_objects(content)
    data = []
    
    for obj in json_objects:
        entry = json.loads(obj)
        entry["body"] = compute_totals(entry.get("body", {}))
        data.append(entry)
    
    return data

     
def to_csv(input_file:str, output_file:str)->bool:
    """Convert processed JSON entries to CSV format."""
    headers = ["schema", "text", "process", "pull", "push"]
    data = add(input_file)
    rows = []
    
    for entry in data:
        body = entry.get("body", {})
        rows.append({
            "schema": body.get("schema", ""),
            "text": body.get("text", "").replace(".txt", ""),
            "process": body.get("process", 0.0),
            "pull": body.get("pull", 0.0),
            "push": body.get("push", 0.0),
        })

    csv_save(output_file, headers, rows)
     
    return True
          

def process_cpu_energy_meter(output:str, headers:list, energy_file:str) -> True:
    """
    Parse cpu energy meter result files 
    """
     
    data = list()
    item = dict()
    
    # For each subfolder in Energy folder (1Mb.JPEG).
    for dir in os.listdir(energy_file):
        dir_path = os.path.join(energy_file, dir)
        schema = dir

        # For each file in the subfolder. 
        for file in os.listdir(dir_path):  
            file_path = os.path.join(dir_path, file)
            text = file.replace(".txt", "")

            with open(file_path, 'r') as file:
                lines = file.readlines()
                
            for line in lines:
                line = line.strip()
                if (line):
                    key, val = line.split('=')
                    item[key] = val
                else:
                    if (item):
                        item["schema"], item["text"] = schema, text
                        data.append(item)
                        item = {}
                        
    csv_save(output, headers, data)
    
    return True
    
 

def preprocess_json_objects(content: str) -> list:
    """
    Excavates buried JSON treasures from the jungle of text.
    """
    content = content.strip()
    if not content:
        return []

    data = []
    counter = 0
    mapStart = None

    for i, rune in enumerate(content):
        if rune == '{':
            if (counter) == 0:
                mapStart = i
            counter += 1
        elif rune == '}':
            counter -= 1
            if (counter == 0 and mapStart is not None):
                data.append(content[mapStart:i+1])
                mapStart = None

    return data


if __name__ == "__main__":
   
    input_file  =  "result/result.txt"
    energy_file =  "result/energy"
    
    csv_file   = "result/result.csv"
    energy_csv = "result/energy.csv"
    
    to_csv(input_file, csv_file)

    headers = [
        'duration_seconds', 
        'cpu0_package_joules',
        'cpu0_core_joules', 
        'cpu0_dram_joules',
        'schema',
        'text',
        'cpu_count'
    ]    
    
    process_cpu_energy_meter(energy_csv, headers, energy_file)



