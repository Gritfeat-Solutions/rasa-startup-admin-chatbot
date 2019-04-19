# -*- coding: utf-8 -*-	
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import print_function

from rasa_core_sdk import Tracker
from rasa_core_sdk.executor import CollectingDispatcher

from typing import Dict, Text, Any, List

import requests
from rasa_core_sdk import Action
from rasa_core_sdk import ActionExecutionRejection
from rasa_core_sdk.events import UserUtteranceReverted
from rasa_core_sdk.events import SlotSet, FollowupAction
from rasa_core_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_core_sdk.events import AllSlotsReset
from rasa_core_sdk.events import Restarted

class AskStartDate(Action):
	def name(self):
		return 'action_start_date'
		
	def run(self, dispatcher, tracker, domain):
		start = next(tracker.get_latest_entity_values("date"), None)
		if not start:
			dispatcher.utter_message("Please enter a start date of your leave(YYYY-MM-DD)")
			return [UserUtteranceReverted()]
		return [SlotSet('from',start)]

class AskEndDate(Action):
	def name(self):
		return 'action_end_date'
		
	def run(self, dispatcher, tracker, domain):
		end = next(tracker.get_latest_entity_values("date"), None)
		if not end:
			dispatcher.utter_message("Please provide end date of your leave(YYYY-MM-DD)")
			return [UserUtteranceReverted()]
		return [SlotSet('to',end)]

class AskReason(Action):
	def name(self):
		return 'action_ask_reason'

	def run(self, dispatcher, tracker, domain):
		personal = tracker.latest_message.get('text')
		return [SlotSet('reason',personal)]

class AskPending(Action):
	def name(self):
		return 'action_ask_pending'
	
	def run(self, dispatcher, tracker,domain):
		message = tracker.latest_message.get('text')
		return [SlotSet('pending',message)]

class GetUserNAme(Action):
	def name(self):
		return 'action_user_name'

	def run(self, dispatcher, tracker, domain):
		user_name = next(tracker.get_latest_entity_values("name"), None)
		if not user_name:
			dispatcher.utter_message("Please enter your name")
			return [UserUtteranceReverted()]
		return [SlotSet('name', user_name)]


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
