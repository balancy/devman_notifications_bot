# Devman notifications telegram bot

App performing long-polling to Devman API with the aim of receiving notifications 
if solutions of devman tasks were returned or passed by a tutor. If so, the status 
message sent to telegram bot. Bot also sends logs.

Link to [bot](https://t.me/dvmn_first_bot) 

## Install

Python3 and Git should be already installed. 

1. Clone the repository by command:
```console
git clone https://github.com/balancy/devman_notifications_bot.git
```

2. Go inside cloned repository and create virtual environment by command:
```console
python -m venv env
```

3. Activate virtual environment. For linux-based OS:
```console
source env/bin/activate
```
&nbsp;&nbsp;&nbsp;
For Windows:
```console
env\scripts\activate
```

4. Install requirements by command:
```console
pip install -r requirements.txt
```

5. Rename `.env.example` to `.env` and define your proper values for environmental variables:

- `DVMN_API_TOKEN` - devman.org API token
- `BOT_TOKEN` - telegram bot token
- `CHAT_ID` - telegram user's chat id

## Launch

Run app by command:
```console
python3 main.py
```

## Deploy on heroku

You need to have an account on heroku.

1. Create an app on heroku and connect it to the [github repository](https://github.com/balancy/devman_notifications_bot.git) 

2. In the settings tab you need to define environmental variables:

- `DVMN_API_TOKEN` - devman.org API token
- `BOT_TOKEN` - telegram bot token
- `CHAT_ID` - telegram user's chat id
   

## Project goals

Code is written for study purpose.