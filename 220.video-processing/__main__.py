import os
import swiftclient
import datetime
import subprocess
from PIL import Image


def video_to_gif_moviepy(input_video_path):

    from moviepy.editor import VideoFileClip

    # Load the video
    clip = VideoFileClip(input_video_path)
    
    output_gif_path = "output.gif"
    # Write the GIF file
    clip.write_gif(output_gif_path)

    return output_gif_path
    

def video_to_gif_imageio(input_video_path):

    import imageio

    # Load the video
    reader = imageio.get_reader(input_video_path)
    
    # Write the GIF file
    output_gif_path = "output.gif"

    writer = imageio.get_writer(output_gif_path)

    for frame in reader:
        writer.append_data(frame)
    writer.close()

    return output_gif_path
    

def video_to_gif_opencv(input_video_path):

    import cv2

    # Open the video file
    cap = cv2.VideoCapture(input_video_path)
    frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Convert the frame to RGB (PIL uses RGB instead of BGR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Append frame to the list
        frames.append(Image.fromarray(frame))

    cap.release()

    # Save frames as a GIF
    output_gif_path = "output.gif"
    frames[0].save(output_gif_path, save_all=True, append_images=frames[1:], loop=0)

    return output_gif_path
    

def video_to_gif_ffmpeg(input_video_path):

    output_gif_path = "output.gif"

    args = ["-i", input_video_path, output_gif_path]
        
    ret = subprocess.run(["ffmpeg", '-y'] + args,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
     
    return output_gif_path
        

def handler(args):

    # Swift identifiant
    auth_url = f'http://{args["ipv4"]}:8080/auth/v1.0'
    username = 'test:tester'
    password = 'testing'

    # Connect to Swift
    conn = swiftclient.Connection(
    	authurl=auth_url,
    	user=username,
    	key=password,
    	auth_version='1'
	)

    container = 'whiskcontainer'
     
    # Image Downloading
    download_begin = datetime.datetime.now()
    obj = conn.get_object(container, args["file"])
    with open(args["file"], 'wb') as f:
        f.write(obj[1])
    download_end = datetime.datetime.now()
    
    download_size = os.path.getsize(args["file"])
    
    # Video to Gif Transformation
    process_begin = datetime.datetime.now()
    out = biblio[args["bib"]](args["file"])
    process_end = datetime.datetime.now()
    out_size = os.path.getsize(out)
    
    # Result Uploading
    upload_begin = datetime.datetime.now()
    with open(out, 'rb') as f:
        conn.put_object(container, out, contents=f.read())
    upload_end = datetime.datetime.now()
    
    download_time = (download_end - download_begin) / datetime.timedelta(seconds=1)
    upload_time = (upload_end - upload_begin) / datetime.timedelta(seconds=1)
    process_time = (process_end - process_begin) / datetime.timedelta(seconds=1)
    
    return {      
            'download_time': download_time,
            'download_size': download_size,
            'upload_time': upload_time,
            'upload_size': out_size,
            'compute_time': process_time,
            'library' : args["bib"],
            'video' : args["file"]
    }


biblio = {'moviepy' : video_to_gif_moviepy, 'ffmpeg' : video_to_gif_ffmpeg, 'imageio' : video_to_gif_imageio, 'opencv' : video_to_gif_opencv}

def main(args):

    # Apply Resize Operation 
    result = handler({

        "file"  : args.get("file", '1Mb.avi'),
        "bib"   : args.get("bib", "ffmpeg"),
        "ipv4": args.get("ipv4", "192.168.1.120")

    })

    return result
