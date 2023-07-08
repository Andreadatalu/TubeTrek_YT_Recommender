import streamlit as st
import pandas as pd
import re
from googleapiclient.discovery import build
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.metrics import jaccard_distance

# Load trend data file
file_path = 'C:/Users/Andrea/Documents/DATA/YT_Channel_Recommender/Database/df_trending.csv'
df_trending = pd.read_csv(file_path)
df_trending['category_id'] = df_trending['category_id'].astype('object')

# Connect my api credentials
api_key = open("api_key_1.txt", "r").read()
youtube = build('youtube', 'v3', developerKey=api_key)

# Get the video ID for user input
def get_video_id(user_input):
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=user_input
    )
    response = request.execute()

    items = response['items']
    video_ids = []
    for item in items:
        if 'id' in item and 'videoId' in item['id']:
            video_id = item['id']['videoId']
            video_ids.append(video_id)

    if len(video_ids) > 0:
        return video_ids
    else:
        st.write("Sorry, I can't find your topic in my recommendations. Let's try another topic :).")
        return None
user_input = input("Type a topic for your channel: ")
video_ids = get_video_id(user_input)

# Get channel details
def get_tags_channel(video_ids):
    request = youtube.videos().list(
        part="snippet",
        id=video_ids
    )
    response = request.execute()

    database = []

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

    return database

database = get_tags_channel(video_ids)
df_channel = pd.DataFrame(database, columns=['channel_id', 'channel_title', 'category_id', 'title', 'tags', 'description', 'custom_url'])

# Clean and process the tags
def clean_up(tag_list):
    cleaned_tags = []
    for tag in tag_list:
        tag = str(tag).lower()
        tag = re.sub("http:\S+", " ", tag)
        tag = re.findall("[a-z]+", tag)
        cleaned_tags.extend(tag)
    return ','.join(cleaned_tags)

def tokenize(tags):
    return word_tokenize(str(tags))

def lemmatize_input(tags):
    lem = WordNetLemmatizer()
    return [lem.lemmatize(word) for word in tags]

english_stopwords = stopwords.words('english')
spanish_stopwords = stopwords.words('spanish')
all_stopwords = english_stopwords + spanish_stopwords

def remove_sw_input(tags):
    return [word for word in tags if not word in all_stopwords]

def clean_tags(tags):
    tags = [tag for tag in tags if tag != ',']
    tags = list(set(tags))
    return tags

def filter_trending_df(df_trending, category):
    filtered_df_trending = df_trending[df_trending['category_id']== category].copy()
    
    if filtered_df_trending.shape[0] < 10:
        st.write("Sorry, we found just one channel. Please try again.")
        return None
    
    return filtered_df_trending

def tokenizer_and_remove_punctuation(row):
    tokens = word_tokenize(row['tags'])
    return [word.lower() for word in tokens if word.isalnum()]

def lemmatize(row):
    lem = WordNetLemmatizer()
    return [lem.lemmatize(word) for word in row['tags']]

def remove_sw(row):
    return [word for word in row['tags'] if not word in all_stopwords]

def calculate_similarity(tags1, tags2):
    set_tags1 = set(tags1)
    set_tags2 = set(tags2)
    score = 1 - jaccard_distance(set_tags1, set_tags2)
    return score

def calculate_score(row):
    tags_channel = df_channel['tags'][0]
    tags_trending = row['tags']
    score = sum(calculate_similarity(tags_channel, tags_trending) for word_trending in tags_trending)
    return score

def get_custom_url():
    channel_url = []
    for channel_id in top_3_scores['channel_id']:
        request = youtube.channels().list(
            part="snippet",
            id=channel_id
        )
        response = request.execute()
        items = response['items']
        for item in items:
            custom_url = item['snippet'].get('customUrl')
            channel_url.append(custom_url)
    return channel_url

def main():
    # Get user input
    st.header("Channel Chaser: Discover the most captivating YouTube Channels for You")
    user_input = st.text_input("Type a topic for your channel:")
    if user_input:
        video_ids = get_video_id(user_input)
        database = get_tags_channel(video_ids)
        df_channel = pd.DataFrame(database, columns=['channel_id', 'channel_title', 'category_id', 'title', 'tags', 'description', 'custom_url'])
        df_channel['tags'] = df_channel['tags'].apply(clean_up)
        df_channel['tags'] = df_channel['tags'].apply(tokenize)
        df_channel['tags'] = df_channel['tags'].apply(lemmatize_input)
        df_channel['tags'] = df_channel['tags'].apply(remove_sw_input)
        df_channel['tags'] = df_channel['tags'].apply(clean_tags)
        category = int(df_channel['category_id'].iloc[0])
        filtered_df_trending = filter_trending_df(df_trending, category)
        if filtered_df_trending is not None:
            filtered_df_trending['tags'] = filtered_df_trending.apply(tokenizer_and_remove_punctuation, axis=1)
            filtered_df_trending['tags'] = filtered_df_trending.apply(lemmatize, axis=1)
            filtered_df_trending['tags'] = filtered_df_trending.apply(remove_sw, axis=1)
            filtered_df_trending['tags'] = filtered_df_trending['tags'].apply(clean_tags)
            filtered_df_trending['score'] = filtered_df_trending.apply(calculate_score, axis=1)
            top_3_scores = filtered_df_trending.sort_values('score', ascending=False).head(3)
            channel_url = get_custom_url()
            top_3_scores['channel_url'] = channel_url
            top_3_scores = top_3_scores.drop(columns=['channel_id', 'category_id', 'title', 'tags', 'description', 'score'])
            st.write("Top Recommended Channels for you:")
            st.dataframe(top_3_scores)
        else:
            st.write("Sorry, no trendingchannels found for the selected category. Please try again with a different topic.")
    else:
        st.write("Sorry, no video found for the given topic. Please try again with a different topic.")
if __name__ == "__main__":
    main()



