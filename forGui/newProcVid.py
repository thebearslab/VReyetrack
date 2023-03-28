import cv2
import sys
import os
from PIL import Image


class VideoFrameCutter:
    def __init__(self, video_path, frame_rate):
        self.video_path = video_path
        self.framename = 'frames'
        self.dirname = '/'.join(video_path.split('.')[0].split('/')[:-1])
        self.output_path = self.dirname + '/' + self.framename + '/'
        self.frameRate = frame_rate

    def get_frames(self):
        vidcap = cv2.VideoCapture(self.video_path)
        os.makedirs(self.output_path)
        sec = 0
        count = 0
        success = self.get_frame(vidcap, sec, count)
        while success:
            count += 1
            sec += self.frameRate
            sec = round(sec, 2)
            success = self.get_frame(vidcap, sec, count)

    def get_frame(self, vidcap, sec, count):
        vidcap.set(cv2.CAP_PROP_POS_MSEC, sec*1000)
        hasFrames, image = vidcap.read()
        if hasFrames:
            cv2.imwrite(self.output_path + "image" +
                        str("{0:02d}".format(count))+".jpg", image)
        return hasFrames

    def crop_frames(self):
        framedirname = self.dirname + '/' + self.framename
        file_list = os.listdir(framedirname)
        output_path = self.dirname + '/' + 'crop' + '/'
        os.makedirs(output_path)
        for img_name in file_list:
            if 'jpg' in img_name:
                im = Image.open(framedirname + '/' + img_name)
                width, height = im.size
                left = 0
                top = 0
                right = width
                bottom = height / 2
                im1 = im.crop((left, top, right, bottom))
                im1.save(output_path + img_name)

    def flip_frames(self):
        flipdirname = self.dirname + '/' + 'crop'
        file_list = os.listdir(flipdirname)
        output_path = self.dirname + '/' + 'flip' + '/'
        os.makedirs(output_path)
        for image_path in file_list:
            if 'jpg' in image_path:
                image_obj = Image.open(flipdirname + '/' + image_path)
                rotated_image = image_obj.transpose(Image.FLIP_LEFT_RIGHT)
                rotated_image.save(output_path + image_path)

        print('finish this video')
