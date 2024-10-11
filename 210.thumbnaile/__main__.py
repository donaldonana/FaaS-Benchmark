import datetime
import os
import swiftclient
import cv2
import pygame


def opencv_resize(path, w, h):
    # Load the image
    img = cv2.imread(path)
    # resize image by specifying custom width and height
    resized = cv2.resize(img, (w, h))
    resize_image = "resize_"+path
    # Save the reduced image
    cv2.imwrite(resize_image, resized)
    return resize_image


def pygame_resize(path, w, h):
    pygame.init()
    image = pygame.image.load(path)
    reduced_image = pygame.transform.scale(image, (w, h))
    resize_image = "resize_"+path
    pygame.image.save(reduced_image, resize_image)
    pygame.quit()

    return resize_image


def wand_resize(path, w, h):
    from wand.image import Image
    img = Image(filename = path)
    img.resize(w, h)
    resize_image = "resize_"+path
    img.save(filename=resize_image)

    return resize_image

 
def pillow_resize(path, w, h):
    from PIL import Image
    img = Image.open(path)
    img.thumbnail((w,h))
    resize_image = "resize_"+path
    img.save(resize_image)

    return resize_image
       

def resize(args):
  
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


    # Image Resizing
    process_begin = datetime.datetime.now()
    out = biblio[args["bib"]](args["file"], args["width"], args["hight"])
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
            'image' : args["file"]
        }


biblio = {'opencv' : opencv_resize, 'pillow' : pillow_resize, 'wand' : wand_resize, 'pygame' : pygame_resize}

def main(args):
 
    # Apply Resize Operation 
    result = resize({

        "width" : args.get("width", 60),
        "hight" : args.get("height", 60),
        "file"  : args.get("file", '15Mb.JPEG'),
        "bib"   : args.get("bib", "pillow"),
        "ipv4"  : args.get("ipv4", " ")

    })

    return result
    
 