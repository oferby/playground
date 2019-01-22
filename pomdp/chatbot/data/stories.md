## greet path
* greeting
    - utter_greet
    - action_restart
    

## Ask My Name
* my_name
    - utter_say_name
    - action_restart

## Are you human 
* what_are_you{"q_are_you":"human"}
    - slot{"q_are_you":"human"}
    - utter_am_i_human
    - action_restart
    

## Are you a bot
* what_are_you{"q_are_you":"bot"}
    - slot{"q_are_you":"bot"}
    - utter_am_i_bot
    - action_restart
    

## What are you
* what_are_you
    - utter_i_am
    - action_restart

    

## How are you
* how_are_you
    - utter_im_fine
    - action_restart

## What can I do
* what_i_do
    - utter_what_i_do
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


## create ecs path
* create_ecs
    - utter_acknowledge
    - utter_ask_if_specific_ecs
> ask_if_specific_ecs

## create ecs with help
> ask_if_specific_ecs
* inform{"q_need_help":"need_help"}
    - slot{"q_need_help":"need_help"}
    - utter_acknowledge
    - utter_need_few_things
    - utter_ask_interest    
* inform{"application":"web_applications"}
    - utter_acknowledge
    - utter_ask_number_of_users
* inform{"number":"100"}
    - utter_ask_care_most
* inform{"q_care_most":"q_price"}
    - slot{"q_care_most":"q_price"}
    - utter_acknowledge
    - utter_have_options
    - utter_just_few_things
    - utter_ask_memory_size
* inform{"q_amount":"q_few"}
    - utter_ask_compute_power
* inform{"q_power":"q_power_not_much"}
    - utter_acknowledge
    - utter_show_options
    - utter_show_options_price
    - utter_choose_or_select_details
* inform{"q_ecs_type":"s2.medium.2"}
    - utter_last_thing
    - utter_ask_image_type
* inform{"image_type":"ubuntu"}
    - utter_os_version
> create_ecs_check_version

## choose OS version number 
> create_ecs_check_version
* inform{"number":"16"}
    - utter_have_everything
    - utter_ask_confirm_create_ecs
> create_esc_final_confirm

## choose OS latest version
> create_ecs_check_version
* inform{"q_options":"latest_version"}
    - utter_have_everything
    - utter_ask_confirm_create_ecs
> create_esc_check_final_confirm


## create ecs without help
> ask_if_specific_ecs
* inform{"q_need_help":"i_know"}
    - slot{"q_need_help":"i_know"}
    - utter_why_come_to_me
    - action_restart

## create ecs final confirmed
> create_esc_check_final_confirm
* confirm
    - utter_infom_server_started
    - utter_sent_login_to_email
    - utter_ask_anything_else
> after_confirm_create_ecs

## create ecs final deny
> create_esc_check_final_confirm
* deny
    - utter_goodbye
    - action_restart


## is there anything else?
> after_confirm_create_ecs
* deny
    - utter_goodbye
    - action_restart

## is there anything else?
> after_confirm_create_ecs
* confim
    - utter_what_i_do
    - action_restart


## move to cloud
* move_to_cloud
    - utter_what_i_do
    - action_restart


## architecture request
* req_architecture{"application":"gaming"}
    - slot{"application":"gaming"}
    - utter_game_architecture
    - action_restart

## architecture 2 request
* req_architecture{"application":"gaming"}
    - slot{"application":"gaming-business"}
    - utter_game_architecture_business
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
    - action_admin_restart
    


