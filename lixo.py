import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

width, height = 500, 500

def get_position(event):
  root.clipboard_clear()
  coordinates = f"({event.x}, {event.y})"
  root.clipboard_append(coordinates)

  print("copiado para o clipboard: " + coordinates)
  
def select_resolution(event):
  if event.get() == '500x500':
    width, height = 500, 500

  if event.get() == '100x100':
    width, height = 100, 100

  if event.get() == '20x20':
    width, height = 20, 20

root = tk.Tk()

canvas_frame = tk.Frame(root, padx=16, pady=16) 
canvas_frame.grid(column=1)

img = Image.open("gopher.png")
img = img.resize((500, 500))
img = ImageTk.PhotoImage(img)

label = tk.Label(canvas_frame, image = img)
label.bind('<Button-1>', get_position)
label.pack()

input_frame = tk.Frame(root, padx=16, pady=16)
input_frame.grid(row=0)

tk.Label(input_frame, text='entrada').grid()

parametersInput = tk.Entry(input_frame)
parametersInput.grid(row=0, column=1)

drawing_option = tk.StringVar()
drawing_option_input = ttk.Combobox(input_frame, textvariable=drawing_option)

drawing_option_input['values'] = ('linha', 'poligono', 'curva')

drawing_option_input.grid(row=2, columnspan=2)

resolution_option = tk.StringVar()
resolution_option_input = ttk.Combobox(input_frame, textvariable=resolution_option)

resolution_option_input['values'] = ('500x500', '100x100', '20x20')

resolution_option_input.bind('<<ComboboxSelected>>', select_resolution)

resolution_option_input.grid(row=2, columnspan=2)

root.mainloop()
