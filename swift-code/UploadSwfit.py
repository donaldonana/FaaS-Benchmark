import swiftclient
from pathlib import Path

# Authentication details
auth_url = 'http://10.245.158.103:8080/auth/v1.0'
username = 'test:tester'
password = 'testing'

# Connect to Swift
conn = swiftclient.Connection(
    authurl=auth_url,
    user=username,
    key=password,
    auth_version='1'
)

# Create container if did not exist
container = 'whiskcontainer'
conn.put_container(container)
print(f'Container {container} created successfully.')

dirpath = Path("params")

for filepath in dirpath.iterdir():
 
    with open(filepath, 'rb') as f:
        conn.put_object(container, str(filepath).replace("params/", ""), contents=f.read())
    
    print(f'File {str(filepath).replace("params/", "")} uploaded successfully to container {container}')
    
        
 

