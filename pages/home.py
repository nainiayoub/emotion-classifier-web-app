import streamlit as st
from PIL import Image

def app():
    st.markdown("""

    # NLP web application _(on going)_
    
    Natural language processing is the use of computers for processing natural language text or speech.  
    
    """)

    # image = Image.open('images/speech-text.png')
    image = Image.open('images/nlp1.png')
    st.image(image)

    st.markdown("""
    ## Find me at
    * [![alt text][1.1]][1] [Twitter](https://twitter.com/nainia_ayoub)
    * [![alt text][2.1]][2] [GitHub](https://github.com/nainiayoub)

    [1.1]: http://i.imgur.com/tXSoThF.png (twitter icon with padding)
    [2.1]: http://i.imgur.com/0o48UoR.png (github icon with padding)

    [1.2]: http://i.imgur.com/wWzX9uB.png (twitter icon without padding)
    [2.2]: http://i.imgur.com/9I6NRUm.png (github icon without padding)

    [1]: http://www.twitter.com/ayoub_nainia
    [2]: http://www.github.com/nainiayoub

    """)