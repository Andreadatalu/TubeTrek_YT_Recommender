# YouTube Channel Recommender: TubeTrek.

TubeTrek is the name of my recommender for portfolio purposes. 


## Overview

The main objective of this project is to train the skills of NLP cleaning techniques, filtering between two dataframes with different shapes,
use of APIs and the understanding of obtaining data by web scraping.
TubeTrek is based on the YouTube API connection, with the premise that YouTube is a massive source of information and you can search almost any keyword.
and it will give you a list of videos from multiple channels, or even the same channel. Sometimes, it can feel overwhelming or boring to filter.
the results with the information that you are really looking for.

Here is where TubeTrek comes alive; It recommends trending channels aligned with your keywords, and the result is tailored recommendations based on your interests.

## Project structure:

- **Database**
  In this folder, you can find several .csv files, which I describe following:
    - df_big: This is the compilation of many datasets in english and spanish from the collecting data of Mitchell J by Kaggle (Thanks!)
    - df_top: Trending dataset created by myself using the YouTube v3 api.
    - df_trending: The final trending dataset used in the project.
 
- **Resources**
  Here you can find valuable information about how the channel recommender is planning to work and the catagpry ID of teh YouTube channels to understand the meaning of each category.

- **Jupyter notebooks**
    - YT_Channel_Recommender_Funcions: You can read about how I created each function, the reason for each connection, and the data cleaning process here.
    - YT_channel_recommender_final_code: The functions that will be used to carry out the complete channel recommendation procedure are collected in this notebook.
    - YT_Channel_Recommender_Funcion_New_way: Here, you may find a suggestion option that basically makes use of the API rather than a database.
 
- **.py**
    - YT_C_R_andrea: An adaptation of the entire code that takes into account using the database to build the interface for streamlit.
    - YT_recommender_1: An adaptation of the entire code that does not take into account using a database to make an interface for streamlit.
 
## How does TubeTrek* work?
The user provides an input when selected keywords from a topic which our recommendation is pick between 3 and 5 words. Using the YouTube v3 API, it tracks the most relevant channels and compares them with the database. It provides up to five options that closely match your search, offering tailored recommendations based on the user's interests.

## Data analysis skills applied:
  - Apis management.
  - Creation of Dataframes with web scraping.
  - Natural language processing (NLP) cleaning techniques.
  - Word similarity (Jaccard distance).
  - Dataset filtering.
  - Streamlit - an open-source Python library for custom web apps for machine learning and data science.
    
**To learn more, I encourage you to go on the following link to the project presentation:** https://bit.ly/TubeTrek_project_Andrea_Luna

## Contributes and support

I hope you enjoy this project like I did, and put these skills into practice. My name is Andrea Luna, and I appreciate you choosing to learn with me. Please get in touch with me if you have any queries, remarks, or ideas. You are also welcome to play around with the data to gain further insights.

Join my network on LinkedIn: andrea-luna/ or https://www.linkedin.com/in/andrea-luna-/





