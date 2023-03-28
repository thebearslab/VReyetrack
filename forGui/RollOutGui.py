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


class RollOutMethodInterface (tk.Tk):

    # initializer
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.root = tk.Tk()
        self.root.title("home page")

        # container = tk.Frame(root, width=200, height=200)
        container = tk.Frame(self.root)
        container.pack(side="top", fill="both", expand=True)

        # container.grid_rowconfigure(0, weight=1)
        # container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # for F in (HomePage, PageOne, PageTwo):
        frame = self.root(container, self)
        self.frames[HomePage] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        # shows the root window aka homepage
        self.show_frame(HomePage)

    # raises each window to be the top level window
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class HomePage(tk.Tk):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.path = None
        self.widgets()

    def widgets(self):

        # create window
        self.title("home page")
        self.geometry("500x300+450+300")
        # set color
        self.configure(bg='#f9f1f1')
        # Create a style
        style = ttk.Style(self)
        # Set the theme with the theme_use method
        style.theme_use('clam')

        # welcome text and file instructions
        welcomeLabel = ttk.Label(self.root, text="Welcome!", font=(
            'Times New Roman', 27))
        welcomeLabel.place(x=20, y=20)

        instructionLabel1 = ttk.Label(self, text="Please select your mp4 video file from the available directories.", font=(
            'Times New Roman', 15))
        instructionLabel1.place(x=20, y=80)

        instructionLabel2 = ttk.Label(self, text="Your video will appear inside the 'Eyetrack' folder on your desktop.", font=(
            'Times New Roman', 15))
        instructionLabel2.place(x=20, y=180)

        nextLabel = ttk.Label(self, text="After you have made your selection, press 'Next' to continue.", font=(
            'Times New Roman', 15))
        nextLabel.place(x=20, y=200)

        # SELECT file
        selectFileButton = ttk.Button(
            self, text="Select File", command=self.selectVideoFile)
        selectFileButton.place(x=20, y=120)

        # pressing NEXT button goes to page one
        nextButton = ttk.Button(
            self, text="Next", command=lambda: controller.show_frame(PageOne))
        nextButton.place(x=20, y=240)

        # ask user if they want to exit the application
        self.protocol("WM_DELETE_WINDOW", self.onClosing)

    # asks user if they actually want to exit the app
    def onClosing(self):
        if messagebox.askyesno(message="Continue to quit?"):
            self.destroy()

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


# class PageOne (tk.Frame):

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.controller = controller
#         self.widgets()

#     def widgets(self):
#         # create window
#         self.master.title("page one")
#         self.geometry("500x300+450+300")
#         # set color
#         self.configure(bg='#f9f1f1')
#         # Create a style
#         style = ttk.Style(self)
#         # Set the theme with the theme_use method
#         style.theme_use('clam')

#         welcomeLabel = ttk.Label(self, text="Altering the video", font=(
#             'Times New Roman', 27))
#         welcomeLabel.place(x=20, y=20)

#         instructionLabel = ttk.Label(self, text="Would you like your video flipped horizontally or cropped vertically?", font=(
#             'Times New Roman', 15))
#         instructionLabel.place(x=20, y=80)

#         # pressing NEXT button goes to page two
#         nextButton = ttk.Button(self, text="Next", command=lambda: controller.show_frame(
#             PageTwo))
#         nextButton.place(x=20, y=240)


# class PageTwo (tk.Frame):

    # def __init__(self, parent, controller):
    #     tk.Frame.__init__(self, parent)
    #     self.controller = controller
    #     self.widgets()

    # def widgets(self):
    #     # create window
    #     self.master.title("page two")
    #     self.geometry("500x300+450+300")
    #     # set color
    #     self.configure(bg='#f9f1f1')
    #     # Create a style
    #     style = ttk.Style(self)
    #     # Set the theme with the theme_use method
    #     style.theme_use('clam')

    # # pressing Back button goes to page one
    #     nextButton = ttk.Button(
    #         self, text="Next", command=lambda: controller.show_frame(PageOne)).place(x=20, y=240)
    #     nextButton.place(x=20, y=240)


# # main method
# if __name__ == '__main__':
appROM = RollOutMethodInterface()
appROM.mainloop()
