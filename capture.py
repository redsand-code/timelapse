import os
import numpy as np
import cv2
import time
import datetime

from utils import CFEVideoConf, image_resize, write_time
import glob

cap = cv2.VideoCapture(0)

frames_per_seconds = 20
now = datetime.datetime.now()
data_path = now.strftime("%Y.%m.%d")
save_path = f"saved-media/Ryder-Sleep-{data_path}.mp4"

config = CFEVideoConf(cap, filepath=save_path, res='720p')
out = cv2.VideoWriter(save_path, config.video_type,
                      frames_per_seconds, config.dims)

timelapse_img_dir = 'images/timelapse/'
hours_duration = 9
seconds_duration = 20
seconds_between_shots = 20

if not os.path.exists('saved-media/'):
    os.mkdir('saved-media/')

if not os.path.exists('images/'):
    os.mkdir('images/')
    os.mkdir(timelapse_img_dir)

#finish_time = now + datetime.timedelta(seconds=seconds_duration)
#finish_time = now + datetime.timedelta(hours=hours_duration)

tomorrow = now + datetime.timedelta(days=1)
morning = datetime.time(6, 40)
finish_time = datetime.datetime.combine(tomorrow.date(), morning)

i = 0
while datetime.datetime.now() < finish_time:
    '''
    Ensure that the current time is still less
    than the preset finish time
    '''
    ret, frame = cap.read()
    filename = f"{timelapse_img_dir}/{i}.jpg"
    i += 1

    write_time(frame, filename)

    #cv2.imwrite(filename, frame)
    time.sleep(seconds_between_shots)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break


def images_to_video(out, image_dir, clear_images=True):
    image_list = glob.glob(f"{image_dir}/*.jpg")
    sorted_images = sorted(image_list, key=os.path.getmtime)
    for file in sorted_images:
        image_frame = cv2.imread(file)
        out.write(image_frame)
    if clear_images:
        '''
        Remove stored timelapse images
        '''
        for file in image_list:
            os.remove(file)


images_to_video(out, timelapse_img_dir)
# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()
