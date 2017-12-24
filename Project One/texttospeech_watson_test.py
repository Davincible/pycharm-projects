# coding=utf-8
from __future__ import print_function
import json
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1

text_to_speech = TextToSpeechV1(
    username='12d55633-734a-45c5-9ade-064e14aafea8',
    password='uQBJuQIYkNrE',
    x_watson_learning_opt_out=True)  # Optional flag

print(json.dumps(text_to_speech.voices(), indent=2))


input_one = "Hello world! this is some sample text to test out the capabilities of this service"
input_two = "Sint en piet zaten te bedenken, wat ze piotr dit jaar nou weer zouden schenken..."

voice_one = "en-US_MichaelVoice"
voice_two = "en-US_AllisonVoice"
voice_three = "en-GB_KateVoice"
voice_four = "en-US_LisaVoice"
voice_five = "es-US_SofiaVoice"

game_voice = voice_three
one = "Hey, Okay so we’ve heard that we need to help you to retrieve some package. We don’t know what the package contains, but you probably know what I’m talking about. I am not in the position to disclose my real name to you, but you can call me Darlene. We are an organization affiliated with Anonymous, we are only here to help you with the technical process. The rest you can figure out yourself. In these couple of audio files, I will explain exactly what you will need to do to retrieve the package. Listen carefully to the instructions I will give you, and do not take any uncalibrated actions. If any of the instructions went to quickly, feel free to replay the audio file, but hurry up. For safety reasons we encrypted the download-link for the modified app and these instructions with some binary. But it seems like you’ve de-crypted that already, otherwise you wouldn’t be listening to me right now. We don’t have a lot of time, so we must complete this mission in a timely manner. Now for obvious reasons you first need to install the app we provided you with. If you haven’t already, download the APK file from the link you got these instructions from, and install the file. I don’t think I will have to explain how, you are smart enough to figure that out yourself. Once you have installed the android app, open it up. Now that looks pretty neat right? Those developers in Spain have done a great job creating this app. Our team in China only implemented some hacking tools to help you with this mission. Once you’re all set up and think you are ready for the next step, just play the next audio file. Disclosure: these instructions are only intended for a game, and have no real-world applications."
two = "So now you have the login screen in front of you right? We need to get a valid username and password to be able to access the application. In order to acquire these credentials, we will have to hack their database. To do that, our Chinese hackers have build in a tool to help you with that process. We can use the terminal they embedded to access the scripts they wrote. To access the terminal, just type “root” in the username textbox, and press enter. A dialog should popup with a terminal. This will be your workplace for the next few minutes. From here we will brute force our way into their database to query for a pair of valid credentials. Go to the next step once you’ve found your way into the terminal. If at any point you accidently close the terminal, just fill in root again. Disclosure: these instructions are only intended for a game, and no real-world applications."
three = "Now in the terminal, we need some commands to execute. Again, for safety, we have encrypted the commands. The download-link for the commands is encrypted in morse code. You will need to decrypt this with the cheat sheet we provided you with. We shipped the morse code with this APK, to play it just execute the command “morse” in the terminal, and it should start playing. If you didn’t get it the first time, just play it again. Here we made use of the same URL shortener as in the binary code. So just go to that website slash the word the morse code contains. Be sure to add an underscore. The link without underscore was already occupied. Proceed to the next set of instructions once you have downloaded the file. Disclosure: these instructions are only intended for a game, and no real-world applications."
four = "Okay, the file you just downloaded is in JSON format. Inside this file you will find some information. The right commands are among them. You need to figure out a way to open this specific file type, just look for an app in the Playstore or something, I’m sure you will figure it out. Anyway, the commands are numbered. However, they are not numbered in chronological order! You can try to execute the commands, but most of them will return an error. Only one of them will work the first time. When I want you to execute commands, I will call them by their respective numbers. Always make sure to type in the commands exactly like they are given to you. They are capital sensitive. If you only make one typo they will not execute properly. Once you have figured out a way to open the file, go on to the next audio file. There I will tell you which command you will have to execute first. Disclosure: these instructions are only intended for a game, and no real-world applications."
five = "Now let’s get down to business. You can try to execute command number one or number two, but you will see that it they will throw back an error. So first we need to unlock the system. We will do this by cracking the circuit. Execute command number three now. Listen to the next set of instructions once you are done with command number three. Let’s go. Disclosure: these instructions are only intended for a game, and no real-world applications."
six = "Well that was fun, right? By cracking this circuit you’ve made sure we can execute the next command. Now we will get down to hacking the actual database. Before we can hack it, we need to establish a connection. We will do this with command number one. You will need to execute that one now. Disclosure: these instructions are only intended for a game, and no real-world applications."
seven = "Now that we have a connection to their database, we can query the database for the information we need. Which is just a fancy way of saying that we will ask the database to send back the information we want to see. Normally a database is secure and protected, but we just took down their firewall. We will ask the database to send us back the password for the user hoofdpiet, such a weird word. I’m having trouble pronouncing it. But I hope you know what I mean. If not, it is in the last part of the next command. This will be the last command, after that you should be able to access the dashboard. Now go execute command number two. Get back to me once the script has finished. Disclosure: these instructions are only intended for a game, and no real-world applications. "
eight = "Cool. Almost done. If you take a look at the output of the script you will see that it printed out some information about the user. His password should also be in there. Write his credentials down, or memorize them if you’re feeling heroic. Then you can exit out of the terminal by typing exit. You now should be with the login screen again. Here you can just fill in the username and password you just hacked. I was told the rest of the process is straight forward. Now my job is done here. Was good assisting you Sir. Good luck and peace out. Disclosure: these instructions are only intended for a game, and no real-world applications."

game_text = {'one': one, 'two': two, 'three': three, 'four': four,
             'five': five, 'six': six, 'seven': seven, 'eight': eight}
# for item, text in game_text.items():
#     with open(join(dirname(__file__), 'tts_examples/{}.wav'.format(item)),
#               'wb') as audio_file:
#         audio_file.write(
#             text_to_speech.synthesize(text, accept='audio/wav',
#                                       voice=game_voice))
#     print("Finished", item)
item = 'three'
text = game_text[item]
with open(join(dirname(__file__), 'tts_examples/03.wav'.format(item)),
          'wb') as audio_file:
    audio_file.write(
        text_to_speech.synthesize(text, accept='audio/wav',
                                  voice=game_voice))
print("Finished", item)

# en-US_MichaelVoice
# en-US_AllisonVoice
# en-GB_KateVoice
# en-US_LisaVoice
# es-US_SofiaVoice

print(json.dumps(text_to_speech.pronunciation(
        'Watson', pronunciation_format='spr'), indent=2))

# print(json.dumps(text_to_speech.customizations(), indent=2))

# print(json.dumps(text_to_speech.create_customization('test-customization'),
#  indent=2))

# print(text_to_speech.update_customization('YOUR CUSTOMIZATION ID',
# name='new name'))

# print(json.dumps(text_to_speech.get_customization('YOUR CUSTOMIZATION ID'),
#  indent=2))

# print(json.dumps(text_to_speech.get_customization_words('YOUR CUSTOMIZATION
#  ID'), indent=2))

# print(text_to_speech.add_customization_words('YOUR CUSTOMIZATION ID',
#                                              [{'word': 'resume',
# 'translation': 'rɛzʊmeɪ'}]))

# print(text_to_speech.set_customization_word('YOUR CUSTOMIZATION ID',
# word='resume',
#                                             translation='rɛzʊmeɪ'))

# print(json.dumps(text_to_speech.get_customization_word('YOUR CUSTOMIZATION
# ID', 'resume'), indent=2))

# print(text_to_speech.delete_customization_word('YOUR CUSTOMIZATION ID',
# 'resume'))

# print(text_to_speech.delete_customization('YOUR CUSTOMIZATION ID'))