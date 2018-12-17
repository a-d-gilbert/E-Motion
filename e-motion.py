import io
import os
import cv2
import tkinter as tk
from google.cloud import vision
import json
import datetime

def get_and_save_image():
    cam = cv2.VideoCapture(1)
    ret, image = cam.read()
    image_name = 'image' + datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S") + '.jpg'
    cv2.imwrite(image_name, image)
    return image_name

def detect_emotion(path):
    """Detects faces in an image."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of emotions to enumaerate
    emotion_names = ['angry', 'happy', 'surprised', 'sad']

    for face in faces:
        emotion_likelihood = []
        emotion_likelihood.append(face.anger_likelihood)
        emotion_likelihood.append(face.joy_likelihood)
        emotion_likelihood.append(face.surprise_likelihood)
        emotion_likelihood.append(face.sorrow_likelihood)
        return emotion_names[emotion_likelihood.index(max(emotion_likelihood))]

def load_poem(file_path):
    with open(file_path) as f:
        poem = json.load(f)
        return poem

def insert_poem(poem_content, wdg):
    wdg.insert(tk.END, poem_content["title"] + '\n\n', tk.CENTER)
    wdg.insert(tk.END, poem_content["author"] +'\n\n', tk.CENTER)
    for line in poem_content["content"]:
        wdg.insert(tk.END, line +'\n', tk.CENTER)

#image_path = get_and_save_image()
image_path = "image18-12-09-21-06-11.jpg"
emotion = detect_emotion(image_path)
print('Emotional State Detected: {}'.format(emotion))
poem_path = emotion + '1.json'
Window = tk.Tk()
Window.title('e-motion')
Window.geometry('500x500')
poem = tk.Text(Window)
poem.tag_configure('center', justify='center')
poem.pack()
poem_content = load_poem(poem_path)
print('Poem Chosen: {} by {}'.format(poem_content['title'], poem_content['author']))
insert_poem(poem_content, poem)
poem.tag_add('center', '1.0', 'end')
poem.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
Window.mainloop()