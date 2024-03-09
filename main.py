import streamlit as st
import speech_recognition as sr
import os
from dotenv import load_dotenv
from deepgram import DeepgramClient, PrerecordedOptions, FileSource


def transcribe_speech_srec(language):
    st.write(language)
    # initialize recognizer class
    r = sr.Recognizer()

    # Reading with microphone as source

    with sr.Microphone() as source:
        st.info("Speak now...")

        # Listen for speech and store in audio_text variable
        audio_text = r.listen(source)

        st.info("Transcribing...")

        try:

            # using google speech recognition
            text = r.recognize_google(audio_text, language=language)

            text_file = open("Output.txt", "w")
            text_file.write(text)
            text_file.close()

            return text

        except:

            return "Sorry I did not get that click the 'Start Record' button and try again"





def voice_recorder():

    import pyaudio
    import wave

    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    seconds = 3
    audio_name = "output.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(audio_name, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()



def deepgram_transcribe(audio_name):
    load_dotenv()

    # Path to the audio file
    AUDIO_FILE = audio_name

    API_KEY = os.getenv("DG_API_KEY")

    try:
        # Creating a Deepgram client ising the API key
        deepgram = DeepgramClient(API_KEY)

        with open(AUDIO_FILE, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        # Configuring Deepgram options for audio analysis
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )

        # Calling the transcribe_file method with the text payload and options

        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

        # Printing the response

        text_2 = response.to_json(indent=4)

        return text_2

    except:
        return "Sorry I did not get that click the 'Start Record' button and try again"


def main():
    st.title("Speech Recognition app")
    program = st.selectbox('Choose a speech program', ("Deepgram", "Google Speech Recognition"))
    st.write("You selected:", program)
    lang = st.selectbox(
        'Select Your Language',
        ('ENGLISH', 'CHINESE', 'FRENCH', 'SPANISH_SPAIN', 'SPANISH_LATAM', 'KOREAN', 'JAPANESE'))
    st.write('You selected:', lang)

    if lang == "ENGLISH":
        lang = "en-US"
    elif lang == "CHINESE":
        lang = "zh-TW"
    elif lang == "FRENCH":
        lang = "fr-FR"
    elif lang == "SPANISH_SPAIN":
        lang = "es-ES"
    elif lang == "SPANISH-LATAM":
        lang = "es-US"
    elif lang == "KOREAN":
        lang = "ko-KR"
    elif lang == "JAPANESE":
        lang = "ja-JP"
    st.write("Click on the button to start speaking")

    # add a button to trigger speech recognition
    if st.button("Start Recording"):
        if program == "Google Speech Recognition":
            text = transcribe_speech_srec(lang)
            st.write("Transcription: ", text)
        elif program == "Deepgram":
            voice_recorder()
            audio_name = "output.wav"
            text_2 = deepgram_transcribe(audio_name)
            st.write("Transcription: ", text_2)


if __name__ == "__main__":
    main()
