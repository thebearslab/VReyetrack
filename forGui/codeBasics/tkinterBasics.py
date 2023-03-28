import tkinter as tk

# create window
root = tk.Tk()
root.title("Roll Out Method Gui")
root.geometry("800x500")

# add widgets
label = tk.Label(root, text="roll out method", font=('Arial', 18))
label.pack(padx=20, pady=20)

textbox = tk.Text(root, height=3, font=('Arial', 16))
textbox.pack(padx=10)

button = tk.Button(root, text='Stop', width=25, command=root.destroy)
button.pack(padx=10, pady=10)

buttonframe = tk.Frame(root)
buttonframe.columnconfigure(0, weight=1)
buttonframe.columnconfigure(1, weight=1)
buttonframe.columnconfigure(2, weight=1)

# passed to buttonframe, which is inside root
btn1 = tk.Button(buttonframe, text='button 1', font=('Arial', 18))
btn1.grid(row=0, column=0, sticky=tk.W+tk.E)

btn2 = tk.Button(buttonframe, text='button 2', font=('Arial', 18))
btn2.grid(row=0, column=1, sticky=tk.W+tk.E)

btn3 = tk.Button(buttonframe, text='button 3', font=('Arial', 18))
btn3.grid(row=0, column=2, sticky=tk.W+tk.E)

btn4 = tk.Button(buttonframe, text='button 4', font=('Arial', 18))
btn4.grid(row=1, column=0, sticky=tk.W+tk.E)

btn5 = tk.Button(buttonframe, text='button 5', font=('Arial', 18))
btn5.grid(row=1, column=1, sticky=tk.W+tk.E)

btn6 = tk.Button(buttonframe, text='button 6', font=('Arial', 18))
btn6.grid(row=1, column=2, sticky=tk.W+tk.E)

# buttons inside grid, inside buttonframe, packed inside root
buttonframe.pack(fill='x')

# can also place things inside pack layout
anotherButton = tk.Button(root, text="and another one", font=('Arial', 18))
anotherButton.place(x=200, y=200, height=100, width=100)

# call constructor/ run window
root.mainloop()
