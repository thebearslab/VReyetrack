# adds new folder to user desktop and places video and appropriate py files inside
import os
homeDir = os.path.expanduser('~')


class newFolder("test.mp4"):

    # creates new folder
    def newFolder():
        os.mkdir(homeDir + "/Desktop/" + "EyeTrack")

    # add file to folder
    def fileToFolder(fileName):
        os.mkdir(homeDir + "/Desktop/EyeTrack/" + fileName)


if __name__ == '__main__':
    run = newFolder("test.mp4")
