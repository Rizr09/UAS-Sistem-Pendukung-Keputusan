import re
import pandas as pd
from math import sqrt
import streamlit as st
from Topsis import Topsis

def display_recommendation(iframe_code, percentage):
    st.markdown(f"This song matches your taste by **{percentage * 100:.3f}%**")
    st.progress(percentage)
    st.markdown(iframe_code, unsafe_allow_html=True)

def main():
    weight = [0] * 8 # create a list of 8 zeros
    impact = [0] * 8 # create a list of 8 zeros
    st.markdown("<h1 style='text-align: center; color: black;'><span style='color: #1DB954;'>Music</span> Recommendation System Using TOPSIS</h1>", unsafe_allow_html=True)
    
    # st.sidebar.markdown(ui.select("What type of song do you want to listen to?", ['English', 'Indonesian', 'Korean']))
    genre = st.sidebar.selectbox("What type of song do you want to listen to?", ['English', 'Indonesia', 'Korea'])

    st.sidebar.markdown("<h3 style='text-align: center; color: black;'>Select your <span style='text-decoration: underline; text-decoration-color: #1DB954;'>preferences</span></h3>", unsafe_allow_html=True)
    # create a list of the musical attributes and their emojis
    attributes = ["Acousticness🎻", "Danceability💃", "Energy⚡", "Instrumentalness🎼", "Liveness🎙️", "Loudness🔉", "Speechiness🗣️", "Tempo⏩"]
    # create a list of the descriptions for each attribute
    descriptions = [
        "A confidence measure whether the track is acoustic. 10 represents high confidence the track is acoustic.",
        "How suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. 10 represents high confidence the track is danceable.",
        "A perceptual measure of intensity and activity. 10 represents high confidence the track is energetic.",
        "Predicts whether a track contains no vocals. 10 represents high confidence the track contains no vocals.",
        "Detects the presence of an audience in the recording. 10 represents high confidence the track is live.",
        "The overall loudness of a track in decibels (dB). 10 represents high confidence the track is loud.",
        "Detects the presence of spoken words in a track. 10 represents high confidence the track contains no speech.",
        "The overall estimated tempo of a track in beats per minute (BPM). 10 represents high confidence the track is fast."
    ]
    # use a loop to iterate over the attributes and their descriptions
    for i in range(len(attributes)):
        # display the attribute name and emoji
        st.sidebar.markdown(f"<h4 style='color: #1DB954; font-weight: bold;'>{attributes[i]}</h4>", unsafe_allow_html=True)
        # display the attribute description and slider
        weight[i] = st.sidebar.slider(descriptions[i], -10, 10, 0)
        # determine the impact based on the weight sign
        impact[i] = 1 if weight[i] >= 0 else 0
        # take the absolute value of the weight
        weight[i] = abs(weight[i])

    if st.sidebar.button("Search") and all([i != 0 for i in weight]):
        data = pd.read_csv(f'data/{genre}.csv')
        topsis = Topsis(data, weight, impact)
        topsis.run()
        rec = topsis.getEmbed()
        percent = topsis.getPercentage()

        for i, percentage in zip(rec, percent):
            iframe_code = f'<iframe style="border-radius:12px; background-color: transparent;" src="{i}?utm_source=generator" width="100%" height="160" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>'
            display_recommendation(iframe_code, percentage)

    else:
        st.sidebar.error("Please change at least one preference!")
        st.markdown("<h4 style='text-align: center; color: black;'>↖️ You haven't searched for a song yet, head to the sidebar</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: black;'>How about recommendation of the day 👇</h4>", unsafe_allow_html=True)
        korea = pd.read_csv(f'data/Korea Trimmed.csv')
        sample = korea.iloc[[100]]
        embed = re.compile(r'https://open.spotify.com/track/(\w+)').sub(r'https://open.spotify.com/embed/track/\1', sample['trackUrl'].values[0])
        iframe_code = f'<iframe style="border-radius:12px; background-color: transparent;" src="{embed}?utm_source=generator" width="100%" height="160" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>'
        st.markdown(f"It's **{sample['trackName'].values[0]}** by **{sample['artistName'].values[0]}**")
        st.markdown(iframe_code, unsafe_allow_html=True)

if __name__ == '__main__':
    main()