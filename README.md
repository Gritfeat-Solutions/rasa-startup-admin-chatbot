A very basic RASA based chatbot, integrated with RocketChat, that can assist with some of the administrative purposes like Days Off Requests, Leave Early Requests etc.

# How to install and setup rasa-startup-admin-chatbot

Step 1: To install admin-chatbot, please clone the repo:

`git clone https://github.com/Gritfeat-Solutions/rasa-startup-admin-chatbot.git`

`cd admin-chatbot`

Use the requirements.txt file to install the appropriate dependencies via pip. 

Step 2: Install requirements:

`pip3 install -r requirements.txt`

Step 3: Install the spaCy English language model by running:

`python3 -m spacy download en`

This will install the bot and all of its requirements.

# How to run admin-chatbot  

1.To train the dialogue model  

`python3 -m rasa_core.train -d domain.yml -s data/core -o models/current/dialogue -c core_config.yml`

This will train the Rasa Core model and store it inside the /models/current/dialogue folder of your project directory.
Before training dialogue model edit domain.yml file as required. (for example, adding your form links (G-drive/or any) to the respective field inside templates.)

2. To train the NLU model  

`python3  -m rasa_nlu.train -c nlu_config.yml --data data/nlu_data.md -o models --fixed_model_name nlu --project current --verbose`

The parameter provided are configuration file, data and path to save NLU model along with fixed name.

3. To run the bot in terminal  

`python3 -m rasa_core.run -d models/current/dialogue -u models/current/nlu`

This will start your bot in terminal and you can start chatting with it.

4. Specify port you want to expose to public internet by using ngrok:  
To create a local webhook from your machine you can use Ngrok. Follow the instructions on their site to set it up on your computer. Move ngrok to your working directory and in a new terminal run:

`./ngrok http 5000`

5. Set up Rocket.Chat by logging as administrator 
To set up Rocket.Chat perform the steps mentioned [here](https://rasa.com/docs/core/connectors/#rocketchat-setup)
Your url will be something like this: `https://xxxxxxx.ngrok.io/webhooks/rocketchat/webhook`. You will have to change url everytime you redo step 4.

6. Run the command below for integration  
Go to the credentials.yml file that you downloaded from the repo and input your user, password and server-url.

`python3 -m rasa_core.run -d models/current/dialogue -u models/current/nlu --port 5000 --credentials credentials.yml`
