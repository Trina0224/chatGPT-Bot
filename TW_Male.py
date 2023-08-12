import os
from google.cloud import texttospeech_v1
import io
import time
import threading
from google.oauth2 import service_account
from google.cloud import speech
from aiy.board import Board,Led
from aiy.voice.audio import AudioFormat, play_wav, record_file, Recorder
import os
import openai
import pygame

def check_button_press():
    with Board() as board:
        #board.led.state = Led.ON
        while True:
            board.button.wait_for_press()
            pygame.mixer.music.stop()
            #board.led.state = Led.OFF


def text_to_speech(input_text, output_filename="output.mp3"):
    #https://cloud.google.com/text-to-speech
    # Assuming the credentials file is in the same directory
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = " Your text2speech json file.json"

    # Instantiates a client
    client = texttospeech_v1.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech_v1.SynthesisInput(text=input_text)

    # Voice parameters
    voice = texttospeech_v1.VoiceSelectionParams(
        language_code="cmn-TW", 
        #language_code="en-US", 

        name="cmn-TW-Wavenet-C", #male
        #name="cmn-TW-Wavenet-A", #female
        #name="en-US-Neural2-A", #male
        #name="en-US-Neural2-C", #female

    )

    # Audio format
    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding=texttospeech_v1.AudioEncoding.MP3,
        speaking_rate=1.3,
        #pitch=0
    )

    # Make the API call
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Save the response to an output file
    with open(output_filename, 'wb') as out:
        out.write(response.audio_content)

    return output_filename

def play_mp3(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    # Start the button monitoring thread right after
    button_thread = threading.Thread(target=check_button_press)
    button_thread.start()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)









def recognize_audio(filename):
    with io.open(filename, 'rb') as f:
        content = f.read()
        audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        audio_channel_count=2,
        sample_rate_hertz=44100,
        language_code='zh-TW'
    )
    response = client.recognize(config=config, audio=audio)
    os.remove(filename)
    if response.results:
        return response.results[0].alternatives[0].transcript
    return ""

def record_and_recognize():
    filename = 'recording.wav'
    with Board() as board:
        print('Press button to start recording.')
        board.led.state = Led.ON
        board.button.wait_for_press()

        done = threading.Event()
        board.button.when_pressed = done.set

        def wait():
            start = time.monotonic()
            while not done.is_set():
                duration = time.monotonic() - start
                print('Recording: %.02f seconds [Press button to stop]' % duration)
                time.sleep(0.5)

        record_file(AudioFormat.CD, filename=filename, wait=wait, filetype='wav')
        board.led.state = Led.OFF
        print('Sending audio for recognition...')
        recognized_text = recognize_audio(filename)
        return recognized_text




# Google Cloud Speech-to-Text client setup
client_file = 'Your speech2text json file.json'
credentials = service_account.Credentials.from_service_account_file(client_file)
client = speech.SpeechClient(credentials=credentials)

API_KEY = 'Your own openai key'
openai.api_key = API_KEY

#messages = [ {"role": "system", "content": 
 #             "You are a intelligent assistant."} ]

#model_id = 'gpt-4'
model_id = 'gpt-3.5-turbo'

def chatgpt_conversation(conversation_log):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation_log
    )

    conversation_log.append({
        'role': response.choices[0].message.role, 
        'content': response.choices[0].message.content.strip()
    })
    return conversation_log

conversations = []
# role: system, user, assistant
conversations.append({'role': 'system', 'content': 'You are a intelligent assistant.'})
conversations = chatgpt_conversation(conversations)

print('{0}: {1}\n'.format(conversations[-1]['role'].strip(), conversations[-1]['content'].strip()))
#filename = text_to_speech('{0}: {1}'.format(conversations[-1]['role'].strip(), conversations[-1]['content'].strip()))
#print(f"Audio saved to: {filename}")
play_mp3("greeting_TW_M.mp3") #You could create your own greeting MP3 files. Here is only an example.


while True:
    prompt = record_and_recognize()
    conversations.append({'role': 'user', 'content': prompt})
    conversations = chatgpt_conversation(conversations)
    print()
    print('{0}: {1}\n'.format(conversations[-1]['role'].strip(), conversations[-1]['content'].strip()))
    #print(conversations[-1]['content'].strip())

    filename = text_to_speech(conversations[-1]['content'].strip())
    print(f"Audio saved to: {filename}")
    #with Board() as board:
    #    board.led.state = Led.ON
    play_mp3(filename)
