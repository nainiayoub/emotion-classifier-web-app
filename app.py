import streamlit as st
from multiapp import Multiapp
from pages import home, text, speech, emotionClassifier

app = Multiapp()

app.add_app("Home", home.app)
app.add_app("Emotion Text Classifier", emotionClassifier.app)
app.add_app("Speech to text", speech.app)
app.add_app("Translation (In progress)", text.app)



app.run()
