# _author_ = "John Oakey"
# A Basic multi-screen demo
# PRELIMINARY HOUSE KEEPING

# only one of the following SHOULD be needed but testing cross platform
# indicates to me one works on windows and the other works on Debian (Unix)
import tkinter as tk
from tkinter import *

# I think it is a good practice to explicitly open a root screen
# This example shows how to get and utilize the full screen for your root example
root = tk.Tk()
root.configure(background='beige')
root.title("Rooty Tooty Root Screen")
scrW = root.winfo_screenwidth()
scrH = root.winfo_screenheight()

root.geometry(str(scrW) + "x" + str(scrH))

# I tested - root.wm_state('zoomed') - but for some reason it prevents top2 from being created


# We will create two screens: one for an intro, one for program process or whatever
top1 = Toplevel(root, bg="light blue")
top1.geometry(str(scrW) + "x" + str(scrH))
top1.title("Top 1 Window")
top1.wm_attributes("-topmost", 1)  # make sure top1 is on top to start

top2 = Toplevel(root, bg="grey85")
# instead of - top2.geometry(str(scrW) + "x" + str(scrH)) - lets use -fullscreen
# IN TESTING both "wm_attributes" and just plain "attributes" both work
top2.attributes('-fullscreen', TRUE)
top2.title("Top 2 Window")


# A couple of widgets I would not normally employ to demo where we are as tops are destroyed.
# our RootButton will call a simple exit function
def Fini():
    exit()


# a lable and button to show we are down to the root
RootLabel = tk.Label(root, text="This is the root screen - normally I would not create widgets here",
                     font=('Arial', 16, 'bold'), takefocus=1)
RootLabel.pack(pady=25, padx=25, ipadx=10, ipady=10, anchor="nw")
# NOTE called without parens = callbacks take no parameteres
RootButton = tk.Button(text="fini", font=('Arial', 16, 'bold'), command=Fini)
RootButton.pack_configure(ipadx=10, ipady=10, padx=25, anchor="nw")

# Now we create a Toplevel "Hello" Screen as a class


class ScreenNo1:
    def __init__(self, top1):
        frame = tk.Frame(top1, width=scrW-300,
                         height=scrH-300, bg="LightCyan2")
        frame.pack(side='bottom', pady=(root.winfo_screenheight() - 300)/2)

        self.button = Button(frame, text="Close TopLevel 1", fg="maroon", font=(
            "courier", 16, "bold"), command=self.end_top1)
        self.button.grid(column=1, row=1, pady=10)

        self.greeting1 = Button(frame, text="Click Me", fg="blue",
                                command=self.write_greeting1, font=("arial", 16, "bold"))
        self.greeting1.grid(column=1, row=0,)

        self.button.configure(height=2, width=20)
        self.greeting1.configure(height=2, width=20)

        msg1 = StringVar()
        msg1.set("Welcome to Python Programming: This is screen number 1")
        self.msglabel = Label(frame, textvariable=msg1,
                              fg="black", font=("courier", 16, "bold"))

    def write_greeting1(self):
        self.msglabel.grid(column=1, row=2, pady=10)

    def end_top1(self):  # using for demo purpose instead of command=top1.destroy in button definition
        top1.destroy()

# Create a Secondary Screen for activity


class ScreenNo2:
    def __init__(self, top1):
        frame2 = tk.Frame(top2, width=scrW-300, height=scrH -
                          400, bg="LightCyan2", pady=150)
        frame2.pack(side=LEFT)

        self.button2 = Button(frame2, text="Close TopLevel 2", fg="maroon",
                              command=top2.destroy, font=("courier", 16, "bold"))
        # could close the whole shebang by using root.destroy instead of top2.destroy
        self.button2.pack(side=LEFT, padx=20)

        self.MoreMsg = Button(frame2, text="Click This Other Me", fg="blue",
                              command=self.write_message2, font=("arial", 16, "bold"))
        self.MoreMsg.pack(side=LEFT)

        self.button2.configure(height=2, width=20)
        self.MoreMsg.configure(height=2, width=20)

        self.anotherLabel = Label(frame2, text="This msg shows on the screen.", font=(
            "arial", 14, "bold"), width=32, padx=10)  # created but not packed

    def write_message2(self):
        # sent to standard out & will duplicate multiple presses- not sent to GUI
        print("You have moved on to activity on Screen Number 2")
        # GUI display, will not be duplicated with multiple presses
        self.anotherLabel.pack(anchor='nw', padx=20, side=BOTTOM)
        self.anotherLabel.configure(bg='cyan')


# here we create our class events
Myapp1 = ScreenNo1(top1)
Myapp2 = ScreenNo2(top2)

root.mainloop()
