## greet path
* greeting
    - utter_greet
    - action_restart

## create ecs path 
* create_ecs
    - utter_ask_image_type
> check_os_type

## user wants ubuntu
> check_os_type
* inform{"image_type":"ubuntu"}
    - slot{"image_type":"ubuntu"}
    - utter_ok
    - action_restart
    
## user wants windows
> check_os_type
* inform{"image_type":"windows"}
    - slot{"image_type":"windows"}
    - utter_not_support
    - action_restart

## show ecs path
* show_ecs
    - utter_let_me_check
    - action_show_ecs
    - utter_is_there_anything_else
* deny
    - utter_goodbye
    - action_restart

## change ECS state path
* ecs_change_state{"vm_state":"stop"}
    -utter_get_server_name
* inform{"name":"server1"}
    - action_change_server_state
    - utter_is_there_anything_else
* deny
    - utter_goodbye
    - action_restart

## change ECS state path
* ecs_change_state{"vm_state":"stop"}
    -utter_get_server_name
* inform
    - action_change_server_state
    - slot{"isInvalidEntry": "True"}
    - utter_invalid_server_name
    - action_restart

## change ECS state path
* ecs_change_state{"vm_state":"start", "name":"server1"}
    - action_change_server_state
    - utter_is_there_anything_else
* deny
    - utter_goodbye
    - action_restart
 
## restart command from client
* system_restart
    - action_restart
    
## request info sent to db
* request_information{"component":"obs", "q_type":"what-is"}
    - action_query_db
    - slot{"dbQuerySuccessful": true}
    - action_restart
    
## request info sent to db and not found
* request_information{"component":"obs", "q_type":"what-is"}
    - action_query_db
    - slot{"isInvalidEntry": true}
    - utter_dont_have_answer
    - action_restart

