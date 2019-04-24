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


##happy_path3
* expense_compensation
  - utter_expense_compensation
* thankyou
  - utter_noworries


##happy_path4
* days_off
  - days_off_form
  - form{"name":"days_off_form"}
  - form{"name":null}
  - utter_confirmation
* affirmation
  - action_days_off_mail
  - utter_mail_send
* thankyou
  - utter_noworries
  - action_restart	

##unhappy_path
* days_off
  - days_off_form
  - form{"name":"days_off_form"}
  - form{"name":null}
  - utter_confirmation
* deny
  - action_restart
  - utter_ask_options_type
* days_off 
  - days_off_form
  - form{"name":"days_off_form"}
  - form{"name":null}
  - utter_confirmation
* affirmation
  - action_days_off_mail
  - utter_mail_send
* thankyou
  - utter_noworries
  - action_restart


