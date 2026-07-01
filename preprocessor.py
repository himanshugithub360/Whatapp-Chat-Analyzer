import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2},\s+\d{1,2}:\d{2}\s*[ap]m\s-\s'
    
    messages = re.split(pattern, data, flags=re.IGNORECASE)[1:]
   
    messages = [ re.sub(r'[\u2066-\u2069]', '', msg).replace('@', ' ').strip() for msg in messages]
    
    dates = re.findall(pattern, data)

    dates = [d.replace('\u202f', ' ') for d in dates]

    print("Messages:", len(messages))
    print("Dates:", len(dates))

    print(messages[:2])
    print(dates[:2])

    df = pd.DataFrame({'user_message': messages,'message_date': dates})

    # Convert to datetime
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ', errors='coerce' )

    print(df['message_date'].isna().sum())

    df['date_12hr'] = df['message_date'].dt.strftime('%d/%m/%Y, %I:%M %p').str.lower()

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []

    for msg in df['user_message']:
        if ': ' in msg:
            user, message = msg.split(': ', 1)  # Split only once
            users.append(user)
            messages.append(message)
        else:
            users.append('group_notification')
            messages.append(msg)

    df['user'] = users
    df['message'] = messages

    df.drop(columns=['user_message'], inplace=True)
    df["year"] = df['date'].dt.year
    df["month"] = df["date"].dt.month_name()
    df["day"] = df["date"].dt.day
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute

    print("Messages:", len(messages))
    print("Dates:", len(dates))
    print(df.shape)

    return df 

f = open('WhatsApp Chat with Apne Group 😎.txt','r',encoding = 'utf-8')
data = f.read()
preprocess(data)