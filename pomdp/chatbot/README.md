#### NLU trainer

To start the on-line trainer, go to the data directory and run:

    rasa-nlu-trainer


#### Train the model

    python3.6 -m rasa_nlu.train -c data/nlu_config.yml --data data/nlu_data.json -o models --fixed_model_name nlu --project current --verbose

#### run NLU as standalone server

    python3.6 -m rasa_nlu.server --path models/current


#### send query to stand alone server

    curl -X POST localhost:5000/parse -d '{"q":"hi","project":"current"}'


#### Train dialogue manager

    python3.6 -m rasa_core.train -d data/domain.yml -s data/stories.md -o models/dialogue --epochs 500

#### start Slack Connector (Server)

    python3 slack_connector.py


#### Custom Action Server

Using the Action Server let you modify the actions without re-training the dialogue engine. 
Configuration is in data/endpoint.yml

to start the action server, run:
        
    python -m rasa_core_sdk.endpoint --actions actions

When modifying the actions, just restart the above action server script. 

#### Interactive mode

This has a bug. use the code instead

    python -m rasa_core.train --online -o models/dialogue -d data/domain.yml -s data/stories.md --endpoints data/endpoints.yml
        

#### Test the code
    
    python3.6 nlu_test.py
    


#### Send message in Slack to me (Ofer)
    curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello, World!"}' https://hooks.slack.com/services/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

#### Send a message to Anan in Slack
    curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello, World!"}'  https://hooks.slack.com/services/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


#### Slack integration

We use ngrok to as an HTTP proxy. 
After starting ngrok
 
    get the address of the server
    - go to Slack API web site
    - click on Your App
    - choose Virtual Cloud Assistant
    - change the address of ngrok in
        - Event Subscription
        - Interactive Components

#### Keras Policy
    
add to policy_config.yml

  - name: KerasPolicy
    epochs: 100
    max_history: 5

#### Embedding Policy    

add to policy_config.yml

  - name: EmbeddingPolicy
    epochs: 2000
    attn_shift_range: 5
