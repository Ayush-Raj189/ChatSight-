from urlextract import URLExtract
extractor = URLExtract()
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
import os


def fetch_stats(selected_user, df):
    """
    Fetch statistics for messages, words, media, and links
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # Fetch the number of messages
    num_messages = df.shape[0]
    
    # Fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())
    num_words = len(words)
    
    # Fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]
    
    # Fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    num_links = len(links)
    
    return num_messages, num_words, num_media_messages, num_links


def most_busy_users(df):
    """
    Get the most busy users in the group
    """
    busy_users = df['user'].value_counts().head()
    df_percent = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index()
    df_percent.columns = ['name', 'percent']
    return busy_users, df_percent


def create_wordcloud(selected_user, df):
    """
    Create a word cloud from messages
    """
    # Load stop words
    if os.path.exists('stop_hinglish.txt'):
        with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
            stop_words = f.read().splitlines()
    else:
        stop_words = []
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # Filter out group notifications and media messages
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']
    
    def remove_stop_words(message):
        """Remove stop words from message"""
        words = []
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
        return " ".join(words)
    
    # Generate word cloud
    wc = WordCloud(
        width=800, 
        height=400, 
        min_font_size=10, 
        background_color='white',
        colormap='viridis',
        relative_scaling=0.5,
        max_words=100
    )
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    """
    Get the most common words used in messages
    """
    # Load stop words
    if os.path.exists('stop_hinglish.txt'):
        with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
            stop_words = f.read().splitlines()
    else:
        stop_words = []
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # Filter out group notifications and media messages
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']
    
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user, df):
    """
    Extract and count emojis from messages
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def monthly_timeline(selected_user, df):
    """
    Create monthly timeline of messages
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    
    timeline['time'] = time
    return timeline


def daily_timeline(selected_user, df):
    """
    Create daily timeline of messages
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline


def week_activity_map(selected_user, df):
    """
    Get activity map by day of the week
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    """
    Get activity map by month
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    """
    Create activity heatmap showing messages by day and time period
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    user_heatmap = df.pivot_table(
        index='day_name', 
        columns='period', 
        values='message', 
        aggfunc='count'
    ).fillna(0)
    
    # Reorder days of the week
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    user_heatmap = user_heatmap.reindex([day for day in day_order if day in user_heatmap.index])
    
    return user_heatmap


def get_message_length_stats(selected_user, df):
    """
    Get statistics about message lengths
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']
    
    temp['message_length'] = temp['message'].str.len()
    
    avg_length = temp['message_length'].mean()
    max_length = temp['message_length'].max()
    min_length = temp['message_length'].min()
    
    return avg_length, max_length, min_length


def get_response_time_stats(selected_user, df):
    """
    Calculate average response time between messages
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    temp = df[df['user'] != 'group_notification'].copy()
    temp = temp.sort_values('date')
    
    if len(temp) > 1:
        temp['time_diff'] = temp['date'].diff()
        avg_response_time = temp['time_diff'].mean()
        return avg_response_time
    
    return None


def get_most_active_hour(selected_user, df):
    """
    Get the most active hour of the day
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['hour'].value_counts().head(1)