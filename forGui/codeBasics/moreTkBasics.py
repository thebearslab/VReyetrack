import tkinter as tk
from tkinter import messagebox

# define gui within class


class MyGui:

    # constructor calls gui
    def __init__(self):
        self.root = tk.Tk()

        # menu bar
        self.menuBar = tk.Menu(self.root)
        self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label="Close", command=self.onClosing)

        self.fileMenu.add_separator()

        self.fileMenu.add_command(label="Close Without Question", command=exit)

        self.actionMenu = tk.Menu(self.menuBar, tearoff=0)
        self.actionMenu.add_command(
            label="Show Message", command=self.show_message)

        self.actionMenu.add_command(label="Clear Message", command=self.clear)

        self.menuBar.add_cascade(menu=self.fileMenu, label="File")
        self.menuBar.add_cascade(menu=self.actionMenu, label="Action")

        self.root.config(menu=self.menuBar)

        self.label = tk.Label(self.root, text="Your message",
                              font=('Times New Roman', 18))
        self.label. pack(padx=10, pady=10)

        self.textbox = tk.Text(self.root, height=5,
                               font=('Times New Roman', 16))
        self.textbox.pack(padx=10, pady=10)

        # have command + enter trigger a function
        self.textbox.bind("<KeyPress>", self.shortCut)

        self.check_state = tk.IntVar()
        self.check = tk.Checkbutton(self.root, text="show message box", font=(
            'Times New Roman', 16), variable=self.check_state)
        self.check.pack(padx=10, pady=10)

        # passing show_message, not calling it. so now when the button is pressed the function is called
        self.button = tk.Button(self.root, text="Show Message", font=(
            "Times New Roman", 16), command=self.show_message)
        self.button.pack(padx=10, pady=10)

        self.clearButton = tk.Button(self.root, text="Clear", font=(
            "Times New Roman", 16), command=self.clear)
        self.root.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.clearButton.pack(padx=10, pady=10)

        self.root.mainloop()

    def show_message(self):
        if self.check_state.get() == 0:
            print(self.textbox.get('1.0', tk.END))
        else:
            messagebox.showinfo(
                title="message", message=self.textbox.get('1.0', tk.END))

    def shortCut(self, event):
        # will get the thingies of the keys we want (command+enter)
        # print(event.keysym)
        # print(event.state)

        if event.state == 8 and event.keysym == "Return":
            self.show_message()

    def onClosing(self):
        if messagebox.askyesno(title="Quit?", message="Do you want to exit the application?"):
            self.root.destroy()

    def clear(self):
        self.textbox.delete("1.0", tk.END)


MyGui()
