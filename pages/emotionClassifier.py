import streamlit as st
import altair as alt
# EDA packages
import pandas as pd
import numpy as np
# utils
import joblib
from datetime import datetime
import base64

pipe_lr = joblib.load(open("models/emotion_classifier_pipe_lr_16_june_2021.pkl", "rb"))

def predict_emotion(text):
    result = pipe_lr.predict([text])

    return result[0]

def get_prediction_proba(text):
    result = pipe_lr.predict_proba([text])

    return result


st.session_state.texts = []
st.session_state.predictions = []
st.session_state.probas = []
st.session_state.date = []

def app():
    
    emotions_emoji_dict = {"anger":"😠","disgust":"🤮", "fear":"😨😱", "happy":"🤗", "joy":"😂", "neutral":"😐", "sad":"😔", "sadness":"😔", "shame":"😳", "surprise":"😮"}

    st.markdown("""
    # Emotion text classification
    
    According to the discrete basic emotion description approach, emotions can be classified into six basic emotions: sadness, joy, surprise, anger, disgust, and fear _(van den Broek, 2013)_
    """)

    with st.form(key='emotion_clf_form'):
        text = st.text_area("Type here")
        submit = st.form_submit_button(label='Classify text emotion')
    
    if submit:
        

        if text:
            st.write(f"{text}")
            col1, col2 = st.columns(2)
            # output prediction and proba
            prediction = predict_emotion(text)
            datePrediction = datetime.now()
            probability = get_prediction_proba(text)

            with col1:   
            # st.write(text)
                emoji_icon = emotions_emoji_dict[prediction]
                st.success(f"Emotion Predicted : {prediction.upper()} {emoji_icon}")
            
            with col2:
                st.success(f"Confidence: {np.max(probability) * 100}%")

            # with col2:
            st.markdown("""### Classification Probability""")
            proba_df = pd.DataFrame(probability, columns=pipe_lr.classes_)
            st.write(proba_df)
            # st.write(proba_df.T)

            # plotting probability
            proba_df_clean = proba_df.T.reset_index()
            proba_df_clean.columns = ["emotions", "probability"]

            fig = alt.Chart(proba_df_clean).mark_bar().encode(x='emotions', y='probability', color='emotions')
            st.altair_chart(fig, use_container_width=True)
            ###### Global View ######

            if 'texts' and 'probas' and 'predictions' and 'date' not in st.session_state:
                st.session_state.texts = []
                st.session_state.predictions = []
                st.session_state.probas = []
                st.session_state.date = []

            st.markdown("""### Collecting inputs and classifications""")
            # store text
            # st.write("User input")
            st.session_state.texts.append(text)
            # st.write(st.session_state.texts)

            #store predictions
            # st.write("Classified emotions")
            st.session_state.predictions.append(prediction.upper())
            # st.write(st.session_state.predictions)

            #store probabilities
            st.session_state.probas.append(np.max(probability) * 100)

            # store date
            st.session_state.date.append(datePrediction)

            prdcts = st.session_state.predictions
            txts = st.session_state.texts
            probas = st.session_state.probas
            dateUser = st.session_state.date


            def get_table_download_link(df):
                """Generates a link allowing the data in a given panda dataframe to be downloaded
                in:  dataframe
                out: href string
                """
                csv = df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
                href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
                st.markdown(href, unsafe_allow_html=True)

            if 'emotions' and 'occurence' not in st.session_state:
                st.session_state.emotions = ["ANGER", "DISGUST", "FEAR", "JOY", "NEUTRAL", "SADNESS", "SHAME", "SURPRISE"]
                st.session_state.occurence = [0, 0, 0, 0, 0, 0, 0, 0]
            

            # Create data frame
            if prdcts and txts and probas:
                st.write("Data Frame")
                d = {'Text': txts, 'Emotion': prdcts, 'Probability': probas, 'Date': dateUser}
                df = pd.DataFrame(d)
                st.write(df)
                get_table_download_link(df)

                ## emotions occurences
                
                index_emotion = st.session_state.emotions.index(prediction.upper())
                st.session_state.occurence[index_emotion] += 1

                d_pie = {'Emotion': st.session_state.emotions, 'Occurence': st.session_state.occurence}
                df_pie = pd.DataFrame(d_pie)
                # st.write("Emotion Occurence")
                # st.write(df_pie)


                # df_occur = {'Emotion': prdcts, 'Occurence': occur['Emotion']}
                # st.write(df_occur)

                

                # Line chart
                # c = alt.Chart(df).mark_line().encode(x='Date',y='Probability')
                # st.altair_chart(c)

                

                col3, col4 = st.columns(2)
                with col3:
                    st.write("Emotion Occurence")
                    st.write(df_pie)
                with col4:
                    chart = alt.Chart(df).mark_line().encode(
                        x=alt.X('Date'),
                        y=alt.Y('Probability'),
                        color=alt.Color("Emotion")
                    ).properties(title="Emotions evolution by time")
                    st.altair_chart(chart, use_container_width=True)

                # Pie chart
                import plotly.express as px
                st.write("Probabily of total predicted emotions")
                fig = px.pie(df_pie, values='Occurence', names='Emotion')
                st.write(fig)

        else:
            st.write("No text has been submitted!")
            
        
            