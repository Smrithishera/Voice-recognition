#!/usr/bin/env python
# coding: utf-8

# In[10]:


import speech_recognition as sr
from gtts import gTTS
import playsound
import pyttsx3
import os
from PIL import Image
import requests
from io import BytesIO


# In[2]:


# Sample dataset of electronics with images from different merchants
products = {
    "laptop": {
        "amazon": {"price": 999.99, "image": "https://i.dell.com/is/image/DellContent/content/dam/ss2/product-images/dell-client-products/notebooks/g-series/g16-7630/media-gallery/black/notebook-g16-7630-nt-black-gallery-1.psd?fmt=pjpg&pscan=auto&scl=1&wid=3500&hei=2625&qlt=100,1&resMode=sharp2&size=3500,2625&chrss=full&imwidth=5000"},
        "bestbuy": {"price": 899.99, "image": "https://img-prod-cms-rt-microsoft-com.akamaized.net/cms/api/am/imageFileData/RE50BkS?ver=1b74&q=90&m=6&h=705&w=1253&b=%23FFFFFFFF&f=jpg&o=f&p=140&aim=true"},
        "walmart": {"price": 949.99, "image": "https://cdn.mos.cms.futurecdn.net/Ajc3ezCTN4FGz2vF4LpQn9.jpg"},
    },
    "smartphone": {
        "amazon": {"price": 699.99, "image": "https://media.wired.com/photos/5f401ecca25385db776c0c46/master/pass/Gear-How-to-Apple-ios-13-home-screen-iphone-xs-06032019_big_large_2x.jpg"},
        "bestbuy": {"price": 649.99, "image": "https://i5.walmartimages.com/seo/Apple-iPhone-X-64GB-Unlocked-GSM-Phone-w-Dual-12MP-Camera-Space-Gray-B-Grade-Used_15c2b968-bb85-41a4-9292-b017f78fe797.a66ebbf32b6d53b6d6eb14c47434ac04.jpeg"},
        "walmart": {"price": 679.99, "image": "https://i.pcmag.com/imagery/roundups/01WOu4NbEnv3pJ54qp7j50k-16..v1647874749.jpg"},
    },
    "tablet": {
        "amazon": {"price": 399.99, "image": "https://m.media-amazon.com/images/I/4129iYx95yL.jpg"},
        "bestbuy": {"price": 349.99, "image": "https://images-cdn.ubuy.co.id/64c6221783bbd74f26794919-lenovo-tab-m10-plus-3rd-gen-10-tablet.jpg"},
        "walmart": {"price": 359.99, "image": "https://cdn.thewirecutter.com/wp-content/media/2023/11/androidtablets-2048px-05895.jpg?auto=webp&quality=75&width=1024"},
    },
}


# In[6]:


import pygame


# In[11]:


def speak(text):
    """Convert text to speech and play it."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for a voice command and return the recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I could not understand what you said.")
            return None
        except sr.RequestError:
            speak("Could not request results; check your internet connection.")
            return None
        
def show_image(image_url):
    """Display an image from a URL."""
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img.show()


# In[12]:


def compare_prices(item):
    """Compare prices from different merchants."""
    if item in products:
        merchant_prices = {merchant: data['price'] for merchant, data in products[item].items()}
        best_deal = min(merchant_prices, key=merchant_prices.get)
        best_price = merchant_prices[best_deal]
        
        # Show the image of the best deal
        image_url = products[item][best_deal]["image"]
        show_image(image_url)
        
        speak(f"The best deal for {item} is from {best_deal} at ${best_price:.2f}.")
        return best_deal, best_price
    else:
        speak("Sorry, that item is not available.")
        return None, None

def purchase_item(item):
    """Purchase an item if it's available."""
    best_deal, best_price = compare_prices(item)
    if best_deal:
        speak(f"You have chosen to purchase {item} from {best_deal} for ${best_price:.2f}.")


# In[14]:


def main():
    speak("Welcome to the voice-activated electronics store.")
    while True:
        speak("Please say the name of the electronic product you want to purchase.")
        command = listen()
        
        if command:
            purchase_item(command)
        
        speak("Do you want to purchase another item? Say yes or no.")
        response = listen()
        
        if response and "no" in response:
            speak("Thank you for visiting. Goodbye!")
            break

if __name__ == "__main__":
    main()


# In[ ]:




