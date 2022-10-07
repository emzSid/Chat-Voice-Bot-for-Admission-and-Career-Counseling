import warnings
from gtts import gTTS
import os
from playsound import playsound
import re


warnings.filterwarnings('ignore')

"""Convert bot-responses in speech"""
def bot_speaks(bot_response):
    file = "bot.mp3"
    if bot_response is None:
        bot_response = "Ask something and click on the audio button. Then I will read my response aloud."
    elif '<' in bot_response:
        bot_response = re.sub(r'<.*?>', '', bot_response) #remove html notations in the string
    speech = gTTS(bot_response, lang= 'en', tld='ca') #convert text to speech
    speech.save(file)
    playsound(file)
    os.remove(file)