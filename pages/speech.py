import streamlit as st
from gtts import gTTS
from PIL import Image
import speech_recognition as sr
from speech_recognition import AudioData
from textblob import TextBlob
from langdetect import detect
# import spacy_streamlit
# from spacy_cld import LanguageDetector
# gensim
# from gensim.Summarization import summarize
# summy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

# import spacy
import base64
import time

def app():
    
    model = {
        'English': 'en_core_web_sm',
        'French': 'fr_core_news_sm',
        'Portuguese': 'pt_core_news_sm',
        'Spanish': 'es_core_news_sm'
    }

    # sumy summarizer
    def sumy_summarizer(docx):
        parser = PlaintextParser.from_string(docx, Tokenizer("english"))
        lex_summarizer = LexRankSummarizer()
        summary = lex_summarizer(parser.document,3)
        summary_list = [str(sentence) for sentence in summary]
        result = ' '.join(summary_list)
        return result

    def read_audio(filename):
        audio_created = open(filename, 'rb')
        audio_bytes = audio_created.read()
        st.audio(audio_bytes, format='audio/ogg')

    # def detect_language(text):
    #     nlp = spacy.load('en_core_web_sm')
    #     language_detector = LanguageDetector()
    #     nlp.add_pipe(language_detector)
    #     docx = nlp(text)
    #     result = docx._.languages
    #     st.write()
    #     return result


    st.write("""
    # Speech to text
    Speech to text (STT) software is a type of assistive technology program that converts words that are spoken 
    aloud to electronic written text to support increased demonstration of learning and independence.

    """)

    image = Image.open('images/speech-to-text.png')
    st.image(image)

    upload = 'Upload audio'
    record = 'Record audio'
    method = [upload, record]
    option = st.radio('Speech method', method)

    if option == upload:
        # Upload speech
        fileUp = st.file_uploader("Upload your speech (WAV file)", type=["wav", "mp3"])
        
        # Reading WAV file
        if fileUp:
            name_fileUp = fileUp.name
            read_audio(name_fileUp)

        r = sr.Recognizer()

        # Text downloader
        timestr = time.strftime("%Y%m%d-%H%M%S")
        
        def text_downloader(raw_text):
            b64 = base64.b64encode(raw_text.encode()).decode()
            new_filename = "text_file_{}_.txt".format(timestr)
            # st.markdown("### Download File ###")
            href = f'<a href="data:file/txt;base64,{b64}" download = "{new_filename}"> Download text </a>'
            st.markdown(href, unsafe_allow_html=True)
        
        # def text_analyzer(text):
        #     nlp = spacy.load("en_core_web_sm")
        #     docx = nlp(text)
        #     tokens = [token.text for token in docx]
        #     allData = [('"Tokens":{},\n"Lemma":{}'.format(token.text, token.lemma_)) for token in docx]
            
        #     return allData
        
        # def entity_analyzer(text):
        #     nlp = spacy.load("en_core_web_sm")
        #     docx = nlp(text)
        #     tokens = [token.text for token in docx]
        #     entities = [(entity.text, entity.label_) for entity in docx.ents]
        #     allData = [('"Tokens":{},\n"Entities":{}'.format(token, entities)) for token in docx]

        #     return allData

        if fileUp :
            
            with sr.AudioFile(fileUp) as source:
                audio_data = r.record(source)
                textSpeech = r.recognize_google(audio_data)
                st.success(textSpeech)
                text_downloader(textSpeech)


                # Text Summarization
                if st.button("Text Summarization"):    
                    st.text("Using Sumy..")
                    summary_result = sumy_summarizer(textSpeech)

                    st.success(summary_result)

    
    elif option == record:
        from threading import Thread
        from streamlit.report_thread import add_report_ctx
        from streamlit.report_thread import get_report_ctx

        # st.set_page_config(
        #     page_title="Speech to text", 
        #     page_icon="🗣️",
        #     layout="centered", # wide
        #     initial_sidebar_state="auto") # collapsed


        language = st.selectbox('Choose language', help='Choose the language you want to speak to the mic', options = ('English', 'French'))
        if language == 'French':
            language = "fr-FR"
        else:
            language = 'en-US'

        duration = st.slider('Choose speaking duration (seconds)', min_value= 10, max_value=60, value = 10, step=10, help = 'Choose how long to record your voice')

        def text_downloader(raw_text):
            b64 = base64.b64encode(raw_text.encode()).decode()
            new_filename = "text_file_{}_.txt".format(timestr)
            # st.markdown("### Download File ###")
            href = f'<a href="data:file/txt;base64,{b64}" download = "{new_filename}"> Download text </a>'
            st.markdown(href, unsafe_allow_html=True)

        def progress_bar(duration):
            ctx = get_report_ctx()
            add_report_ctx(None, ctx)
            latest_iteration = st.empty()
            bar = st.progress(0)
            for i in range(duration+1):
                latest_iteration.text(f'{duration - i} seconds left')
                bar.progress((100//duration)*i)
                time.sleep(1)
            st.text('Analyzing your speech...')

        r = sr.Recognizer()
        if st.button('Speak', help='Once you click, speak and wait for the transcription'):
            t = Thread(target=progress_bar, args=(duration,)) # I need a thread in order to show progress bar and record simultanesouly
            add_report_ctx(t)
            t.start()
            try:
                with sr.Microphone() as source:
                    # read the audio data from the microphone
                    audio_data = r.record(source, duration=duration)
                    # convert speech to text
                    textFromSpeech = r.recognize_google(audio_data, language= language)
                    st.info(textFromSpeech)
                    if textFromSpeech:
                        text_downloader(textFromSpeech)
            except Exception as e:
                st.error('Could not process audio')

