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
    weight = [0] * 9
    impact = [0] * 9
    st.markdown("<h1 style='text-align: center; color: black;'><span style='color: #1DB954;'>Music</span> Recommendation System Using TOPSIS</h1>", unsafe_allow_html=True)    
    genre = st.sidebar.selectbox("What type of song do you want to listen to?", ['English', 'Indonesia', 'Japan', 'Korea'])

    st.sidebar.markdown("<h3 style='text-align: center; color: black;'>Select your <span style='text-decoration: underline; text-decoration-color: #1DB954;'>preferences</span></h3>", unsafe_allow_html=True)
    attributes = ["Acousticness🎻", "Danceability💃", "Energy⚡", "Instrumentalness🎼", "Liveness🎙️", "Loudness🔉", "Speechiness🗣️", "Tempo⏩", "Valence😊"]
    descriptions = [
        "A confidence measure whether the track is acoustic. 10 represents high confidence the track is acoustic.",
        "How suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. 10 represents high confidence the track is danceable.",
        "A perceptual measure of intensity and activity. 10 represents high confidence the track is energetic.",
        "Predicts whether a track contains no vocals. 10 represents high confidence the track contains no vocals.",
        "Detects the presence of an audience in the recording. 10 represents high confidence the track is live.",
        "The overall loudness of a track in decibels (dB). 10 represents high confidence the track is loud.",
        "Detects the presence of spoken words in a track. 10 represents high confidence the track contains no speech.",
        "The overall estimated tempo of a track in beats per minute (BPM). 10 represents high confidence the track is fast.",
        "Describing the musical positiveness conveyed by a track. 10 represents high confidence the track is positive."
    ]

    for i in range(len(attributes)):
        st.sidebar.markdown(f"<h4 style='color: #1DB954; font-weight: bold;'>{attributes[i]}</h4>", unsafe_allow_html=True)
        weight[i] = st.sidebar.slider(descriptions[i], -10, 10, 0)
        impact[i] = 1 if weight[i] >= 0 else 0
        weight[i] = abs(weight[i])

    if st.sidebar.button("Search") and weight != [0] * 9:
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
        st.markdown("02:01")
        korea = pd.read_csv(f'data/Korea Trimmed.csv')
        sample = korea.iloc[[100]]
        embed = re.compile(r'https://open.spotify.com/track/(\w+)').sub(r'https://open.spotify.com/embed/track/\1', sample['trackUrl'].values[0])
        # iframe_code = f'<iframe style="border-radius:12px; background-color: transparent;" src="{embed}?utm_source=generator" width="100%" height="160" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>'
        # st.markdown(f"It's **{sample['trackName'].values[0]}** by **{sample['artistName'].values[0]}**")
        iframe_code = f'<iframe style="border-radius:12px" src="https://open.spotify.com/embed/track/00Coyxt9mTec1acC52qtWa?utm_source=generator" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>'
        st.markdown(iframe_code, unsafe_allow_html=True)

if __name__ == '__main__':
    main()