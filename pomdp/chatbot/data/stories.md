## path 1
* greeting
    - utter_greet
* create_ecs
    - action_say_ok

## show ecs path
* greeting
    - utter_greet
* show_ecs
    - utter_let_me_check
    - action_show_ecs
    - utter_is_there_anything_else
* deny
    - utter_goodbye

## change ECS state path
* greeting
    - utter_greet
* ecs_change_state{"vm_state":"stop"}
    -utter_get_server_name
* inform{"name":"server1"}
    - action_change_server_state
    - utter_is_there_anything_else
* deny
    - utter_goodbye

## change ECS state path
* greeting
    - utter_greet
* ecs_change_state{"vm_state":"stop"}
    -utter_get_server_name
* inform
    - action_change_server_state
    - slot{"isInvalidEntry": "True"}
    - utter_invalid_server_name

## change ECS state path
* greeting
    - utter_greet
* ecs_change_state{"vm_state":"start", "name":"server1"}
    - action_change_server_state
    - utter_is_there_anything_else
* deny
    - utter_goodbye
 