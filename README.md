A very basic RASA based chatbot, integrated with RocketChat, that can assist with some of the administrative purposes like Days Off Requests, Leave Early Requests etc.

# How to install and setup rasa-startup-admin-chatbot

**Step 1: To install admin-chatbot, please clone the repo:**  
`git clone https://github.com/Gritfeat-Solutions/rasa-startup-admin-chatbot.git`  
`cd rasa-startup-admin-chatbot`  
Use the requirements.txt file to install the appropriate dependencies via pip. 

**Step 2: Install requirements:**  
`pip3 install -r requirements.txt`  

**Step 3: Install the spaCy English language model by running:**  
`python3 -m spacy download en`

This will install the bot and all of its requirements.

# How to run admin-chatbot  

1. To train the dialogue and NLU model
`rasa train`  

2. In a new terminal start the server for the custom action by running:
`rasa run actions`

3. To run the bot in terminal  
`rasa shell`  
This will start your bot in terminal and you can start chatting with it.

4. Start the duckling server by using following command. You must have docker for the command given to work.
`docker run -p 8000:8000 rasa/duckling`

5. Specify port you want to expose to public internet by using ngrok:  
To create a local webhook from your machine you can use Ngrok. Follow the instructions on their site to set it up on your computer. Move ngrok to your working directory and in a new terminal run:  
`./ngrok http 5000`

6. Set up Rocket.Chat by logging as administrator  
To set up Rocket.Chat perform the steps mentioned [here](https://rasa.com/docs/core/connectors/#rocketchat-setup).
Your url will be something like this: `https://xxxxxxx.ngrok.io/webhooks/rocketchat/webhook`. You will have to change url everytime you redo step 5.

7. Run the command below for integration    
Go to the credentials.yml file that you downloaded from the repo and input your user, password and server-url.  
`rasa run -m models -p 5002 --connector rocketchat --credentials credentials.yml`
