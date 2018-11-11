# NLU trainer

To start the on-line trainer, go to the data directory and run:

    rasa-nlu-trainer


## Train the model

    python3.6 -m rasa_nlu.train -c data/nlu_config.yml --data data/nlu_data.json -o models --fixed_model_name nlu --project current --verbose

## run NLU as standalone server

    python3.6 -m rasa_nlu.server --path models/current


## send query to stand alone server



## Train dialogue manager

    python3.6 -m rasa_core.train -d data/domain.yml -s data/stories.md -o models/dialogue --epochs 500


## Custom Action Server

Using the Action Server let you modify the actions without re-training the dialogue engine. 
Configuration is in data/endpoint.yml

to start the action server, run:
        
    python -m rasa_core_sdk.endpoint --actions actions

When modifying the actions, just restart the above action server script. 

## Interactive mode

This has a bug. use the code instead

    python -m rasa_core.train --online -o models/dialogue -d data/domain.yml -s data/stories.md --endpoints data/endpoints.yml
        

## Test the code
    
    python3.6 nlu_test.py
    


## Send message in Slack to me (Ofer)
    curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello, World!"}' https://hooks.slack.com/services/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

## Send a message to Anan in Slack
    curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello, World!"}'  https://hooks.slack.com/services/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

 