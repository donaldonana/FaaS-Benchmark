import json

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

def replace_field_name(input_file, output_file, old_field_name, new_field_name, schema_values):
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
        if entry.get('schema') in schema_values and old_field_name in entry:
            entry[new_field_name] = entry.pop(old_field_name)

    # Write the modified data to a new file
    with open(output_file, 'w') as file:
        for entry in data:
            file.write(json.dumps(entry, indent=4) + '\n')

# Usage
input_file = 'result.txt'
output_file = 'log_modified.txt'
old_field_name = 'facerecprim'
new_field_name = 'facerec'
schema_values = ['S1', 'S5', 'S7']

replace_field_name(input_file, output_file, old_field_name, new_field_name, schema_values)

