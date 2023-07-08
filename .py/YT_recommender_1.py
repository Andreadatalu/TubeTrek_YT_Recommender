import streamlit as st
from PIL import Image
import pandas as pd
from googleapiclient.discovery import build

api_key = open("api_key_1.txt", "r").read()
youtube = build('youtube', 'v3', developerKey=api_key)

def set_background_color(color):
    hex_color = '#{}'.format(color.lstrip('#'))
    css = """
        <style>
        body {
            background-color: %s;
        }
        </style>
    """ % hex_color
    st.markdown(css, unsafe_allow_html=True)

set_background_color("#EBEBEB")  

#st.image("C:\\Users\\Andrea\\Documents\\DATA\\YT_Channel_Recommender\\.py\\Images\\TubeTrek_banner.jpg")
st.image("./Images/TubeTrek-banner.jpg")
#st.title("Channel Chaser: Discover the most captivating YouTube Channels for You")
st.markdown("<h2 style='font-size:24px;'>Channel Chaser:<br>Discover the most captivating YouTube Channels for You!</h2>", unsafe_allow_html=True)
def get_channel_ids(user_input):
    try:
        request = youtube.search().list(
            part="snippet",
            order="relevance",
            maxResults=5,
            q=user_input,
        )
        response = request.execute()

        channel_ids = []
        for item in response['items']:
            channel_id = item['snippet']['channelId']
            if channel_id not in channel_ids:
                channel_ids.append(channel_id)

        if channel_ids:
            return channel_ids
        else:
            st.write("Sorry, I can't find your topic in my recommendations. Let's try another topic :).")
            return None
    except Exception as e:
        st.write("An error occurred:", str(e))
        return None


user_input = st.text_input("Type a topic for your channel:")
channel_ids = get_channel_ids(user_input)


def get_video_ids(channel_ids):
    video_ids = []
    for channel_id in channel_ids:
        try:
            request = youtube.search().list(
                part="snippet",
                channelId=channel_id,
                maxResults=1,
                q=user_input,
                type="video"
            )
            response = request.execute()

            video_id = response['items'][0]['id']['videoId']
            video_ids.append(video_id)
        except Exception as e:
            st.write("An error occurred:", str(e))

    return video_ids


video_ids = get_video_ids(channel_ids)


def get_tags_channel(video_ids):
    database = []
    for video_id in video_ids:
        try:
            request = youtube.videos().list(
                part="snippet",
                id=video_id
            )
            response = request.execute()

            items = response['items']
            for item in items:
                video_data = [
                    item['snippet'].get('channelId'),
                    item['snippet'].get('channelTitle'),
                    item['snippet'].get('categoryId'),
                    item['snippet'].get('title'),
                    item['snippet'].get('tags'),
                    item['snippet'].get('description')
                ]

                channel_url = item['snippet'].get('channelId')

                request_1 = youtube.channels().list(
                    part="snippet",
                    id=channel_url
                )
                response_1 = request_1.execute()

                channel_data = response_1['items'][0]['snippet']
                video_data.append(channel_data.get('customUrl'))

                database.append(video_data)
        except Exception as e:
            st.write("An error occurred:", str(e))

    return database

def main():
    # Search button
    search_button = st.button("Discover your channel in one click")
    
    if search_button:
        # Perform YouTube search
        channel_ids = get_channel_ids(user_input)
        video_ids = get_video_ids(channel_ids)
        database = get_tags_channel(video_ids)
        df_channel = pd.DataFrame(database, columns=['channel_id', 'channel_title', 'category_id', 'title', 'tags', 'description', 'channel_url'])
        top_5_channels = df_channel.drop(columns=['channel_id', 'category_id', 'title', 'tags', 'description'])
        st.write("Top Channels for you:")
        st.dataframe(top_5_channels)
        video_reccomendation = df_channel.drop(columns=['channel_id', 'channel_title', 'category_id', 'tags', 'description', 'channel_url'])
        st.write("Also see some video reccomendations:")
        st.dataframe(video_reccomendation)
    if user_input:
        st.write("Please click the 'Search on YouTube' button to perform the search.")
        search_url = "https://www.youtube.com/results?search_query=" + user_input.replace(" ", "+")
        st.markdown(f"[Search on YouTube]({search_url})")
if __name__ == "__main__":
    main()

