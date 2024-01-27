from urlextract import URLExtract
extract = URLExtract()

from wordcloud import WordCloud

import pandas as pd
from collections import Counter

import emoji

def fetch_stats(selected_user,df):

    if selected_user != 'overall':
        df = df[df['users'] == selected_user]

    # 1 fetch no. of message
    num_messages = df.shape[0]

    # 2 fetch no. of words
    words = []
    for message in df['messages']:
        words.extend(message.split())

    #3 fetch no. of media messages shared
    num_media_messages = df[df['messages'] == '<Media omitted>\n'].shape[0]

    #4 fetch no. of link shared
    links=[]
    for message in df['messages']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    x = df['users'].value_counts().head()
    df = round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','users':'percent'})
    return x,df             #mujhe bar k side m dataframe b chahiye


def create_wordcloud(selected_user,df):

    file = open('stop_hinglish.txt', 'r')
    stop_words = file.read()

    if selected_user != 'overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group_notification']  # maine group notification wale liye hi nhi
    temp = temp[temp['messages'] != '<Media omitted>\n']  # media omitted from messages

    def remove_stop_words(message):
        words = []
        for message in temp['messages']:
            for word in message.lower().split():
                if word not in stop_words:
                    words.append(word)
        return " ".join(words)

    wc = WordCloud(width = 500, height = 500, min_font_size = 10, background_color = 'white')
    temp['messages'] = temp['messages'].apply(remove_stop_words)
    df_wc = wc.generate(temp['messages'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):

    file = open('stop_hinglish.txt','r')
    stop_words = file.read()

    if selected_user != 'overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group_notification']  # maine group notification wale liye hi nhi
    temp = temp[temp['messages'] != '<Media omitted>\n']  # media omitted from messages

    words = []
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

            #i don't have stop words text document. so copy this file and paste in pycharm pythonproject

    most_common_df = pd.DataFrame(Counter(words).most_common(25))
    return most_common_df


def emoji_helper(selected_user,df):

    if selected_user != 'overall':
        df = df[df['users'] == selected_user]

    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


def monthly_timeline(selected_user,df):

    if selected_user != 'overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline (selected_user,df):

    if selected_user != 'overall':
        df = df[df['users'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'overall':
        df = df[df['users'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user,df):
    if selected_user != 'overall':
        df = df[df['users'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)

    return user_heatmap


