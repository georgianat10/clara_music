import speech_recognition as sr
import playsound
import os
import random
from gtts import gTTS
from tkinter import *
from PIL import Image, ImageTk
import sentiment_analysis as sa
import DBConnection as db
import vlc
import pafy
import time

model = sa.load_model()
overall_feeling = 0
overall_weight = 0
ulr_song = ''
text =  None
play_song = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "lft.db")
conn = db.connection(db_path)

################################################# view #################################################

def listen():
    clara_speak('How can i help you?')
    voice_data = record_audio()
    print('U: ' + str(voice_data))
    responde(voice_data)

def stop_song():
    global play_song
    play_song = False


def make_view(root):
    global text

    root.title("Music Recommendations ChatBot")
    root.geometry('390x180')

    root.config(background='#f8f8f8')

    frame_label = Frame(root)
    frame_label.pack(side=TOP)

    frame_images = Frame(root)
    frame_images.pack()

    intro = Label(frame_label, text="     I'm here to make your day better with a song :)     ", font=("Calibri Bold", 12))
    intro.config(background='#f8f8f8')
    intro.pack(side=TOP)

    load_speak = Image.open("D:\\An3sem2\\LFT\\Chatbot\\assets\\mic1.png")
    render_speak = ImageTk.PhotoImage(load_speak)
    img_speak = Label(frame_images, image=render_speak)
    img_speak.image = render_speak
    button_speak = Button(frame_images)
    button_speak.config(image=render_speak, command=listen)
    button_speak.grid(column=1, row=5, padx=10, pady=10)

    # load_stop = Image.open(".\\LFT\\stop.png")
    # render_stop = ImageTk.PhotoImage(load_stop)
    # img_stop = Label(frame_images, image=render_stop)
    # img_stop.image = render_stop
    # button_stop = Button(frame_images)
    # button_stop.config(image=render_stop, command=stop_song)
    # button_stop.grid(column=2, row=5, padx=10, pady=10)

    frame_text = Frame(root)
    frame_text.pack()

    url_mel  = Label(frame_text, text="Song url: ", font=('Calibri', 10))
    url_mel.config(background='#f8f8f8')
    url_mel.grid(column=0, row=6)
    text = Text(frame_text, height=1, width=30, bg='white')
    text.grid(column=1, row=6)

def open_interface():
    root = Tk()
    make_view(root)
    root.mainloop()

################################################# audio asistent #################################################
r = sr.Recognizer()  # initialize recognizerw

def record_audio():
    with sr.Microphone() as sourse:
        audio = r.listen(sourse)
        voice_date = ''
        try:
            voice_date = r.recognize_google(audio, language='en-US', show_all=True)
            vd = [x["transcript"] for x in voice_date["alternative"]]
        except sr.UnknownValueError:
            clara_speak('Sorry, I did not understand')
        except sr.RequestError:
            clara_speak('Sorry, my speech service is down')
        return vd

def responde(voice_data):
    if 'I want to tell you how was my day' in voice_data:
        clara_speak('Please tell me, I am listening')
        user_feeling = record_audio()
        print('U: ' + str(user_feeling))
        update_feeling(user_feeling[0])
        clara_speak('I understand.')
    elif 'play me a song' in voice_data:
        clara_speak('this is a song that I think you would like.')
        find_song()
    elif 'I like this song' in voice_data:
        update_likes()
        clara_speak('I will remember that next time!')
    elif 'I want to add this song' in voice_data:
        clara_speak('How does this song make you feel?')
        user_feeling = record_audio()
        print('U: ' + str(user_feeling))
        add_song(user_feeling[0])
    elif 'Stop' in voice_data:
        exit()
    else:
        clara_speak('I do not know how to respond to that.')


def clara_speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 100000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print('C: ' + audio_string)
    os.remove(audio_file)


################################################# controller #################################################
def find_song():
    global overall_feeling, overall_weight, ulr_song

    sentiment = overall_feeling / overall_weight
    print(str(sentiment) + ' inainte de rotunjire')
    sentiment = round(sentiment, 1)
    if sentiment < 0.1:
        sentiment = 0.1
    elif sentiment > 1:
        sentiment =1

    print('f: ' + str(sentiment))
    songs = db.select_songs(conn, sentiment)
    song_index = random.randrange(songs.__len__())
    play_song(songs[song_index][0])
    ulr_song = songs[song_index][0]

    print('S: ' + str(songs[song_index][1]))

    overall_feeling = 0
    overall_weight = 0


def update_feeling(string):
    global overall_feeling, overall_weight

    feeling = sa.get_prediction(string, model)
    print(str(feeling) +' pentru un sentiment ')

    # weight = [2, 1.75, 1.5, 1.25, 1]
    # if feeling <= 0.1 or feeling >= 0.9:  # 0,0.1,0.9,1
    #     #     overall_weight += weight[0]
    #     #     overall_feeling += feeling * weight[0]
    #     # elif (0.1 < feeling <= 0.2) or (0.8 <= feeling < 0.9):  # 0.2,0.8
    #     #     overall_weight += weight[1]
    #     #     overall_feeling += feeling * weight[1]
    #     # elif (0.2 < feeling <= 0.3) or (0.7 <= feeling < 0.8):
    #     #     overall_weight += weight[2]
    #     #     overall_feeling += feeling * weight[2]
    #     # elif (0.3 < feeling <= 0.4) or (0.6 <= feeling < 0.7):
    #     #     overall_weight += weight[3]
    #     #     overall_feeling += feeling * weight[3]
    #     # elif (0.4 < feeling <= 0.5) or (0.5 <= feeling < 0.6):  # 0.2,0.8
    #     #     overall_weight += weight[4]
    #     #     overall_feeling += feeling * weight[4]
    overall_feeling += feeling
    overall_weight +=1

def update_likes():
    db.change_likes(conn, ulr_song)

def add_song(user_feeling):
    global text
    url = text.get("1.0", END)
    print(url)
    if url == "\n":
        clara_speak("You didn't insert a song")
    else:
        sentiment = sa.get_prediction(user_feeling, model)
        sentiment = round(float(sentiment), 1)
        print(str(sentiment))
        song = (url, sentiment, 1)
        print(song)
        db.create_song(conn, song)
        clara_speak('I added this song.')
    # print(url)

def play_song(url):
    video = pafy.new(url)
    best = video.getbest()
    play_url = best.url
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(play_url)
    media.get_mrl()
    player.set_media(media)

    player.play()
    time.sleep(20)
    player.stop()

def create_thread():
    print('aici vom crea thredul')


def main():
    open_interface()


if __name__ == '__main__':
    main()