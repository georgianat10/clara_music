from tkinter import *
from PIL import Image, ImageTk

def play_song():
    print("Redam cantecul")

def listen():
    print("Acum ascult ce zici")


def stop_song():
    print("Opresc cantecul")


def make_view(root):
    root.title("Music Recomandations ChatBot")
    root.geometry('360x150')

    root.config(background='white')

    frame_label = Frame(root)
    frame_label.pack(side=TOP)

    frame_images = Frame(root)
    frame_images.pack()

    intro = Label(frame_label, text="I'm here to make your day better with a song :)", font=("Arial Bold", 12))
    intro.config(background='white')
    intro.pack(side=TOP)

    load_redo = Image.open("D:\\An3sem2\\LFT\\Chatbot\\assets\\redo.png")
    render_redo = ImageTk.PhotoImage(load_redo)
    img_redo = Label(frame_images, image=render_redo)
    img_redo.image = render_redo
    button_redo = Button(frame_images)
    button_redo.config(image=render_redo, command=play_song)
    button_redo.grid(column=1, row=5)
    #img_redo.grid(column=1, row=5)

    load_speak = Image.open("D:\\An3sem2\\LFT\\Chatbot\\assets\\speak.png")
    render_speak = ImageTk.PhotoImage(load_speak)
    img_speak = Label(frame_images, image=render_speak)
    img_speak.image = render_speak
    button_speak = Button(frame_images)
    button_speak.config(image=render_speak, command=listen)
    button_speak.grid(column=0, row=5)

    load_stop = Image.open("D:\\An3sem2\\LFT\\Chatbot\\assets\\stop.png")
    render_stop = ImageTk.PhotoImage(load_stop)
    img_stop = Label(frame_images, image=render_stop)
    img_stop.image = render_stop
    button_stop = Button(frame_images)
    button_stop.config(image=render_stop, command=stop_song)
    button_stop.grid(column=2, row=5)


def open_interface():
    root = Tk()
    make_view(root)
    root.mainloop()

if __name__ == '__main__':
    open_interface()