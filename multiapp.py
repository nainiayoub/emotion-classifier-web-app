import streamlit as st
from PIL import Image

class Multiapp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        app = st.sidebar.selectbox(
            'Navigation',
            self.apps,
            format_func = lambda app: app['title'])

        

        app['function']()