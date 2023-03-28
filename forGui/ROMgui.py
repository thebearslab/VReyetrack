# gui takes in video from user and saves it to a new folder on the desktop
# @author Fevronia Van Sickle
# @version 3/23/23
# from logging import root
import tkinter as tk
import os
import shutil
from tkinter import Entry, Toplevel, messagebox, Button
from tkinter import filedialog
from tkinter import ttk

class RollOutMethodInterface (tk.Frame):

       # initializer
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.initializeUserInterface()

    # initialize window
    def initializeUserInterface(self):

        # create window
        self.root.title("Roll Out Method Gui")
        self.root.geometry("500x300+450+300")
        # set color
        self.root.configure(bg='#f2e3c6')
        # Create a style
        style = ttk.Style(root)
        # Set the theme with the theme_use method
        style.theme_use('clam')

         # welcome text and file instructions
        welcomeLabel = ttk.Label(self.root, text="Welcome!", font=(
            'Times New Roman', 27))
        welcomeLabel.place(x=20, y=20)

        instructionLabel1 = ttk.Label(self.root, text="Please select your mp4 video file from the available directories.", font=(
            'Times New Roman', 15))
        instructionLabel1.place(x=20, y=80)

        instructionLabel2 = ttk.Label(self.root, text="Your video will appear inside the 'Eyetrack' folder on your desktop.", font=(
            'Times New Roman', 15))
        instructionLabel2.place(x=20, y=180)

        nextLabel = ttk.Label(self.root, text="After you have made your selection, press 'Next' to continue.", font=(
            'Times New Roman', 15))
        nextLabel.place(x=20, y=200)

        # SELECT file
        selectFileButton = ttk.Button(
            self.root, text="Select File", command=self.selectVideoFile)
        selectFileButton.place(x=20, y=120)


        # pressing NEXT button goes to page one
        nextButton = ttk.Button(
            self.root, text="Next") 
        nextButton.place(x=20, y=240)

        # ask user if they want to exit the application
        # self.protocol("WM_DELETE_WINDOW", self.onClosing)

        # asks user if they actually want to exit the app
    def onClosing(self):
        if messagebox.askyesno(message="Continue to quit?"):
            self.root.destroy()

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

        # self.path = os.path.dirname(filePath)
        self.path = filePath

        # place videoFile into Eyetrack Folder
        self.newFolder()

        # return self.path

        # adds new folder to user desktop and places video inside

    def newFolder(self):

        # creates new folder
        homeDir = os.path.expanduser('~')
        folder = "EyeTrack"

        # creates an Eyetrack folder in the desktop
        try:
            os.makedirs(os.path.join(homeDir, "Desktop", folder))
        except:
            # breaks from try/except
            passed = True

        # save path to videoFile
        oldVideoPath = self.path
        print(oldVideoPath)
        # get video file name from path
        videoFileName = os.path.basename(oldVideoPath)
        print(videoFileName)

        newVideoPath = os.path.join(homeDir, "Desktop", folder, videoFileName)
        print(newVideoPath)
        shutil.move(oldVideoPath, newVideoPath)

if __name__ == '__main__':
    root = tk.Tk()
    run = RollOutMethodInterface(root)
    root.mainloop()
# appROM = RollOutMethodInterface()
# appROM.mainloop()

