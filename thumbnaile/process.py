import os
import csv
import json
import pandas as pd


def csv_save(output, headers, data) -> True:
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
    
    return True

 
def metric_precess(content: str, headers: list, csv_file: str) -> True:
    """
    Excavates buried JSON treasures from the jungle of text.
    """
    content = content.strip()
    if not content:
        return []

    data = []
    counter = 0
    mapStart = None
    
    with open(input_file, 'r') as file:
        content = file.read()
        
    for i, char in enumerate(content):
        if char == '{':
            if (counter) == 0:
                mapStart = i
            counter += 1
        elif char == '}':
            counter -= 1
            if (counter == 0 and mapStart is not None):
                obj = content[mapStart:i+1]
                data.append(json.loads(obj))
                mapStart = None

    csv_save(csv_file, headers, data)
    
    return True
    
    
def process_cpu_energy_meter(output:str, headers:list, energy_file:str) -> True:
    """
    Parse cpu energy meter result files 
    """
    data = list()
    item = dict()
    
    # For each subfolder in Energy folder (1Mb.JPEG).
    for dir in os.listdir("result/energy"):
        dir_path = os.path.join("result/energy", dir)
        image = dir.replace(".JPEG", "")

        # For each file in the subfolder. 
        for file in os.listdir(dir_path):  
            file_path = os.path.join(dir_path, file)
            library = file.replace(image+".JPEG.txt", "")

            with open(file_path, 'r') as file:
                lines = file.readlines()
                
            for line in lines:
                line = line.strip()
                if (line):
                    key, val = line.split('=')
                    item[key] = val
                else:
                    if (item):
                        item["image"], item["library"] = image, library
                        data.append(item)
                        item = {}
                        
    csv_save(output, headers, data)
    
    return True
    

if __name__ == "__main__":
    
    input_file  =  "result/result.txt"
    energy_file =  "result/energy"
    
    csv_file   = "result/result.csv"
    energy_csv = "result/energy.csv"
    
    
    # Define CSV headers for others data proc. 
    headers = [
        "compute_time", 
        "download_size", 
        "download_time", 
        "image", 
        "library", 
        "upload_size", 
        "upload_time"
    ]
    
    metric_precess(input_file, headers, csv_file)
    
    headers = [
        'duration_seconds', 
        'cpu0_package_joules',
        'cpu0_core_joules', 
        'cpu0_dram_joules', 
        'image', 
        'library',
        'cpu_count'
    ]
    
    process_cpu_energy_meter(energy_csv, headers, energy_file)


    

    

