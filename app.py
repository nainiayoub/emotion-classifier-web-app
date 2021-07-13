import streamlit as st
from multiapp import Multiapp
from pages import home, emotionClassifier

app = Multiapp()

app.add_app("Home", home.app)
app.add_app("Emotion Text Classifier", emotionClassifier.app)

app.run()
