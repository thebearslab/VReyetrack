# moves and calibrates .mp4 video according to user specifications
# goal: eye tracking analysis
# author: Fevronia Van Sickle
# version: 6/3/23

import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import class_process_video
import subprocess
import sys

#Gui to analyse eye tracking 
class RollOutMethodInterface(tk.Tk):
    def __init__(self,newVideoPath=None, newDataPath=None, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #set window configurations
        # widthxheightxhorizontalxvertical
        self.geometry("700x550+430+200")
        self.title("Roll Out Method Gui")

        # # Create a style
        # style = ttk.Style()
        # style.theme_use('clam')

        #create container for windows on top of the root
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (HomePage, CalibrationPage, CreateLabelsPage, TadaPage):
            frame = F(container, self, newVideoPath=newVideoPath, newDataPath=newDataPath)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

        # ask user if they want to exit the application
        # self.protocol("WM_DELETE_WINDOW", self.onClosing)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

     # asks user if they actually want to exit the app
    def onClosing(self):
        if messagebox.askyesno(message="Continue to quit?"):
            self.destroy()

# first page
class HomePage(tk.Frame):
    def __init__(self, parent, controller, newVideoPath, newDataPath):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.newVideoPath = newVideoPath
        self.newDataPath = newDataPath
        self.create_widgets()

    def create_widgets(self):
        
        self.title_label = ttk.Label(self, text="Home Page")

         # welcome text and file instructions
        welcomeLabel = tk.Label(self, text="Welcome to the Roll Out Method!", font=(
            'Times New Roman', 27))
        # welcomeLabel.place(x=20, y=20)
        welcomeLabel.pack(side='top', anchor='w', pady = 20, padx=10)

        overviewLabel1 = tk.Label(self, text="This GUI will walk you through all steps of the Roll Out Method.", font=(
            'Times New Roman', 15),)
        # nextLabel.place(x=20, y=200)
        overviewLabel1.pack(side='top', anchor='w', pady = 20, padx=10)

        overviewLabel2 = tk.Label(self, text="You will be asked to upload a 360 video and correpsonding eye tracking data for one participant.", font=(
            'Times New Roman', 15),)
        # nextLabel.place(x=20, y=200)
        overviewLabel2.pack(side='top', anchor='w', pady = 20, padx=10)

        overviewLabel3 = tk.Label(self, text=" On the slides that follow you will select settings for your analysis, annotate video frames, \n and recieve final analysis results.", font=(
            'Times New Roman', 15),)
        # nextLabel.place(x=20, y=200)
        overviewLabel3.pack(side='top', anchor='w', pady = 20, padx=10)

        overviewLabel4 = tk.Label(self, text="Please refer back to the paper and/or files in the repository to clarify any questions you may have.", font=(
            'Times New Roman', 15),)
        # nextLabel.place(x=20, y=200)
        overviewLabel4.pack(side='top', anchor='w', pady = 20, padx=10)

        #goes to next page
        self.nextButton = tk.Button(self, text="Next", command=lambda: self.controller.show_frame(CalibrationPage))
        self.nextButton.pack(side='top', anchor='w', pady = 20, padx=10)

# second page
class CalibrationPage(tk.Frame):
    def __init__(self, parent, controller, newVideoPath, newDataPath):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.newVideoPath = newVideoPath
        self.newDataPath = newDataPath
        self.create_widgets()

    def create_widgets(self):


        # # go back button 
        # self.home_button = tk.Button(self, text="Go back", command=lambda: self.controller.show_frame(HomePage))
        # self.home_button.pack()

        # self.title_label = tk.Label(self, text="Calibration Page")
        
        # welcome text and file instructions
        choicesLabel = tk.Label(self, text="Video Stills Creation", font=(
            'Times New Roman', 27))
        choicesLabel.pack(side='top', anchor='w', pady = 20, padx=10)

        instructionLabel1 = tk.Label(self, text="Select your mp4 video file and xml data file from the available directories.", font=(
            'Times New Roman', 15))
        # instructionLabel1.place(x=20, y=80)
        instructionLabel1.pack(side='top', anchor='w', padx=10)

        # SELECT file
        selectFileButton = tk.Button(
            self, text="Select .mp4 File", command=self.selectVideoFile)
        # selectFileButton.place(x=20, y=120)
        selectFileButton.pack(side='top', anchor='w', pady = 10, padx=10)

        # SELECT file
        selectFileButton = tk.Button(
            self, text="Select .xml File", command=self.selectXMLFile)
        # selectFileButton.place(x=20, y=120)
        selectFileButton.pack(side='top', anchor='w', pady = 0, padx=10)


        # instructionLabel1 = tk.Label(self, text="You may find that cropping your video stills vertically and flipping them horizontally to be helpful \n Please select if you would like to do so.", font=(
        #     'Times New Roman', 15))
        # instructionLabel1.pack(side='top', anchor='w', pady = 40, padx=10)

        #choices
        instructionLabel2 = tk.Label(self, text="Would you like your images cropped or flipped?", font=(
            'Times New Roman', 15))
        instructionLabel2.pack(side='top', anchor='w', padx=10)

        #crop check box
        self.checkState1 = tk.IntVar()
        self.check1 = tk.Checkbutton(self, text="crop video", font=(
            'Times New Roman', 16), variable=self.checkState1)
        self.check1.pack(padx=10, pady=10)

        #flip check box 
        self.checkState2 = tk.IntVar()
        self.check2 = tk.Checkbutton(self, text="flip video", font=(
            'Times New Roman', 16), variable=self.checkState2)
        self.check2.pack(pady=10)

        #set interval
        instructionLabel3 = tk.Label(self, text="Please select the interval you would like to use.", font=(
            'Times New Roman', 15))
        instructionLabel3.pack(side='top', anchor='w', padx=10)
        self.interval = tk.DoubleVar()
        spinbox = tk.Spinbox(self, from_=0, to=3, increment=0.5, textvariable=self.interval)
        spinbox.pack(pady=10)

        nextLabel = tk.Label(self, text="After you have made your selections, press 'Process Video' to create video stills .", font=(
            'Times New Roman', 15),)
        # nextLabel.place(x=20, y=200)
        nextLabel.pack(side='top', anchor='w', pady = 5, padx=10)


        self.processVideoButton = tk.Button(self, text="Process Video", command=self.controlSettings)
        self.processVideoButton.pack()

        instructionLabel2 = tk.Label(self, text="Your video, data, and stills will appear inside the 'Eyetrack' folder on your desktop. \n Please allow time for the folder to populate.", font=(
            'Times New Roman', 15))
        # instructionLabel2.place(x=20, y=180)
        instructionLabel2.pack(side='top', anchor='w', padx=10)

        #goes to next page
        self.nextButton = tk.Button(self, text="Next", command=lambda: self.controller.show_frame(CreateLabelsPage))
        self.nextButton.pack(side='top', anchor='w', pady = 20, padx=10)

    # select the directory holding the video file
    def selectVideoFile(self):

        filetypes = (
            ('video files', '*.mp4'),
            ('All files', '*.*')
        )

        # open file dialog to select videoFile
        filePath = filedialog.askopenfilename(
            title='Open a file', initialdir='/', filetypes=filetypes)

        # show what was selected
        messagebox.showinfo(
            title='Selected File',
            message=filePath
        )
        self.path = filePath

        self.count = 0
        # place videoFile into Eyetrack Folder
        self.newEyetrackFolder(self.count)

    # adds new folder to user desktop and places video inside
    def newEyetrackFolder(self, count):

        # creates new folder
        homeDir = os.path.expanduser('~')
        folder = "EyeTrack"

        # creates an Eyetrack folder in the desktop
        try:
            os.makedirs(os.path.join(homeDir, "Desktop", folder))
        except:
            # breaks from try/except
            folder = "Eyetrack" + str(count)
            count += 1
            self.newEyetrackFolder(count)


        # save path to videoFile
        oldVideoPath = self.path
        print(oldVideoPath)
        # get video file name from path
        videoFileName = os.path.basename(oldVideoPath)
        print(videoFileName)

        #define directory path 
        self.folderPath = os.path.join(homeDir, "Desktop", folder)

        newVideoPath = os.path.join(self.folderPath, videoFileName)

        print(newVideoPath)
        shutil.move(oldVideoPath, newVideoPath)

    # select the directory holding the video file
    def selectXMLFile(self):

        filetypes = (
            ('video files', '*.xml'),
            ('All files', '*.*')
        )

        # open file dialog to select videoFile
        filePath = filedialog.askopenfilename(
            title='Open a file', initialdir='/', filetypes=filetypes)

        # show what was selected
        messagebox.showinfo(
            title='Selected File',
            message=filePath
        )
        self.path = filePath

        # place dataFile into Eyetrack/data Folder
        self.newDataFolder()

    # adds new folder to Eyetrack folder and places dataFile inside
    def newDataFolder(self):

        # creates new folder
        homeDir = os.path.expanduser('~')
        dataFolder = "Data"
        participantFolder = "001"
        destinationFolder = "Eye_Data_001"

        # creates an eyetrack/data folder in the desktop
        try:
            os.makedirs(os.path.join(homeDir, "Desktop/Eyetrack", dataFolder, participantFolder, destinationFolder))
        except:
            # breaks from try/except
            passed = True

        # save path to videoFile
        oldDataPath = self.path
        print(oldDataPath)
        # get video file name from path
        dataFileName = os.path.basename(oldDataPath)
        print(dataFileName)

        newDataPath = os.path.join(homeDir, "Desktop/Eyetrack", dataFolder + "/" + participantFolder,  destinationFolder, dataFileName)
        print(newDataPath)
        shutil.move(oldDataPath, newDataPath)

    #control settings
    def controlSettings(self):

        #crop
        if self.checkState1.get() == 0:
            cropBool = 0
        else:
            cropBool = 1

        #flip
        if self.checkState2.get() == 0:
            flipBool = 0
        else:
            flipBool = 1

        #interval
        interval = self.interval.get()
        interval = float(interval)

        #process the video
        self.frames = class_process_video.processVideo(self.folderPath, self.interval)
        self.frames.setOutputPath()
        self.frames.captureAtInterval(interval)
        self.frames.cropFrames(cropBool)
        self.frames.flipFrames(flipBool)

# third page
class CreateLabelsPage(tk.Frame):
    def __init__(self, parent, controller, newVideoPath, newDataPath):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.newVideoPath = newVideoPath
        self.newDataPath = newDataPath
        self.create_widgets()

    def create_widgets(self):
        
        # welcome text and file instructions
        choicesLabel = tk.Label(self, text="Create AOIs", font=(
            'Times New Roman', 27))
        choicesLabel.pack(side='top', anchor='w', pady = 20, padx=10)

        instructionLabel2 = tk.Label(self, text="Annotate video frames to determine Areas of Interest.", font=(
            'Times New Roman', 15))
        # instructionLabel2.place(x=20, y=180)
        instructionLabel2.pack(side='top', anchor='w', pady = 20, padx=10)

        instructionLabel3 = tk.Label(self, text="Save annotated frames to the folder of the frames you want to analyze; choose either 'frames', 'crop', or 'flip'.", font=(
            'Times New Roman', 15))
        # instructionLabel2.place(x=20, y=180)
        instructionLabel3.pack(side='top', anchor='w', pady = 10, padx=10)

        instructionLabel4 = tk.Label(self, text="Return to this GUI once done annotating.", font=(
            'Times New Roman', 15))
        # instructionLabel2.place(x=20, y=180)
        instructionLabel4.pack(side='top', anchor='w', pady = 10, padx=10)

        instructionLabel5 = tk.Label(self, text="If you accidentally close the GUI, simply navigate back to this page and continue.", font=(
            'Times New Roman', 15))
        # instructionLabel2.place(x=20, y=180)
        instructionLabel5.pack(side='top', anchor='w', pady = 10, padx=10)

        instructionLabel6 = tk.Label(self, text="You do not need to re-annotate your slides.", font=(
            'Times New Roman', 15))
        # instructionLabel2.place(x=20, y=180)
        instructionLabel6.pack(side='top', anchor='w', pady = 10, padx=10)

        # start labelling button 
        self.labelMeButton = tk.Button(self, text="Annotate Frames", command=self.startLabelMe)
        self.labelMeButton.pack(side='top', anchor='w', pady = 20, padx=10)

        # go back button 
        self.home_button = tk.Button(self, text="Go back", command=lambda: self.controller.show_frame(CalibrationPage))
        self.home_button.pack(side='top', anchor='w', pady = 20, padx=10)

        #next button
        self.nextButton = tk.Button(self, text="Next", command=lambda: self.controller.show_frame(TadaPage))
        self.nextButton.pack(side='top', anchor='w', pady = 20, padx=10)

    def startLabelMe(self):
        subprocess.Popen(['labelme'])


# fourth page
class TadaPage(tk.Frame):
    def __init__(self, parent, controller, newVideoPath, newDataPath):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.newVideoPath = newVideoPath
        self.newDataPath = newDataPath
        self.create_widgets()

    def create_widgets(self):
        
        # welcome text and file instructions
        choicesLabel = tk.Label(self, text="Data Tables and Hitting Points", font=(
            'Times New Roman', 27))
        choicesLabel.pack(side='top', anchor='w', pady = 20, padx=10)


        # instructionLabel1 = tk.Label(self, text="Calculate the hitting points. \n This will produce a csv table of x,y coordinates from participant eye tracking data", font=(
        #     'Times New Roman', 15))
        # # instructionLabel2.place(x=20, y=180)
        # instructionLabel1.pack(side='top', anchor='w')

        instructionLabel1 = tk.Label(self, text="Select the 'data' directory from within Desktop/Eyetrack", font=(
            'Times New Roman', 15))
        # instructionLabel1.place(x=20, y=80)
        instructionLabel1.pack(side='top', anchor='w', padx=10)

        # SELECT data folder
        selectFileButton1 = tk.Button(
            self, text="Select data folder", command=self.selectDataFolder)
        # selectFileButton.place(x=20, y=120)
        selectFileButton1.pack(side='top', anchor='w', pady = 10, padx=10)

        # SELECT image directory
        instructionLabel2 = tk.Label(self, text="Select the frames directory containing the frames and annotated frames you want analyzed", font=(
            'Times New Roman', 15))
        # instructionLabel1.place(x=20, y=80)
        instructionLabel2.pack(side='top', anchor='w', padx=10)

        selectFileButton2 = tk.Button(
            self, text="Select frames folder", command=self.selectFrameFolder)
        # selectFileButton.place(x=20, y=120)
        selectFileButton2.pack(side='top', anchor='w', pady = 10, padx=10)

        # SELECT end image directory
        instructionLabel3 = tk.Label(self, text="Select a directory for the analysis frames to be placed", font=(
            'Times New Roman', 15))
        # instructionLabel1.place(x=20, y=80)
        instructionLabel3.pack(side='top', anchor='w', padx=10)

        selectFileButton3 = tk.Button(
            self, text="Select image results folder", command=self.selectEndImageFolder)
        # selectFileButton.place(x=20, y=120)
        selectFileButton3.pack(side='top', anchor='w', pady = 10, padx=10)

        # SELECT 2D hitting points csv table
        instructionLabel4 = tk.Label(self, text="Select the csv table containing 2D hitting points located within new participant xyz folder", font=(
            'Times New Roman', 15))
        # instructionLabel1.place(x=20, y=80)
        instructionLabel4.pack(side='top', anchor='w', padx=10)

        selectFileButton4 = tk.Button(
            self, text="Select 2D hitting points", command=self.selectCSVFile)
        # selectFileButton.place(x=20, y=120)
        selectFileButton4.pack(side='top', anchor='w', pady = 10, padx=10)

        #get interval
        instructionLabel5 = tk.Label(self, text="Which interval did you select for your frames?", font=(
            'Times New Roman', 15))
        instructionLabel5.pack(side='top', anchor='w', padx=10)
        self.interval = tk.DoubleVar()
        spinbox = tk.Spinbox(self, from_=0, to=3, increment=0.5, textvariable=self.interval)
        spinbox.pack(pady=10)


        self.showResultButton = tk.Button(self, text="Calculate results", command=self.giveResults)
        self.showResultButton.pack(side='top', anchor='w', pady = 20, padx=10)

        # go back button 
        self.home_button = tk.Button(self, text="Go back", command=lambda: self.controller.show_frame(CalibrationPage))
        self.home_button.pack(side='top', anchor='w', pady = 10, padx=10)

        # #next button
        # self.nextButton = tk.Button(self, text="Next", command=lambda: self.controller.show_frame(TadaPage))
        # self.nextButton.pack(side='top', anchor='w', pady = 20, padx=10)
        
        #home button
        self.nextButton = tk.Button(self, text="Home", command=lambda: self.controller.show_frame(HomePage))
        self.nextButton.pack(side='top', anchor='w', pady = 20, padx=10)

    # get Data Folder
    def selectDataFolder(self):

        # open file dialog to select videoFile
        filepath = filedialog.askdirectory()

        # show what was selected
        messagebox.showinfo(
            title='Selected folder',
            message=filepath
        )
        self.dataFolderPath = filepath

        subprocess.run(["python3", "process.py", self.dataFolderPath])
        

    # get Frame Folder
    def selectFrameFolder(self):

        # open file dialog to select videoFile
        filepath = filedialog.askdirectory()

        # show what was selected
        messagebox.showinfo(
            title='Selected folder',
            message=filepath
        )

        self.framesPath = filepath
        print(self.framesPath)
    
    #get EndImage folder
    def selectEndImageFolder(self):

        # open file dialog to select videoFile
        filepath = filedialog.askdirectory()

        # show what was selected
        messagebox.showinfo(
            title='Selected folder',
            message=filepath
        )

        self.endImagePath = filepath
        print(self.endImagePath)

    # select the directory holding the video file
    def selectCSVFile(self):

        filetypes = (
            ('video files', '*.csv'),
            ('All files', '*.*')
        )

        # open file dialog to select videoFile
        filepath = filedialog.askopenfilename(
            title='Open a file', initialdir='/', filetypes=filetypes)

        # show what was selected
        messagebox.showinfo(
            title='Selected File',
            message=filepath
        )

        self.csvFilePath = filepath
        print(self.csvFilePath)
        

    def giveResults(self):
        print("this is giveResults")

        #interval
        interval = self.interval.get()
        interval *= 100000
        interval = str(interval)
        

        #calculate results
        subprocess.run(["python3", "compare_eye_anno.py", interval, self.csvFilePath, self.framesPath, self.endImagePath])
        # subprocess.run(["python3", "compare_eye_anno.py", interval])


appROM = RollOutMethodInterface()
appROM.mainloop()
