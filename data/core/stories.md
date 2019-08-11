## story_goodbye
* bye
  - utter_goodbye

## story_thankyou
* thankyou
  - utter_noworries

## story_greet
* greet
  - action_name
  - utter_ask_options_type

## story_days_off
* options{"days_off":"Days Off"}
  - days_off_form
  - form{"name":"days_off_form"}
  - form{"name":null}
  - utter_days_off
  - utter_confirm
* affirmation
  - action_days_off_mail
  - utter_mail_send
  - action_restart	
* thankyou
  - utter_noworries

## story_days_off2
* options{"days_off":"Days Off"}
  - days_off_form
  - form{"name":"days_off_form"}
  - form{"name":null}
  - utter_days_off
  - utter_confirm
* deny
  - action_slot_reset
  - action_name
  - utter_ask_options_type
* options{"days_off":"Days Off"}
  - days_off_form
  - form{"name":"days_off_form"}
  - form{"name":null}
  - utter_days_off
  - utter_confirm
* affirmation
  - action_days_off_mail
  - utter_mail_send
  - action_restart	
* thankyou
  - utter_noworries

## story_early_leave
* options{"early_leave":"Early Leave"}
  - early_leave_form
  - form{"name":"early_leave_form"}
  - form{"name":null}
  - utter_early_leave
  - utter_confirm
* affirmation
  - action_early_leave_mail
  - utter_mail_send
  - action_restart	
* thankyou
  - utter_noworries

## story_expense_compensation
* options{"expense_compensation":"Expense Compensation"}
  - expense_compensation_form
  - form{"name":"expense_compensation_form"}
  - form{"name":null}
  - utter_expense_compensation
  - utter_confirm
* affirmation
  - action_expense_compensation_mail
  - utter_receipt
  - action_restart	
* thankyou
  - utter_noworries

## story_early_leave2
* options{"early_leave":"Early Leave"}
  - early_leave_form
  - form{"name":"early_leave_form"}
  - form{"name":null}
  - utter_early_leave
  - utter_confirm
* deny
  - action_slot_reset
  - action_name
  - utter_ask_options_type
* options{"early_leave":"Early Leave"}
  - early_leave_form
  - form{"name":"early_leave_form"}
  - form{"name":null}
  - utter_early_leave
  - utter_confirm
* affirmation
  - action_early_leave_mail
  - utter_mail_send
  - action_restart	
* thankyou
  - utter_noworries

## story_expense_compensation2
* options{"expense_compensation":"Expense Compensation"}
  - expense_compensation_form
  - form{"name":"expense_compensation_form"}
  - form{"name":null}
  - utter_expense_compensation
  - utter_confirm
* deny
  - action_slot_reset
  - action_name
  - utter_ask_options_type
* options{"expense_compensation":"Expense Compensation"}
  - expense_compensation_form
  - form{"name":"expense_compensation_form"}
  - form{"name":null}
  - utter_expense_compensation
  - utter_confirm
* affirmation
  - action_expense_compensation_mail
  - utter_receipt
  - action_restart	
* thankyou
  - utter_noworries


## story_book_request2
* options{"book_request":"Book Request"}
  - library_form
  - form{"name":"library_form"}
  - form{"name":"null"}
  - action_library_date
  - utter_library
  - utter_confirm
* deny 
  - action_slot_reset
  - action_name
  - utter_ask_options_type
* options{"book_request":"Book Request"}
  - library_form
  - form{"name":"library_form"}
  - form{"name":"null"}
  - action_library_date
  - utter_library
  - utter_confirm
* affirmation
  - action_library
  - utter_mail_send
  - action_restart
* thankyou
  - utter_noworries

## story_book_request
* options{"book_request":"Book Request"}
  - library_form
  - form{"name":"library_form"}
  - form{"name":"null"}
  - action_library_date
  - utter_library
  - utter_confirm
* affirmation
  - action_library
  - utter_mail_send
  - utter_next_book
  - action_slot_reset
  - action_name
* affirmation
  - library_form
  - form{"name":"library_form"}
  - form{"name":"null"}
  - action_library_date
  - utter_library
  - utter_confirm
* affirmation
  - action_library
  - utter_mail_send
  - action_restart

## story_book_request3
* options{"book_request":"Book Request"}
  - library_form
  - form{"name":"library_form"}
  - form{"name":"null"}
  - action_library_date
  - utter_library
  - utter_confirm
* affirmation
  - action_library
  - utter_mail_send
  - utter_next_book
  - action_slot_reset
  - action_name
* deny 
  - utter_noworries

## story_purchase_req
* options{"purchase_req":"Purchase Requisition"}
  - purchase_req_form
  - form{"name":"purchase_req_form"}
  - form{"name":"null"}
  - utter_purchase_req
  - utter_confirm
* affirmation
  - action_purchase_mail
  - utter_mail_send
  - action_restart
* thankyou
  - utter_noworries

## story_purchase_req2
* options{"purchase_req":"Purchase Requisition"}
  - purchase_req_form
  - form{"name":"purchase_req_form"}
  - form{"name":"null"}
  - utter_purchase_req
  - utter_confirm
* deny 
  - action_slot_reset
  - action_name
  - utter_ask_options_type
* options{"purchase_req":"Purchase Requisition"}
  - purchase_req_form
  - form{"name":"purchase_req_form"}
  - form{"name":"null"}
  - utter_purchase_req
  - utter_confirm
* affirmation
  - action_purchase_mail
  - utter_mail_send
  - action_restart
* thankyou
  - utter_noworries
  
  ## story_telljoke
* telljoke
  - action_tell_joke
