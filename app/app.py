import streamlit as st
import altair as alt
# EDA packages
import pandas as pd
import numpy as np
# utils
import joblib

pipe_lr = joblib.load(open("models/emotion_classifier_pipe_lr_16_june_2021.pkl", "rb"))

def predict_emotion(text):
    result = pipe_lr.predict([text])

    return result[0]

def get_prediction_proba(text):
    result = pipe_lr.predict_proba([text])

    return result

emotions_emoji_dict = {"anger":"😠","disgust":"🤮", "fear":"😨😱", "happy":"🤗", "joy":"😂", "neutral":"😐", "sad":"😔", "sadness":"😔", "shame":"😳", "surprise":"😮"}

def main():
    st.markdown("""
    # Emotion text classification app
    
    According to the discrete basic emotion description approach, emotions can be classified into six basic emotions: sadness, joy, surprise, anger, disgust, and fear (van den Broek, 2013)
    """)
    menu = ["Home", "Monitor", "About"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    # HOME
    if choice == "Home":

        with st.form(key='emotion_clf_form'):
            text = st.text_area("Type here")
            submit = st.form_submit_button(label='Submit')
        
        if submit:
            st.write(f"{text}")
            col1, col2 = st.beta_columns(2)
            # output prediction and proba
            prediction = predict_emotion(text)
            probability = get_prediction_proba(text)
            
            with col1:   
            # st.write(text)
                emoji_icon = emotions_emoji_dict[prediction]
                st.success(f"Emotion Predicted : {prediction.upper()} {emoji_icon}")
            
            with col2:
                st.success(f"Confidence: {np.max(probability) * 100}%")

            # with col2:
            st.markdown("""### Prediction Probability""")
            proba_df = pd.DataFrame(probability, columns=pipe_lr.classes_)
            st.write(proba_df)
            # st.write(proba_df.T)

            # plotting probability
            proba_df_clean = proba_df.T.reset_index()
            proba_df_clean.columns = ["emotions", "probability"]

            fig = alt.Chart(proba_df_clean).mark_bar().encode(x='emotions', y='probability', color='emotions')
            st.altair_chart(fig, use_container_width=True)


    elif choice == "Monitor":
        st.subheader("Monitor app")
            


if __name__ == '__main__':
	main()