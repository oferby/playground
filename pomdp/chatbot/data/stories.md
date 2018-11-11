## greet path
* greeting
    - utter_greet
    - action_restart

## create ecs path 
* create_ecs
    - action_say_ok
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
 
 ## Generated Story -439388227201137117
* request_solution{"application": "web application"}
    - action_request_solution
    - utter_ask_learn_more
* confirm
    - utter_ok
    - action_restart

## request information 1
* request_information
    - action_request_info
    - slot{"isInvalidEntry": "True"}
    - utter_solution_unknown
    - action_restart

## request information 2
* request_information{'component':'oss'}
    - action_request_info
    - slot{"slot_action_info_ok": "True"}
    - utter_is_there_anything_else
    - action_restart         
    
