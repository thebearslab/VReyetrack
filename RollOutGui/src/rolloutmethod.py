# moves and calibrates .mp4 video according to user specifications
# goal: eye tracking analysis
# author: Fevronia Van Sickle
# version: 5/13/24

import os
import sys
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import subprocess
from . import class_process_video, process, compare_eye_anno



#Gui to analyse eye tracking 
class RollOutMethodInterface(tk.Tk):
    def __init__(self,newVideoPath=None, newDataPath=None, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #set window configurations
        self.geometry("750x550+430+200")
        self.title("Roll Out Method Gui")

        #create container for windows on top of the root
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (   Welcome_Page,  Step_1_Page, Step_2_Page, Step_3_Page):
            frame = F(container, self, newVideoPath=newVideoPath, newDataPath=newDataPath)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(   Welcome_Page)

        # ask user if they want to exit the application
        self.protocol("WM_DELETE_WINDOW", self.onClosing)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

     # asks user if they actually want to exit the app
    def onClosing(self):
        if messagebox.askyesno(message="Continue to quit?"):
            self.destroy()

# first page
class    Welcome_Page(tk.Frame):
    def __init__(self, parent, controller, newVideoPath, newDataPath):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.newVideoPath = newVideoPath
        self.newDataPath = newDataPath
        self.create_widgets()

    def create_widgets(self):
        
        self.title_label = ttk.Label(self, text="Home Page")

         # welcome text and file instructions
        welcomeLabel = tk.Label(self, text="Welcome to the Graphic User Interface for the Roll Out Method!", font=(
            'Times New Roman', 25))
        # welcomeLabel.place(x=20, y=20)
        welcomeLabel.pack(anchor='w', pady = 20, padx=10)

        overviewLabel1 = tk.Label(self, text="This GUI interface will walk you through three steps needed to determine attentional hitting points on 360 video stimuli: ", font=(
            'Times New Roman', 15),)
        # nextLabel.place(x=20, y=200)
        overviewLabel1.pack(anchor='w', pady = 20, padx=10)
#######
        overviewLabel2_1 = tk.Label(self, text="1. Creating video stills from your 360 video", font=(
            'Times New Roman', 15),)
        # nextLabel.place(x=20, y=200)
        overviewLabel2_1.pack(anchor='w', padx=10)

        overviewLabel2_2 = tk.Label(self, text="2. Determining areas of interest (AOIs) on your video stills at determined intervals", font=(
            'Times New Roman', 15),)
        # nextLabel.place(x=20, y=200)
        overviewLabel2_2.pack(anchor='w', padx=10)

        overviewLabel2_3 = tk.Label(self, text="3. Determining if participants’ attention falls within AOIs at each video still interval", font=(
            'Times New Roman', 15),)
        # nextLabel.place(x=20, y=200)
        overviewLabel2_3.pack(anchor='w', padx=10)

        overviewLabel3 = tk.Label(self, text="In order to use this program, you will need the following saved on your desktop:", font=(
            'Times New Roman', 15),)
        # nextLabel.place(x=20, y=200)
        overviewLabel3.pack(anchor='w', pady = 20, padx=10)

        overviewLabel4_1 = tk.Label(self, text="1. An .mp4 file of your 360 video", font=(
            'Times New Roman', 15),)
        # nextLabel.place(x=20, y=200)
        overviewLabel4_1.pack(anchor='w', padx=10)
########
        overviewLabel4_2 = tk.Label(self, text="2. An .xml file of raw eye-tracking data* derived from a participant viewing this 360 video", font=(
            'Times New Roman', 15),)
        # nextLabel.place(x=20, y=200)
        overviewLabel4_2.pack(anchor='w', padx=10)

        #goes to next page
        self.nextButton = tk.Button(self, text="Next", command=lambda: self.controller.show_frame( Step_1_Page))
        self.nextButton.pack(anchor='w', pady = 20, padx=10)

        overviewLabel5 = tk.Label(self, text="* our program is currently only compatible with output from Tobii Pro but soon to be compatible with Varjo", font=(
            'Times New Roman', 15),)
        # nextLabel.place(x=20, y=200)
        overviewLabel5.pack(anchor='w', pady = 20, padx=10)


# second page
class  Step_1_Page(tk.Frame):
    def __init__(self, parent, controller, newVideoPath, newDataPath):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.newVideoPath = newVideoPath
        self.newDataPath = newDataPath
        self.create_widgets()

    def create_widgets(self):

        # welcome text and file instructions
        choicesLabel = tk.Label(self, text="Step 1: Creating Video Stills from your 360 Video", font=(
            'Times New Roman', 25))
        choicesLabel.pack(  anchor='w', pady = 20, padx=10)

        instructionLabel1_vid = tk.Label(self, text="Select your .mp4 video file", font=(
            'Times New Roman', 15))
        instructionLabel1_vid.pack(anchor='w', padx=10)
        
        # SELECT file
        self.selectVideoButton = tk.Button(
            self, text="Select .mp4 File", command=self.selectVideoFile)
        self.selectVideoButton.pack(anchor='w', padx=10)

        instructionLabel1_file = tk.Label(self, text="Select your .xml raw eye tracking data file", font=(
            'Times New Roman', 15))
        instructionLabel1_file.pack(anchor='w', padx=10)

        # SELECT file
        self.selectXMLFileButton = tk.Button(
            self, text="Select .xml File", command=self.selectXMLFile)
        self.selectXMLFileButton.pack(anchor='w', padx=10)

        #choices
        instructionLabel2 = tk.Label(self, text="Determine if you would like your video file cropped* or flipped", font=(
            'Times New Roman', 15))
        instructionLabel2.pack(anchor='w', padx=10)

        #crop check box
        self.checkState1 = tk.IntVar()
        self.check1 = tk.Checkbutton(self, text="crop video", font=(
            'Times New Roman', 16), variable=self.checkState1)
        self.check1.pack(anchor='w', padx=10)

        #flip check box 
        self.checkState2 = tk.IntVar()
        self.check2 = tk.Checkbutton(self, text="flip video", font=(
            'Times New Roman', 16), variable=self.checkState2)
        self.check2.pack(anchor='w', padx=10)

        #set interval
        instructionLabel3 = tk.Label(self, text="Select the intervals in seconds at which you would like your video stills to be created", font=(
            'Times New Roman', 15))
        instructionLabel3.pack(anchor='w', padx=10)
        self.interval = tk.DoubleVar()
        validate_cmd = self.register(self.validate_interval)
        spinbox = tk.Spinbox(self, from_=0.5, to=3, increment=0.5, textvariable=self.interval,
                             validate='key', validatecommand=(validate_cmd, '%P'))
        spinbox.pack(anchor='w', padx=10)

########
        processLabel_1 = tk.Label(self, text="Once you click “Process Video” below, your video, video stills, and data will appear in a folder called “EyeTrack”", font=(
            'Times New Roman', 15),)
        # nextLabel.place(x=20, y=200)
        processLabel_1.pack(anchor='w', padx=10)

        nextLabel_2 = tk.Label(self, text="on your desktop. Please allow up to one minute for the video stills to be processed.", font=(
            'Times New Roman', 15),)
        # nextLabel.place(x=20, y=200)
        nextLabel_2.pack(anchor='w', padx=10)

        #process video button 
        self.processVideoButton = tk.Button(self, text="Process Video", command=self.controlSettings)
        self.processVideoButton.pack(anchor='w', pady = 5)
        #goes to next page
        self.nextButton = tk.Button(self, text="Next", command=lambda: self.controller.show_frame(Step_2_Page))
        self.nextButton.pack(anchor='w', pady = 20, padx=10)

        instructionLabel2_ast_1 = tk.Label(self, text="*cropped video should be selected if your .mp4 video file is represented in stereoscopic format", font=(
            'Times New Roman', 15))
        instructionLabel2_ast_1.pack(anchor='w', padx=10)

        instructionLabel2_ast_2 = tk.Label(self, text="(the image is duplicated on both the top and bottom half of the screen)", font=(
            'Times New Roman', 15))
        instructionLabel2_ast_2.pack(anchor='w', padx=10)

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
        self.selectVideoButton.config(text=os.path.basename(filePath))
        self.path = filePath

        # place videoFile into Eyetrack Folder
        self.newEyetrackFolder()

    # adds new folder to user desktop and places video inside
    # still needs work, will revisit over summer to prevent duplicate files
    def newEyetrackFolder(self):
        # creates new folder
        homeDir = os.path.expanduser('~')
        folder = "EyeTrack"
        # creates an Eyetrack folder in the desktop
        try:
            os.makedirs(os.path.join(homeDir, "Desktop", folder))
        except FileExistsError:
           print('Duplicate Folders Are Not Allowed. Please Rename The Folder that Is Not In Use.', file=sys.stderr)
        # save path to videoFile
        oldVideoPath = self.path
        # get video file name from path
        videoFileName = os.path.basename(oldVideoPath)
    
        #define directory path 
        self.folderPath = os.path.join(homeDir, "Desktop", folder)

        newVideoPath = os.path.join(self.folderPath, videoFileName)
        # print(newVideoPath)
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
        self.selectXMLFileButton.config(text=os.path.basename(filePath))
        self.path = filePath

        # place dataFile into Eyetrack/data Folder
        self.newDataFolder()

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

        # get video file name from path
        dataFileName = os.path.basename(oldDataPath)


        newDataPath = os.path.join(homeDir, "Desktop/Eyetrack", dataFolder + "/" + participantFolder,  destinationFolder, dataFileName)

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

    #validate spinbox input
    def validate_interval(self, new_value):
        try:
            value = float(new_value)
            return value != 0
        except ValueError:
            return False

# third page
class Step_2_Page(tk.Frame):
    def __init__(self, parent, controller, newVideoPath, newDataPath):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.newVideoPath = newVideoPath
        self.newDataPath = newDataPath
        self.create_widgets()

    def create_widgets(self):
        
        # welcome text and file instructions
        choicesLabel = tk.Label(self, text="Step 2: Determining Areas of Interest (AOIs)", font=(
            'Times New Roman', 25))
        choicesLabel.pack(  anchor='w', pady = 20, padx=10)

        instructionLabel2 = tk.Label(self, text="To determine AOIs, the roll out method uses a program called “labelme” created by Wada (2016)*", font=(
            'Times New Roman', 15))
        instructionLabel2.pack(anchor='w', padx=10)

        instructionLabel2_1 = tk.Label(self, text="To open labelme, click the button below", font=(
            'Times New Roman', 15))
        instructionLabel2_1.pack(anchor='w',padx=10)

        # start labelling button 
        self.labelMeButton = tk.Button(self, text="Annotate Frames", command=self.startLabelMe)
        self.labelMeButton.pack(anchor='w', pady = 10, padx=10)

        instructionLabel3 = tk.Label(self, text="Labelme Instructions:", font=(
            'Times New Roman', 15))
        instructionLabel3.pack(anchor='w', padx=10)

        instructionLabel4_1 = tk.Label(self, text="1. Click the “Open Dir” button on the top left of the labelme GUI", font=(
            'Times New Roman', 15))
        instructionLabel4_1.pack(  anchor='w', padx=10)

        instructionLabel4_2 = tk.Label(self, text="2. Select the EyeTrack folder", font=(
            'Times New Roman', 15))
        instructionLabel4_2.pack(  anchor='w', pady =5, padx=10)

        instructionLabel4_2_a = tk.Label(self, text="   a. Select the “crop” folder if you opted to have your video stills cropped", font=(
            'Times New Roman', 15))
        instructionLabel4_2_a.pack(  anchor='w', padx=10)

        instructionLabel4_2_b = tk.Label(self, text="   b. Select the “frames” folder if you did not opt to have your video stills cropped", font=(
            'Times New Roman', 15))
        instructionLabel4_2_b.pack(  anchor='w', pady =5, padx=10)

        instructionLabel4_3 = tk.Label(self, text="3. Click “create polygons” on the top of your labelme GUI", font=(
            'Times New Roman', 15))
        instructionLabel4_3.pack(  anchor='w', padx=10)

        instructionLabel4_4 = tk.Label(self, text="4. Draw a polygon around the AOI using mouse.When you close the polygon you will be prompted to provide a label", font=(
            'Times New Roman', 15))
        instructionLabel4_4.pack(  anchor='w', pady =5, padx=10)

        instructionLabel4_5 = tk.Label(self, text="5. You may determine multiple AOIs on each still", font=(
            'Times New Roman', 15))
        instructionLabel4_5.pack(anchor='w', padx=10)

        instructionLabel4_6 = tk.Label(self, text="6. Once you are done determining your AOI(s) press “save” and “next image”\nand repeat until you have annotated all of your video stills ", font=(
            'Times New Roman', 15))
        instructionLabel4_6.pack(  anchor='w', pady =5, padx=10)

        instructionLabel5 = tk.Label(self, text="Click “Next” to proceed to Step 3", font=(
            'Times New Roman', 15))
        instructionLabel5.pack(  anchor='w', padx=10)

        # go back button 
        self.home_button = tk.Button(self, text="Go back", command=lambda: self.controller.show_frame( Step_1_Page))
        self.home_button.pack(anchor='w', padx=10)

        #next button
        self.nextButton = tk.Button(self, text="Next", command=lambda: self.controller.show_frame(Step_3_Page))
        self.nextButton.pack(anchor='w', padx=10)
        
        instructionLabel6 = tk.Label(self, text="*available directly on github at https://github.com/wkentaro/labelme", font=(
                    'Times New Roman', 15))
        instructionLabel6.pack(  anchor='w', padx=10)

    def startLabelMe(self):
        subprocess.Popen(['labelme'])


# fourth page
class Step_3_Page(tk.Frame):
    def __init__(self, parent, controller, newVideoPath, newDataPath):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.newVideoPath = newVideoPath
        self.newDataPath = newDataPath
        self.create_widgets()

    def create_widgets(self):
        
        # welcome text and file instructions
        choicesLabel = tk.Label(self, text="Step 3: Determine participants’ attention within AOIs", font=(
            'Times New Roman', 25))
        choicesLabel.pack(  anchor='w', pady = 20, padx=10)

        # SELECT data folder
        self.selectFileButton1 = tk.Button(
            self, text="Determine Data Path", command=self.selectDataFolder)
        self.selectFileButton1.pack(anchor='w', pady = 10, padx=10)

        instructionLabel1_1 = tk.Label(self, text="Click the button above to determine the data path", font=(
            'Times New Roman', 15))
        instructionLabel1_1.pack(  anchor='w', padx=10)

        instructionLabel1_2 = tk.Label(self, text="then select Desktop -> EyeTrack -> Data and click Choose", font=(
            'Times New Roman', 15))
        instructionLabel1_2.pack(  anchor='w', padx=10)

        self.selectFileButton2 = tk.Button(
            self, text="Determine AOI Path", command=self.selectFrameFolder)
        self.selectFileButton2.pack(anchor='w', pady = 10, padx=10)

        # SELECT image directory
        instructionLabel2_1 = tk.Label(self, text="Click the button above to determine the AOI path", font=(
            'Times New Roman', 15))
        instructionLabel2_1.pack(  anchor='w', padx=10)

        # SELECT image directory
        instructionLabel2_2 = tk.Label(self, text="then select Desktop -> EyeTrack -> Frames (or Crop if you cropped your images) and click Choose", font=(
            'Times New Roman', 15))
        instructionLabel2_2.pack(  anchor='w', padx=10)
        
         # SELECT 2D hitting points csv table
        self.selectFileButton3 = tk.Button(
            self, text="Determine Attentional Hitting Points Path", command=self.selectCSVFile)
        self.selectFileButton3.pack(anchor='w', pady = 10, padx=10)

        instructionLabel4_1 = tk.Label(self, text="Click the button above to determine the participants’ Attentional Hitting Points path", font=(
            'Times New Roman', 15))
        instructionLabel4_1.pack(  anchor='w', padx=10)

        instructionLabel4_2 = tk.Label(self, text="then select Desktop -> EyeTrack -> Data -> 001 -> Eye_Data_001_xyz, then the CSV file and click Open", font=(
            'Times New Roman', 15))
        instructionLabel4_2.pack(  anchor='w', padx=10)

        #get interval
        instructionLabel5 = tk.Label(self, text="Select the intervals in seconds at which you processed your video stills in Step 1", font=(
            'Times New Roman', 15))
        instructionLabel5.pack(  anchor='w', pady = 5, padx=10)

        self.interval = tk.DoubleVar()
        validate_cmd = self.register(self.validate_interval)
        spinbox = tk.Spinbox(self, from_=0.5, to=3, increment=0.5, textvariable=self.interval,
                             validate='key', validatecommand=(validate_cmd, '%P'))
        spinbox.pack(anchor='w', padx=10)

        instructionLabel5 = tk.Label(self, text="Click Calculate to determine whether participants’ attentional hitting points fall within specified AOIs.", font=(
            'Times New Roman', 15))
        instructionLabel5.pack(  anchor='w', pady = 10, padx=10)

        self.showResultButton = tk.Button(self, text="Calculate", command=self.giveResults)
        self.showResultButton.pack( anchor='w', padx=10)

        # go back button 
        self.home_button = tk.Button(self, text="Go back", command=lambda: self.controller.show_frame( Step_1_Page))
        self.home_button.pack(  anchor='w', padx=10)

        #home button
        self.nextButton = tk.Button(self, text="Start Over", command=lambda: self.controller.show_frame(   Welcome_Page))
        self.nextButton.pack(  anchor='w',  padx=10)

    # get Data Folder
    def selectDataFolder(self):

        # open file dialog to select videoFile
        filePath = filedialog.askdirectory()

        # show what was selected
        self.selectFileButton1.config(text=os.path.basename(filePath))
    
        self.dataFolderPath = filePath

        #make sure correct folder is chosen 
        if (self.dataFolderPath.__contains__("Data")):
            subprocess.run(["python3", "RollOutGui/src/process.py", self.dataFolderPath])
        else:
            print("Please select the data folder ")
        

    # get Frame Folder
    def selectFrameFolder(self):

        # open file dialog to select videoFile
        filePath = filedialog.askdirectory()

        # show what was selected
        self.selectFileButton2.config(text=os.path.basename(filePath))

        self.framesPath = filePath

    

    #get EndImage folder
    def selectEndImageFolder(self):

        # open file dialog to select videoFile
        filePath = filedialog.askdirectory()

        # show what was selected
        self.selectFileButton3.config(text=os.path.basename(filePath))

        self.endImagePath = filePath



    # select the csv file to give results
    def selectCSVFile(self):

        filetypes = (
            ('video files', '*.csv'),
            ('All files', '*.*')
        )

        # open file dialog to select videoFile
        filePath = filedialog.askopenfilename(
            title='Open a file', initialdir='/', filetypes=filetypes)

        # show what was selected
        # self.showResultButton.config(text=os.path.basename(filePath))

        self.csvFilePath = filePath

        
    #validate spinbox input
    def validate_interval(self, new_value):
        try:
            value = float(new_value)
            return value != 0
        except ValueError:
            return False


    def giveResults(self):

        #interval
        interval = self.interval.get()
        interval *= 100000
        interval = str(interval)
        
        #this gets past the loader not knowing things at the first subprocess call
        try:
            subprocess.run(["python3", "RollOutGui/src/compare_eye_anno.py", interval, self.csvFilePath, self.framesPath])

        except:
            print("loading")

        finally:
            subprocess.run(["python3", "RollOutGui/src/compare_eye_anno.py", interval, self.csvFilePath, self.framesPath])

