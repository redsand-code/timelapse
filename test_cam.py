import cv2
import datetime
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from skimage.metrics import structural_similarity as ssim


def test_image():
    # Open an Image
    img = Image.open('images/timelapse/0.jpg')

    I1 = ImageDraw.Draw(img)

    now = datetime.datetime.now()
    label = now.strftime("%I:%M:%S %p")

    ifont = ImageFont.truetype('Helvetica', 40)
    I1.text((1000, 600), label, font=ifont, fill=(200, 200, 200))

    img.show()
    # img.save("0.1.jpg")


def get_hour():
    now = datetime.datetime.now()
    morning = datetime.time(6, 40)
    print(now.strftime("%Y-%m-%d %H:%M:%S"))

    tomorrow = now + datetime.timedelta(days=1)

    finish_time = datetime.datetime.combine(tomorrow.date(), morning)
    print(finish_time.strftime("%Y-%m-%d %H:%M:%S"))

    return


def test_cam():
    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)

    if vc.isOpened():  # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    last_frame = None

    while rval:
        cv2.imshow("preview", frame)
        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break

    vc.release()
    cv2.destroyWindow("preview")


def compare():
    img0 = Image.open('images/timelapse/0.jpg')
    img1 = Image.open('images/timelapse/1.jpg')
    simlarityIndex = ssim(img0, img1)
    print(simlarityIndex)


compare()
