# ChatGPT-Bot
**Integration of Google API, ChatGPT API, RaspberryPi, AIY Board (V1), and VOSK**

- **VOSK**: Used specifically for the "Wake Word".
- **Google Assistant API**: This is not a requirement for the project.

**Getting Started**:

1. **OpenAI Key**: Acquire your own OpenAI key [here](https://platform.openai.com/account/api-keys).
  
2. **Google Cloud Projects**:
    - Navigate to [Google Cloud Console](console.cloud.google.com).
    - Create your project(s) and include the required APIs.
    - Generate your API keys in JSON file format.
    
    ![Google Cloud Project](https://github.com/Trina0224/chatGPT-Bot/assets/5771864/a346fa47-ed5e-4717-ae5b-9dae86eb4404.png)

3. **Demo Video**: The demonstration is available in English, Japanese, and TW Chinese. You can view it [here](https://drive.google.com/file/d/1yaMadnF3EtJCUFp2lD_YzmloZnL1kxAr/view?usp=drive_link).

4. **Setting Up Your Python Environment**:
    Ensure you have the necessary libraries installed:
    ```bash
    pip3 install google-cloud-texttospeech  
    pip3 install --upgrade google-cloud-texttospeech  
    pip3 install google-cloud-speech  
    pip3 install openai  
    pip3 install vosk sounddevice
    ```
    - **VOSK Models**: Download the models and place them under `~/.cache/vosk`. They can also be automatically downloaded using VOSK examples.
    
    ![VOSK Models](https://github.com/Trina0224/chatGPT-Bot/assets/5771864/8a3d4b38-7f09-443a-8796-daaea8a9f852.png)

### Known Issues:

1. The program has an exit code of 999; this needs to be modified.
2. There's a need to clear the VOSK queue after a ChatGPT session.
3. Google's API for text-to-speech is slow. Alternate solutions are being considered.
4. GPIO pin initialization requires attention.

### Upcoming Enhancements:

1. Exploration of alternative Text-To-Speech (TTS) solutions.
2. Aim to eliminate the need to press the red button during the ChatGPT session.
3. Introduce a feature to email or text chat records.
4. Experiment with hardware control-related functions.

### Update:  
1. You only need Male.py or Female.py. I will remove other .py files later.
2. The VOSK queue seems cleared after a wakeword section.

### References:

- A demo code in the AIY project can be found at: `/AIY-projects-python/src/examples/voice/voice_recorder.py`.
  
- Jie Jenn's insightful videos: 
    - [Watch Video 1](https://youtu.be/ZXnPMzmrmIY)
    - [Watch Video 2](https://youtu.be/izdDHVLc_Z0)

--- 

This revised version is more structured and the grammar has been refined. Let me know if you have any further modifications in mind!

