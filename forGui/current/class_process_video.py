import cv2
import os
from PIL import Image

class processVideo():
    def __init__(self, videoPath):
        self.filenamepath = videoPath
        print(self.filenamepath)

    #set interval
    def setInterval(self, interval):
        self.interval = interval
        print(interval)

    # saves new folder "frames" to filenamepath
    def setOutputPath(self):
        
        filenamepath = self.filenamepath 
        video_file_list = os.listdir(filenamepath)
        videoname = ''
        print(video_file_list)
        for f in video_file_list:
            if 'mp4' in f:
                videoname = filenamepath + '/' + f 

        self.vidcap = cv2.VideoCapture(videoname)

        self.framename = 'frames'
        self.dirname = '/'.join(videoname.split('.')[0].split('/')[:-1])
        self.output_path = self.dirname + '/' + self.framename + '/'

        os.makedirs(self.output_path)
        print(self.output_path)


    def getFrame(self, sec):

        vidcap = self.vidcap
        output_path = self.output_path

        vidcap.set(cv2.CAP_PROP_POS_MSEC, sec*1000)
        hasFrames, image = vidcap.read()
        if hasFrames:
            # save frame as JPG file
            cv2.imwrite(output_path + "image" +
                        str("{0:02d}".format(self.count))+".jpg", image)
        return hasFrames


    # set cut video into frames at interval rate 
    def captureAtInterval(self, interval):

        frameRate = interval
        sec = 0
        # frameRate = 0.5  # //it will capture image in each 0.5 second
        self.count = 0
        success = self.getFrame(sec)
        while success:
            self.count = self.count + 1
            sec = sec + frameRate
            sec = round(sec, 2)
            success = self.getFrame(sec)


    # crop
    def cropFrames(self):
        framedirname = self.dirname + '/' + self.framename
        print("the script has the name %s" % (framedirname))
        file_list = os.listdir(framedirname)

        output_path = self.dirname + '/' + 'crop' + '/'

        os.makedirs(output_path)
        # print(file_list)
        for img_name in file_list:

            if 'jpg' in img_name:
                # Opens a image in RGB mode
                im = Image.open(framedirname + '/' + img_name)

                # Size of the image in pixels (size of orginal image)
                # (This is not mandatory)
                width, height = im.size

                # Setting the points for cropped image
                left = 0
                top = 0
                right = width
                bottom = height / 2

                # Cropped image of above dimension
                # (It will not change orginal image)
                im1 = im.crop((left, top, right, bottom))

                # Shows the image in image viewer
                im1.save(output_path + img_name)

        self.img_name = img_name

        # flip
    def flipFrames(self):
        flipdirname = self.dirname + '/' + 'crop'
        print("the script has the name %s" % (flipdirname))
        file_list = os.listdir(flipdirname)

        output_path = self.dirname + '/' + 'flip' + '/'

        os.makedirs(output_path)
        # print(file_list)
        for image_path in file_list:

            if 'jpg' in self.img_name:
                image_obj = Image.open(flipdirname + '/' + image_path)
                rotated_image = image_obj.transpose(Image.FLIP_LEFT_RIGHT)
                rotated_image.save(output_path + image_path)


if __name__ == "__main__":

    #instantiate class 
    frames = processVideo("/Users/fevroniavansickle/Desktop/EyeTrack")

    frames.setInterval(0.5)
    frames.setOutputPath()
    frames.captureAtInterval(0.5)
    frames.cropFrames()
    frames.flipFrames()
    


