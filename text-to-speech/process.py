import os
import json
import csv


def csv_save(output:str, headers:list, data:dict) -> None:
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
          

def process_cpu_energy_meter(output:str, headers:list, directory:str) -> True:
     
    data = list()
    item = dict()
    
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
    
    return True
    

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


if __name__ == "__main__":
   
    input_file = 'result/result.txt'
    csv_file   = 'result/result.csv' 
    
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
    
    process_cpu_energy_meter("result/energy.csv", headers, "energy")



