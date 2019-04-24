# -*- coding: utf-8 -*-
import datetime
from typing import Dict, Text, Any, List, Union

from rasa_core_sdk import ActionExecutionRejection
from rasa_core_sdk import Tracker
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.executor import CollectingDispatcher
from rasa_core_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_core_sdk import Action

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
                    dispatcher.utter_template('utter_wrong_format',tracker)
                    slot_values[slot] = None

            if slot == 'to':
                if self.date_validation(value)==False:
                    dispatcher.utter_template('utter_wrong_format',tracker)
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
		msg['From'] = 'sending_email_address'  #sender's email address
		msg['To'] = 'receiving_email_address'  #receiver's email address

		msg.set_content('Hi,\nOur member {} has submitted a days off request starting from {} to {} (if both dates are same, its a one day leave request). The reason for the leave request is \"{}\" currently \"{}\". Please acknowledge this request. \nYour\'s sincerely,\nYour-bot'.format(user, start, end, reason, pending)) 

		with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
			smtp.login('EMAIL_ADDRESS', 'PASSWORD')	#replace with your email and password
			smtp.send_message(msg)
