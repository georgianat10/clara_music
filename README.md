# Clara Music

### Clara Music Assistant Application that aims to play a song based on your disposition that you communicated earlier.

This application has three main parts:
 1. Sentiment analysis - implemented with Recursive Neural Network (RNN) using Tensorflow;
 2. Speech recognition - implemented using google libraries;
 3. Database for song and the feeling associated with it.


## Available Scripts
### Run:
```
python main.py
```
The application will start, and if you will press on the microphone button Clara will listen what command should will be executed next (i. e. 'I want to tell you how was my day.').

## Prerequisite
1. Create a virtual environment with ```virtualenv envoronment_name```. Open command line in the environment directory and activate it with ```.\Scripts\activate```.
2. ``` pip install --upgrade tensorflow```
3. ``` pip install gTTS ``` 
4. ``` pip install SpeechRecognition```
