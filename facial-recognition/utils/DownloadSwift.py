import swiftclient

# Authentication details
auth_url = 'http://172.20.20.78:8080/auth/v1.0'
username = 'test:tester'
password = 'testing'

# Connect to Swift
conn = swiftclient.Connection(
    authurl=auth_url,
    user=username,
    key=password,
    auth_version='1'
)

# Create a container
container = 'whiskcontainer'
#conn.put_container(container_name)
#print(f'Container {container_name} created successfully.')



for i in range(10):
	
	path = f'./chunk.{i}.mp4'
	file_name = f'chunk.{i}.mp4'
	obj = conn.get_object(container, file_name)
	with open(path, 'wb') as f:
		f.write(obj[1])
		
	print(f'File {file_name} downloaded successfully from container {container} to {path}')

