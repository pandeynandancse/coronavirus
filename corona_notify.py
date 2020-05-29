import requests
import json
import pyttsx3
import speech_recognition as sr
import re
import threading
import time
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup as bs

a = "Jammu and Kashmir\nPunjab\nHimachal Pradesh\nHaryana\nDelhi\nRajasthan\nUttar Pradesh\nUttarakhand\nMadhya Pradesh\nChattisgarh\nGujarat\nMaharashtra\nKarnataka\nGoa\nKerala\nTamil nadu\nAndhra pradesh\nTelangana\nOrissa\nBihar\nJharkhand\nWest Bengal\nAssam\nArunach Pradesh\nSikkim\nMeghalaya\nMizoram\nNagaland\nTripura"

states = a.split("\n")
states_list = []
for state in states:
    states_list.append(state.lower())


def getData(url):
    r = urllib.request.urlopen(url)
    return r



myHtmlData = getData("https://www.mohfw.gov.in/")

soup = bs(myHtmlData, 'html.parser')
myDataStr = ""
for tr in soup.find_all('tr'):
    myDataStr += tr.get_text()
myDataStr = myDataStr[1:]
itemList = myDataStr.split("\n\n")


def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for j, v in enumerate(voices):
        if voices[j].id == 'hindi':
            break

    print(voices[j].id)
    engine.setProperty('voice', voices[j].id)
    engine.setProperty('rate', 100)
    engine.setProperty('volume', 0.9)
    engine.say(text)
    engine.runAndWait()


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Say something!")
        audio = r.listen(source, timeout=3)
        said = ""

        try:
            said = r.recognize_google(audio)
        except Exception as e:
            print("Exception:", str(e))

    return said.lower()


def main():
    print("Started Program")

    END_PHRASE = "stop"

    i = 0

    while True:
        getAudio = []
        print("Listening...")
        text = get_audio()
        getAudio.append(text)
        print(text)
        if (getAudio[0] == 'total cases'):
            total_confirmed_in_india = itemList[34].split("\n")
            total_confirmed_cases_in_india_text = total_confirmed_in_india[0]
            total_number_of_cases_in_india = total_confirmed_in_india[1]
            total_number_of_cured_in_india = itemList[35]
            total_number_of_deaths_in_india = itemList[36]

            nTex = f'I ,am ,announcing ,about  , {total_confirmed_cases_in_india_text}  , in, which, total,' \
                    f'confirmed, cases, are, {total_number_of_cases_in_india[:-1]} , cured,and, discharge' \
                    f'd, are ,{total_number_of_cured_in_india},  ' \
                    f'and, total ,deaths, till, now, are , {total_number_of_deaths_in_india} ,'
            speak(nTex)
            continue
        for item in itemList[1:35]:
            dataList = item.split("\n")
            if dataList[1].lower() in getAudio:

                nText = f'I ,am ,announcing ,about ,State , {dataList[1]}  in, which, total,confirmed,cases, are, {dataList[2]} , cured,and, discharged, are ,{dataList[3]},  ' \
                        f'and, total ,deaths, till, now, are , {dataList[4]} ,'

                speak(str(nText))
                break
            else:
                continue
        if text.find(END_PHRASE) != -1:  # stop loop
            print("Exit")
            break


main()
