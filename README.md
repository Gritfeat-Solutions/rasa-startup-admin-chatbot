A very basic RASA based chatbot, integrated with RocketChat, that can assist with some of the administrative purposes like Days Off Requests, Leave Early Requests etc.

# How to run admin-chatbot  
1.To train the dialogue model  
`python3 -m rasa_core.train -d domain.yml -s data/core -o models/current/dialogue -c core_config.yml`

2. To train the NLU model  
`python3  -m rasa_nlu.train -c nlu_config.yml --data data/nlu_data.md -o models --fixed_model_name nlu --project current --verbose`  
The parameter provided are configuration file, data and path to save NLU model along with fixed name.

3. To run the bot in terminal  
`python3 -m rasa_core.run -d models/current/dialogue -u models/current/nlu`

4. Specify port you want to expose to public internet by using ngrok:  
`./ngrok http 5000`

5. Set up Rocket.Chat by logging as administrator 

6. Run the command below for integration  
`python3 -m rasa_core.run -d models/current/dialogue -u models/current/nlu --port 5000 --credentials credentials.yml`
