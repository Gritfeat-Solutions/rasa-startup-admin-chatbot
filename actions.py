# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, Text, Any, List, Union

from rasa_sdk import ActionExecutionRejection
from rasa_sdk import Tracker
from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_sdk import Action
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
                "from": [self.from_entity(entity='time')],
                "to": [self.from_entity(entity='time')],
                "reason": [self.from_text(intent='days_off_reason'),
                                self.from_text()],
                "pending": [self.from_text(intent='pending'), self.from_text()]}


    @staticmethod
    def from_validation(date_text) -> bool:
        start = parse(date_text)
        now = datetime.strftime(datetime.now(), '20%y-%m-%d')
        range = pd.date_range(start=now, end= datetime.strftime(datetime.now()+timedelta(30), '20%y-%m-%d'))
        if start in (range): 
            return True
        else:
            return False

    @staticmethod
    def to_validation(to, start) -> bool:
        #to = datetime.strptime(date_text, '%Y-%m-%d')
        #to = parse(to)
        #start = tracker.get_slot('from')
        strt = datetime.strptime(start, '20%y-%m-%d')
        range = pd.date_range(start=strt, end= datetime.strftime(strt+timedelta(30), '20%y-%m-%d'))
        if to in (range): 
            return True
        else:
            return False

    def validate_from(self,value,dispatcher,tracker,domain):
        if any(tracker.get_latest_entity_values("time")):
            if isinstance(value,dict):
                from_date = value['from'][0:10]
                to_date = value['to'][0:10]

                if self.from_validation(from_date)==False:
                    dispatcher.utter_template('utter_range',tracker)
                    return{"from":None}
                    
                    if self.to_validation(to_date,from_date)==False:
                        dispatcher.utter_template('utter_range',tracker)
                        return{"to":None}
                else:    
                    return {
                        'from': value['from'][0:10],
                        'to': datetime.strftime(parse(value['to'][0:10])- timedelta(days=1),"%Y-%m-%d")
                    }
            else:
                from_date = value[0:10]
                if self.from_validation(from_date)==False:
                    dispatcher.utter_template('utter_range',tracker)
                    return{"from":None}
                else:
                    return {'from':value[0:10]}

        else:
            # no entity was picked up, we want to ask again
            dispatcher.utter_template("utter_no_date", tracker)
            return {"from": None}


    def validate_to(self,value,dispatcher,tracker,domain):
        if any(tracker.get_latest_entity_values("time")):
            # entity was picked up, validate slot
            if isinstance(value,dict):
                to_date = value['to'][0:15]
            else:
                to_date = value[0:10]
            if self.to_validation(to_date,tracker.get_slot('from'))==False:
                dispatcher.utter_template('utter_range',tracker)
                return {"to": None}
            else:
                return {"to": to_date}
        else:
            # no entity was picked up, we want to ask again
            dispatcher.utter_template("utter_no_date", tracker)
            return {"to": None}

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

        msg.set_content('Hey Admins!,\nOur member \"{}\" has submitted a days off request starting from \"{}\" to \"{}\" (if both dates are same, its a one day leave request).\nThe reason for the leave request: {}.\nTask and Incharge: {}.\nPlease acknowledge this request. \nYour\'s sincerely,\nGritfeat-bot'.format(user, start, end, reason, pending)) 

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
                "request": [self.from_entity('time')],
                "time": [self.from_entity(entity='time')],
                "reason": [self.from_text(intent="reason"), self.from_text()]
                }

    @staticmethod
    def date_validation(date_text) -> bool:
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except:
            return False

    @staticmethod
    def from_validation(date_text) -> bool:
        start = parse(date_text)
        now = datetime.strftime(datetime.now(), '20%y-%m-%d')
        range = pd.date_range(start=now, end= datetime.strftime(datetime.now()+timedelta(30), '%Y-%m-%d'))
        if start in (range): 
            return True
        else:
            return False

    @staticmethod
    def time_validation(time_text) -> bool:
        if (parse('13:00') <= parse(time_text)) & (parse('17:00') >= parse(time_text)):
            return True
        else:
            return False


    def validate_request(self,value,dispatcher,tracker,domain):
        if any(tracker.get_latest_entity_values("time")):
            date = value[0:10]
            if self.from_validation(date)==False:
                dispatcher.utter_template('utter_range',tracker)
                return {"request":None}
            else:
                return {"request":date}
        else:
            # no entity was picked up, we want to ask again
            dispatcher.utter_template("utter_no_date", tracker)
            return {"to": None}

    def validate_time(self,value,dispatcher,tracker,domain):
        if any(tracker.get_latest_entity_values("time")):
            if value[11:16] != '00:00':
                time = datetime.strftime(parse(value[11:16]),format = "%I:%M %p")
                if self.time_validation(time)==False:
                    dispatcher.utter_template('utter_wrong_time',tracker)
                    return{"time":None}
                else:
                    return{"time":time}
            else:
                return{"time":None}


            # if self.time_validation(time)==False:
            #     dispatcher.utter_template('utter_wrong_time',tracker)
            #     return{"time":None}
            # else:
            #     return{"time":time}


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
        msg.set_content('Hey Admins!,\nOur member \"{}\" has submitted a leave early request.\nEarly leave Date: \"{}\"\nLeaving Time: \"{}\".\nThe reason for the request is \"{}\".\nPlease acknowledge this request. \nYour\'s sincerely,\nGritfeat-bot'.format(user, request, time, reason)) 

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
                "date": self.from_entity(entity="time"),
                "type": self.from_text(),
                "desc": self.from_text(),
                "amount": self.from_entity(entity='money', intent='inform')}


    @staticmethod
    def date_validation(date_text) -> bool:
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except:
            return False

    def validate_date(self,value,dispatcher,tracker,domain):
        if any(get_latest_entity_values('time')):
            date = value[0:10]
            if self.date_validation(date)==False:
                dispatcher.utter_template('utter_wrong_date',tracker)
                return{'date':None}
            else:
                return{'date':None}
        else:
            dispatcher.utter_template('utter_no_date',tracker)
            return{'date': None}

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

        msg.set_content('Hey Admins!, \n Our member \"{}\" has an expense compensation request of Rs. {} for items \"{}\". Purchased on \"{}\".\n Please Acknowledge the request. \n Sincerely, Gritfeat-bot'.format(user, amount, desc, date)) 
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('EMAIL_ADDRESS', 'PASSWORD') #replace with your email and password
            smtp.send_message(msg)

class Library(FormAction):

    def name(self):
        #type: () -> Text
        return "library_form"


    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        return ["book"]

    def slot_mappings(self):

        return {"book": self.from_text()}


    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_template('utter_submit', tracker)
        return []



class LibraryMail(Action):
    def name(self):
        return 'action_library'
  
    def run(self, dispatcher, tracker, domain):
        import os
        import smtplib
        from email.message import EmailMessage
        
        book = tracker.get_slot('book')
        issue = tracker.get_slot('from')
        due = tracker.get_slot('to')
        user = tracker.get_slot('name')

        msg = EmailMessage()
        msg['Subject'] = 'Book Request'
        msg['Subject'] = 'Expense Compensation Request'
        msg['From'] = 'sending_email_address' #sender's email address
        msg.set_content('Hey Admins!, \n Our member \"{}\" has a book request\nName of the book: {}\nIssue Date:{}\nDue Date: {}\n Please Acknowledge the request. \n Sincerely, Gritfeat-bot'.format(user, book, issue, due)) 

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('EMAIL_ADDRESS', 'PASSWORD') #replace with your email and password
            smtp.send_message(msg)

class LibraryDate(Action):
    def name(self):
        return 'action_library_date'

    def run(self, dispatcher, tracker, domain):
        now = datetime.strftime(datetime.now(), '20%y-%m-%d')
        due = datetime.strftime(datetime.now()+timedelta(14), '20%y-%m-%d')
        return [SlotSet('from',now),SlotSet('to',due)]

class PurchaseReq(FormAction):
    def name(self):
        return "purchase_req_form"


    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        return ["p_desc", "qty", "date_needed"]

    def slot_mappings(self):

        return {"p_desc": self.from_text(), 
                "qty": [self.from_text(),self.from_entity(entity="quantity")],
                "date_needed": self.from_text()}

    @staticmethod
    def date_validation(date_text) -> bool:
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except:
            return False

    @staticmethod
    def from_validation(date_text) -> bool:
        start = parse(date_text)
        now = datetime.strftime(datetime.now(), '20%y-%m-%d')
        range = pd.date_range(start=now, end= datetime.strftime(datetime.now()+timedelta(30), '20%y-%m-%d'))
        if start in (range): 
            return True
        else:
            return False

    def validate_date_needed(self,value,dispatcher,tracker,domain):
        if any(tracker.get_latest_entity_values("time")):
            date = value[0:10]
            if self.from_validation(date)==False:
                dispatcher.utter_template('utter_range',tracker)
                return {"date_needed":None}
            else:
                return {"date_needed":date}
        else:
            # no entity was picked up, we want to ask again
            dispatcher.utter_template("utter_no_date", tracker)
            return {"date_needed": None}

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_template('utter_submit', tracker)
        return []

class PurchaseReqMail(Action):
    def name(self):
        return 'action_purchase_mail'

    def run(self, dispatcher, tracker, domain):
        import os
        import smtplib
        from email.message import EmailMessage

        desc = tracker.get_slot('p_desc')
        quantity = tracker.get_slot('qty')
        date = tracker.get_slot('date_needed')
        user = tracker.get_slot('name')

        msg = EmailMessage()
        msg['Subject'] = 'Purchase Requisition Form'
        msg['From'] = 'sending_email_address'  #sender's email address
        msg['To'] = 'receiving_email_address'  #receiver's email address
        msg.set_content('Hey Admins!,\nOur member \"{}\" has submitted a purchase requisition form with following description:\nItem Description: {}\nQuantity: {}\nDate needed: {}\nPlease acknowledge this request. \nYour\'s sincerely,\nGritfeat-bot'.format(user, desc, quantity, date))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('EMAIL_ADDRESS', 'PASSWORD') #replace with your email and password
            smtp.send_message(msg)


class ActionSlotReset(Action): 
    def name(self): 
        return 'action_slot_reset'

    def run(self, dispatcher, tracker, domain): 
        return[AllSlotsReset()]

class TellJoke(Action):
    def name(self):
        return 'action_tell_joke'

    def run(self,dispatcher,tracker,domain):
        import json
        import requests 
        headers = {'Accept': 'application/json'}
        request = json.loads(requests.get('https://icanhazdadjoke.com', headers= headers).text)  # make an api call
        joke = request['joke'] 

        dispatcher.utter_message(joke)
        return[]
