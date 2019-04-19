## story_goodbye
* bye
 - utter_goodbye

## story_thankyou
* thankyou
 - utter_noworries

## happy_path
* greet
 - utter_ask_options_type

## happy_path1
* early_leave
 - utter_early_leave
* thankyou
 - utter_noworries

## happy_path2
* days_off
 - utter_days_off
* thankyou
 - utter_noworries

## happy_path3
* expense_compensation
 - utter_expense_compensation
* thankyou
 - utter_noworries
 
 ## happy_path4
* days_off
    - utter_ask_user_name
* name{"name": "elisha"}
    - slot{"name": "elisha"}
    - action_user_name
    - slot{"name": "elisha"}
    - utter_ask_start_date
* inform{"date": "2019 - 04 - 21"}
    - action_start_date
    - slot{"from": "2019 - 04 - 21"}
    - utter_ask_end_date
* inform{"date": "2019 - 04 - 23"}
    - action_end_date
    - slot{"to": "2019 - 04 - 23"}
    - utter_ask_reason
* days_off_reason
    - action_ask_reason
    - slot{"reason": "i am sick"}
    - utter_ask_work_incharge
* work_incharge
    - action_ask_pending
    - slot{"pending": "rojina is incharge"}
    - utter_confirmation
* affirmation
    - action_days_off_mail
    - utter_mail_send
    - action_restart


