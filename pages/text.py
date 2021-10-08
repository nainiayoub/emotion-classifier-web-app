import streamlit as st
from gtts import gTTS
from PIL import Image
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
# import spacy
# import spacy_streamlit


# To run your app: streamlit run first_app.py

# functions

def save_audio(text, lang, speed, filename):
    audio_created = gTTS(text, lang=lang, slow=speed)
    audio_created.save(filename)

    return audio_created

def read_audio(filename):
    audio_created = open(filename, 'rb')
    audio_bytes = audio_created.read()
    st.audio(audio_bytes, format='audio/ogg')

# sumy summarizer

def sumy_summarizer(docx):
    parser = PlaintextParser.from_string(docx, Tokenizer("english"))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document,3)
    summary_list = [str(sentence) for sentence in summary]
    result = ' '.join(summary_list)
    return result

def app():

    st.write("""
    # Translation (text to speech)
    There are several APIs available to convert text to speech in Python. 
    One of such APIs is the Google Text to Speech API commonly known as the gTTS API.

    Choose the language and fill in the text input to convert to speech.
    """)

    image = Image.open('images/text-to-speech.png')
    st.image(image)

    # Radion button (Language choice)

    langs = {
        'English': 'en',
        'French': 'fr',
        'Portuguese': 'pt',
        'Spanish': 'es'
    }

    # model = {
    #     'English': 'en_core_web_sm',
    #     'French': 'fr_core_news_sm',
    #     'Portuguese': 'pt_core_news_sm',
    #     'Spanish': 'es_core_news_sm'
    # }


    page_names = list(langs.keys())
    # Text to speech parameters
    slow_audio_speed = False
    filename = 'speech.mp3'
    col1, col2 = st.columns(2)

    with col1:
        # Select box
        language = st.selectbox('Speech Language', page_names)
        speech_lang = language
        language = langs[language]

    with col2:
        # Text translation
            from google_trans_new import google_translator 
            from textblob import TextBlob
            
            filename_translated = "translation.mp3"
            
            translation_lang = st.selectbox('Choose translation language', help='Choose the language you want to translate the speech to', options=page_names)
            full_lang = translation_lang
            translation_lang = langs[translation_lang]

    # Input
    text = st.text_area("Enter your text")
    # nlp = spacy.load(model[speech_lang])
    if text :
        st.success(f"{text}")
        audio_created = save_audio(text, language, slow_audio_speed, filename)
        read_audio(filename)
        
        #Translation
        if st.button(f"Translate in {full_lang}"):
            translator = google_translator()
            text_output = translator.translate(text, lang_tgt=translation_lang)
            st.success(text_output)
            save_audio(text_output, translation_lang, slow_audio_speed, filename_translated)
            read_audio(filename_translated)

        # # Tokenize
        # if st.button("Tokenize"):
        #     docx = nlp(text)
        #     spacy_streamlit.visualize_tokens(docx, attrs=['text', 'pos_', 'dep_', 'ent_type_'])

        # # NER
        # if st.button("Named Entity Recognition"):
        #     docx = nlp(text)
        #     spacy_streamlit.visualize_ner(docx, labels=nlp.get_pipe('ner').labels)

        # Text Summarization
        if st.button("Summarize"):
            st.text("Using Sumy..")
            summary_result = sumy_summarizer(text)

            st.success(summary_result)
            filename = 'summarized.wav'
            audio_created = save_audio(summary_result, language, slow_audio_speed, filename)
            read_audio(filename)

        