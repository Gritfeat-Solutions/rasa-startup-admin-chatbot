# -*- coding: utf-8 -*-
import datetime
from typing import Dict, Text, Any, List, Union

from rasa_core_sdk import ActionExecutionRejection
from rasa_core_sdk import Tracker
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.executor import CollectingDispatcher
from rasa_core_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_core_sdk import Action
from dateutil.parser import parse

class GetName(Action):
	def name(self):
		return 'action_name'
		
	def run(self, dispatcher, tracker, domain):
		import requests
		
		most_recent_state = tracker.current_state()
		user = most_recent_state['sender_id']
		bot = "" #bot-userid
		name = user.split(bot)
		for i in name:
			if i != '':
        			sid = i
		headers = {
    			'X-Auth-Token': '', #bot-auth-token
    			'X-User-Id': ''  #bot-userid
			}
		r = requests.get('https://server-url/api/v1/users.info?userId={}'.format(sid), headers=headers,allow_redirects=False).json() #replace server-url with your own server url
		first_name = r['user']['name']
		return [SlotSet('name', first_name)]
	
class DaysOffForm(FormAction):
    """Example of a custom form action"""

    def name(self):
        # type: () -> Text
        """Unique identifier of the form"""

        return "days_off_form"


    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["name", "from", "to",
                "reason", "pending"]

    def slot_mappings(self):
        # type: () -> Dict[Text: Union[Dict, List[Dict]]]
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {"name": [self.from_entity(entity="name"),self.from_text()],
                "from": [self.from_text()],
                "to": [self.from_text()],
                "reason": [self.from_text(intent='days_off_reason'),
                                self.from_text()],
                "pending": [self.from_text(intent='pending'), self.from_text()]}
    @staticmethod
    def date_validation(date_text) -> bool:
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except:
            return False


    def validate(self,
                 dispatcher: CollectingDispatcher,
                 tracker: Tracker,
                 domain: Dict[Text, Any]) -> List[Dict]:
        """Validate extracted requested slot
            else reject the execution of the form action
        """
        # extract other slots that were not requested
        # but set by corresponding entity
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)

        # extract requested slot
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
        if slot_to_fill:
            slot_values.update(self.extract_requested_slot(dispatcher,
                                                           tracker, domain))
            if not slot_values:
                # reject form action execution
                # if some slot was requested but nothing was extracted
                # it will allow other policies to predict another action
                raise ActionExecutionRejection(self.name(),
                                               "Failed to validate slot {0} "
                                               "with action {1}"
                                               "".format(slot_to_fill,
                                                         self.name()))

        # we'll check when validation failed in order
        # to add appropriate utterances
        for slot, value in slot_values.items():
            if slot == 'from':
                if self.date_validation(value)==False:
                    dispatcher.utter_template('utter_wrong_date',tracker)
                    slot_values[slot] = None

            if slot == 'to':
                if self.date_validation(value)==False:
                    dispatcher.utter_template('utter_wrong_date',tracker)
                    slot_values[slot] = None


        # validation succeed, set the slots values to the extracted values
        return [SlotSet(slot, value) for slot, value in slot_values.items()]

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_template('utter_submit', tracker)
        return []

class DaysOffMail(Action):
	def name(self):
		return 'action_days_off_mail'
	def run(self, dispatcher, tracker, domain):
		import os
		import smtplib
		from email.message import EmailMessage
		
		start = tracker.get_slot('from')
		end = tracker.get_slot('to')
		reason = tracker.get_slot('reason')
		pending = tracker.get_slot('pending')
		user = tracker.get_slot('name')


		msg = EmailMessage()
		msg['Subject'] = 'Days Off Request'
		msg['From'] = 'sending_email_address' #sender's email address
		msg['To'] = 'receiving_email_address' #receiver's email address

		msg.set_content('Hi,\nOur member \"{}\" has submitted a days off request starting from \"{}\" to \"{}\" (if both dates are same, its a one day leave request).\nThe reason for the leave request: {}.\nTask and Incharge: {}.\nPlease acknowledge this request. \nYour\'s sincerely,\nGritfeat-bot'.format(user, start, end, reason, pending)) 

		with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
			smtp.login('EMAIL_ADDRESS', 'PASSWORD') #replace with your email and password
			smtp.send_message(msg)


class EarlyLeaveForm(FormAction):

    def name(self):
        # type: () -> Text

        return "early_leave_form"
    
    @staticmethod
    def required_slots(tracker:Tracker) -> List[Text]:
        """ A list of required slots that the form has to fill"""

        return ["name", "request", "time", "reason"]


    def slot_mappings(self):
        # type: () -> Dict[Text: Union[Dict, List[Dict]]]
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        
        return {"name": [self.from_entity(entity="name"),self.from_text()],
                "request": [self.from_text(),self.from_entity(entity='date', intent='inform')],
                "time": [self.from_text(),self.from_entity(entity='time', intent='inform')],
                "reason": [self.from_text(intent="reason"), self.from_text()]
                }

    @staticmethod
    def date_validation(date_text) -> bool:
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except:
            return False

    @staticmethod
    def time_validation(time_text) -> bool:
        try:
            date = parse(time_text)
            datetime.datetime.strftime(date,'%H:%M %p')
            return True
        except:
            return False

    def validate(self,
                 dispatcher: CollectingDispatcher,
                 tracker: Tracker,
                 domain: Dict[Text, Any]) -> List[Dict]:
        """Validate extracted requested slot
            else reject the execution of the form action
        """
        # extract other slots that were not requested
        # but set by corresponding entity
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)

        # extract requested slot
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
        if slot_to_fill:
            slot_values.update(self.extract_requested_slot(dispatcher,
                                                           tracker, domain))
            if not slot_values:
                # reject form action execution
                # if some slot was requested but nothing was extracted
                # it will allow other policies to predict another action
                raise ActionExecutionRejection(self.name(),
                                               "Failed to validate slot {0} "
                                               "with action {1}"
                                               "".format(slot_to_fill,
                                                         self.name()))

        # we'll check when validation failed in order
        # to add appropriate utterances
        for slot, value in slot_values.items():
            if slot == 'request':
                if self.date_validation(value)==False:
                    dispatcher.utter_template('utter_wrong_date',tracker)
                    slot_values[slot] = None

            if slot == 'time':
                if self.time_validation(value)==False:
                    dispatcher.utter_template('utter_wrong_time',tracker)
                    slot_values[slot] = None



        # validation succeed, set the slots values to the extracted values
        return [SlotSet(slot, value) for slot, value in slot_values.items()]

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_template('utter_submit', tracker)
        return []

class EarlyLeaveMail(Action):
    def name(self):
        return 'action_early_leave_mail'
    def run(self, dispatcher, tracker, domain):
        import os
        import smtplib
        from email.message import EmailMessage

        request = tracker.get_slot('request')
        time = tracker.get_slot('time')
        reason = tracker.get_slot('reason')
        user = tracker.get_slot('name')

	msg = EmailMessage()
        msg['Subject'] = 'Leave Early Request'
	msg['From'] = 'sending_email_address' #sender's email address
	msg['To'] = 'receiving_email_address' #receiver's email address


        msg.set_content('Hi,\nOur member \"{}\" has submitted a leave early request.\nEarly leave Date: \"{}\"\nLeaving Time: \"{}\".\nThe reason for the request is \"{}\".\nPlease acknowledge this request. \nYour\'s sincerely,\nYour-bot'.format(user, request, time, reason)) 

	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
		smtp.login('EMAIL_ADDRESS', 'PASSWORD') #replace with your email and password
		smtp.send_message(msg)


class ExpenseCompensation(FormAction):
    
    def name(self):
        #type: () -> Text
     
        return "expense_compensation_form"


    @staticmethod
    def required_slots(tracker:Tracker) -> List[Text]:


        return ["name", "date", "type", "desc", "amount"]

    def slot_mappings(self):
        # type: () -> Dict[Text: Union[Dict, List[Dict]]]

        return {"name": [self.from_entity(entity="name"),self.from_text()],
                "date": self.from_text(),
                "type": self.from_text(),
                "desc": self.from_text(),
                "amount": self.from_entity(entity='money', intent='inform')}


    @staticmethod
    def date_validation(date_text) -> bool:
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except:
            return False

    def validate(self,
                 dispatcher: CollectingDispatcher,
                 tracker: Tracker,
                 domain: Dict[Text, Any]) -> List[Dict]:
        """Validate extracted requested slot
            else reject the execution of the form action
        """
        # extract other slots that were not requested
        # but set by corresponding entity
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)

        # extract requested slot
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
        if slot_to_fill:
            slot_values.update(self.extract_requested_slot(dispatcher,
                                                           tracker, domain))
            if not slot_values:
                # reject form action execution
                # if some slot was requested but nothing was extracted
                # it will allow other policies to predict another action
                raise ActionExecutionRejection(self.name(),
                                               "Failed to validate slot {0} "
                                               "with action {1}"
                                               "".format(slot_to_fill,
                                                         self.name()))

        # we'll check when validation failed in order
        # to add appropriate utterances
        for slot, value in slot_values.items():
            if slot == 'date':
                if self.date_validation(value)==False:
                    dispatcher.utter_template('utter_wrong_date',tracker)
                    slot_values[slot] = None


        # validation succeed, set the slots values to the extracted values
        return [SlotSet(slot, value) for slot, value in slot_values.items()]

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_template('utter_submit', tracker)
        return []

class ExpenseCompensationMail(Action):
    def name(self):
        return 'action_expense_compensation_mail'

    def run(self, dispatcher, tracker, domain):
        import os
        import smtplib
        from email.message import EmailMessage

        date = tracker.get_slot('date')
        typ = tracker.get_slot('type')
        desc = tracker.get_slot('desc')
        amount = tracker.get_slot('amount')
        user = tracker.get_slot('name')

	msg = EmailMessage()
        msg['Subject'] = 'Expense Compensation Request'
	msg['From'] = 'sending_email_address' #sender's email address
	msg['To'] = 'receiving_email_address' #receiver's email address


        msg.set_content('Hi, \n Our member \"{}\" has an expense compensation request of Rs. {} for items \"{}\". Purchased on \"{}\".\n Please Acknowledge the request. \n Sincerely, Your-bot'.format(user, amount, desc, date)) 

	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
		smtp.login('EMAIL_ADDRESS', 'PASSWORD') #replace with your email and password
		smtp.send_message(msg)

