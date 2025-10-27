import re
import pandas as pd


def preprocess_whatsapp_chat(data):
    """
    Preprocess WhatsApp chat data and extract structured information
    
    Args:
        data (str): Raw WhatsApp chat export text
    
    Returns:
        pd.DataFrame: Processed DataFrame with extracted features
    """
    # Regex pattern including Unicode thin space (\u202F) before am/pm
    # Supports multiple date formats
    patterns = [
        r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\u202F[ap]m\s-\s',  # With thin space
        r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[ap]m\s-\s',      # With regular space
        r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s',              # 24-hour format
    ]
    
    dates = []
    messages = []
    pattern_used = None
    
    # Try each pattern until one works
    for pattern in patterns:
        dates = re.findall(pattern, data)
        if dates:
            messages = re.split(pattern, data)[1:]
            pattern_used = pattern
            break
    
    # If no pattern matched, return empty DataFrame
    if not dates:
        return pd.DataFrame()
    
    # Handle possible length mismatch
    min_len = min(len(dates), len(messages))
    dates, messages = dates[:min_len], messages[:min_len]
    
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    
    # Clean up and parse date column
    df['message_date'] = df['message_date'].str.replace('\u202f', ' ')
    
    # Try different date formats
    date_formats = [
        '%d/%m/%Y, %I:%M %p - ',
        '%d/%m/%y, %I:%M %p - ',
        '%m/%d/%Y, %I:%M %p - ',
        '%m/%d/%y, %I:%M %p - ',
        '%d/%m/%Y, %H:%M - ',
        '%d/%m/%y, %H:%M - ',
    ]
    
    for fmt in date_formats:
        try:
            df['message_date'] = pd.to_datetime(df['message_date'], format=fmt, errors='coerce')
            if df['message_date'].notna().sum() > 0:
                break
        except:
            continue
    
    df.rename(columns={'message_date': 'date'}, inplace=True)
    
    # Drop rows where date parsing failed
    df = df.dropna(subset=['date'])
    
    # Extract sender and clean message
    users = []
    messages_clean = []
    
    for message in df['user_message']:
        # Split on first occurrence of colon
        entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)
        
        if len(entry) >= 3:  # User message format
            users.append(entry[1].strip())
            messages_clean.append(entry[2].strip())
        else:  # System/group notification
            users.append('group_notification')
            messages_clean.append(entry[0].strip())
    
    df['user'] = users
    df['message'] = messages_clean
    df.drop(columns=['user_message'], inplace=True)
    
    # Add time features
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    
    # Create period feature (hourly intervals)
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(f"{hour:02d}-00")
        elif hour == 0:
            period.append("00-01")
        else:
            period.append(f"{hour:02d}-{hour+1:02d}")
    
    df['period'] = period
    
    # Additional features
    df['day_of_week'] = df['date'].dt.dayofweek  # Monday=0, Sunday=6
    df['is_weekend'] = df['day_of_week'].isin([5, 6])  # Saturday and Sunday
    
    # Categorize time of day
    def get_time_category(hour):
        if 5 <= hour < 12:
            return 'Morning'
        elif 12 <= hour < 17:
            return 'Afternoon'
        elif 17 <= hour < 21:
            return 'Evening'
        else:
            return 'Night'
    
    df['time_of_day'] = df['hour'].apply(get_time_category)
    
    # Clean any remaining NaN values
    df = df.dropna()
    
    return df


def validate_chat_format(data):
    """
    Validate if the uploaded file is in correct WhatsApp format
    
    Args:
        data (str): Raw chat data
    
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    # Check if file has any content
    if not data or len(data.strip()) == 0:
        return False, "The file is empty"
    
    # Check for common WhatsApp patterns
    patterns = [
        r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}',  # Date pattern
        r':\s',  # Message separator
    ]
    
    matches = sum(1 for pattern in patterns if re.search(pattern, data))
    
    if matches < 2:
        return False, "The file doesn't appear to be a valid WhatsApp chat export"
    
    return True, ""


def get_chat_info(df):
    """
    Get basic information about the chat
    
    Args:
        df (pd.DataFrame): Processed chat DataFrame
    
    Returns:
        dict: Chat information
    """
    if df.empty:
        return {}
    
    info = {
        'total_messages': len(df),
        'total_users': len(df['user'].unique()) - (1 if 'group_notification' in df['user'].unique() else 0),
        'date_range': f"{df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}",
        'total_days': (df['date'].max() - df['date'].min()).days,
        'is_group_chat': len(df['user'].unique()) > 2
    }
    
    return info