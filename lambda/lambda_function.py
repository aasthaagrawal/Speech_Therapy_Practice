# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
import os
import json
import locale
import requests
import calendar
import gettext
import random
from datetime import datetime
from pytz import timezone
from ask_sdk_s3.adapter import S3Adapter
from ask_sdk_model.dialog import DelegateDirective
s3_adapter = S3Adapter(bucket_name=os.environ["S3_PERSISTENCE_BUCKET"])

from alexa import data

from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractRequestInterceptor, AbstractExceptionHandler)
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

from ask_sdk_core.utils import is_request_type, is_intent_name

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

NUM_ALPHABET_OPTIONS = 3
alphabet_options_string = "1. sound R, 2. sound L, 3. sound S,"
alphabet_options = ["R", "L", "S"]
practice_types_string = "words, phrases or sentences"
practice_types = ["words", "phrases", "sentences"]
practice_collection = {}

class LaunchRequestHandler(AbstractRequestHandler):
    """
    Handler for Skill Launch
    """
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        data = handler_input.attributes_manager.request_attributes["_"]
        speech = data["WELCOME_MSG"].format(alphabet_options_string)
        reprompt = data["WELCOME_REPROMPT_MSG"].format(alphabet_options_string)
        handler_input.response_builder.speak(speech).ask(reprompt)
        return handler_input.response_builder.response

class AlphabetOptionsRepeatHandler(AbstractRequestHandler):
    
    #Handler for Repeating options to the user
    
    def can_handle(self, handler_input):
        return is_intent_name("AlphabetOptionsRepeatIntent")(handler_input)

    def handle(self, handler_input):
        data = handler_input.attributes_manager.request_attributes["_"]
        speech = data["ALPHABET_OPTIONS_REPEAT_MSG"].format(alphabet_options_string)
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response

class SetAlphabetHandler(AbstractRequestHandler):
    
    #Handler for setting alphabet_option session attribute and asking user about practice type
    
    def can_handle(self, handler_input):
        return is_intent_name("SetAlphabetIntent")(handler_input)
    
    def handle(self, handler_input):
        data = handler_input.attributes_manager.request_attributes["_"]
        slots = handler_input.request_envelope.request.intent.slots
        alphabet_option = int(slots["alphabet_option"].value)-1
        
        if alphabet_option>(len(alphabet_options)-1) or alphabet_option<0:
            speech =  data["ALPHABET_OPTIONS_REPEAT_MSG"].format(alphabet_options_string)
            handler_input.response_builder.speak(speech).ask(speech)
            return handler_input.response_builder.response
        
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr['alphabet_option'] = alphabet_option
        speech = data["PRACTICE_TYPE_MSG"].format(alphabet_options[alphabet_option], practice_types_string)
        repromt = data["PRACTICE_TYPE_REPROMPT_MSG"].format(practice_types_string)
        handler_input.response_builder.speak(speech).ask(repromt)
        return handler_input.response_builder.response

class CreatePracticeHandler(AbstractRequestHandler):
    
    #Handler for recording practice_type attribute
    
    def can_handle(self, handler_input):
        return is_intent_name("CreatePracticeIntent")(handler_input)
    
    def handle(self, handler_input):
        data = handler_input.attributes_manager.request_attributes["_"]
        slots = handler_input.request_envelope.request.intent.slots
        practice_type = slots["practice_type"].value
        if practice_type not in practice_types:
            speech = data["PRACTICE_TYPE_REPROMPT_MSG"].format(practice_types_string)
            handler_input.response_builder.speak(speech).ask(speech)
            return handler_input.response_builder.response
        
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr['practice_type'] = practice_type
        
        speech = data["NUM_PRACTICES_MSG"].format(practice_type)
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response

class StartPracticeHandler(AbstractRequestHandler):
    
    #Handler for creating practice item and telling the user to repeat
    
    def can_handle(self, handler_input):
        return is_intent_name("StartPracticeIntent")(handler_input)
    
    def handle(self, handler_input):
        data = handler_input.attributes_manager.request_attributes["_"]
        slots = handler_input.request_envelope.request.intent.slots
        session_attr = handler_input.attributes_manager.session_attributes
        num_practices = int(slots["num_practices"].value)
        if "alphabet_option" not in session_attr:
            speech = data["ALPHABET_OPTIONS_REPEAT_MSG"].format(alphabet_options_string)
            handler_input.response_builder.speak(speech).ask(speech)
            return handler_input.response_builder.response
        if "practice_type" not in session_attr:
            speech = data["PRACTICE_TYPE_REPROMPT_MSG"].format(practice_types_string)
            handler_input.response_builder.speak(speech).ask(speech)
            return handler_input.response_builder.response
        
        session_attr["num_practices"] = num_practices
        session_attr["num_left_practices"] = num_practices
        alphabet_option = alphabet_options[session_attr["alphabet_option"]]
        practice_type = session_attr["practice_type"]
        global practice_collection
        collection = practice_collection[alphabet_option][practice_type]
        if (num_practices > len(collection)):
            speech = data["CORRECT_NUM_PRACTICES_MSG"].format(len(collection))
            handler_input.response_builder.speak(speech).ask(speech)
            return handler_input.response_builder.response
        practice_item_indices = random.sample(range(len(collection)-1), num_practices)
        practice_items = []
        for index in practice_item_indices:
            practice_items.append((collection[index]).lower())
        session_attr['practice_items'] = practice_items
        speech = data["START_SESSION_MSG"]
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response

class ContinuePracticeHandler(AbstractRequestHandler):
    
    #Handler for creating practice item and telling the user to repeat
    
    def can_handle(self, handler_input):
        return is_intent_name("ContinuePracticeIntent")(handler_input)
    
    def handle(self, handler_input):
        data = handler_input.attributes_manager.request_attributes["_"]
        session_attr = handler_input.attributes_manager.session_attributes
        current_intent = handler_input.request_envelope.request.intent
        # num_practices = session_attr["num_practices"]
        num_left_practices = session_attr["num_left_practices"]
        if (num_left_practices == 0):
            speech = data["QUIT_OR_CONTINUE_MSG"]
            handler_input.response_builder.speak(speech).ask(speech)
            return handler_input.response_builder.response
        practice_items = session_attr['practice_items']
        session_attr['practice_item'] = practice_items[num_left_practices - 1]
        speech = data["START_PRACTICE_MSG"].format(practice_items[num_left_practices - 1])
        session_attr["num_left_practices"] -= 1
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response

class ValidationHandler(AbstractRequestHandler):
    
    #Handler for validating user utterence 
    
    def can_handle(self, handler_input):
        return is_intent_name("ValidationIntent")(handler_input)
    
    def handle(self, handler_input):
        data = handler_input.attributes_manager.request_attributes["_"]
        slots = handler_input.request_envelope.request.intent.slots
        session_attr = handler_input.attributes_manager.session_attributes
        user_item = (slots["sentence"].value).lower()
        practice_item = session_attr["practice_item"]
        alphabet_option = session_attr["alphabet_option"]
        # print(alphabet_option)
        
        practice_item_words = practice_item.split(" ")
        user_item_words = user_item.split(" ")
        
        if len(user_item_words) != len(practice_item_words):
            speech = data["VALIDATION_INCORRECT_USER_SENTENCE"].format(user_item, practice_item)
            handler_input.response_builder.speak(speech).ask(speech)
            return handler_input.response_builder.response
        else:
            wrong_index = len(user_item_words)
            for i in range(len(user_item_words)):
                if user_item_words[i] != practice_item_words[i]:
                    lowercase_word = practice_item_words[i].lower()
                    if (alphabet_option == 0):
                        if "r" in lowercase_word:
                            wrong_index = i;
                            break;
                    if (alphabet_option == 1):
                        if "l" in lowercase_word:
                            wrong_index = i;
                            break;
                    if (alphabet_option == 2):
                        if "s" in lowercase_word or "c" in lowercase_word:
                            wrong_index = i;
                            break;
                    
            if (wrong_index == 0):
                speech = data["VALIDATION_INCORRECT_USER_SENTENCE"].format(user_item, practice_item)
                handler_input.response_builder.speak(speech).ask(speech)
                return handler_input.response_builder.response
            elif (wrong_index == len(user_item_words)):
                num_correct_string_options = len(data["VALIDATION_CORRECT_USER_SENTENCE"])
                index = random.randint(0, num_correct_string_options-1)
                speech = data["VALIDATION_CORRECT_USER_SENTENCE"][str(index)] + " " + data["SAY_NEXT_SENTENCE"]
                handler_input.response_builder.speak(speech).ask(speech)
                return handler_input.response_builder.response
            else:
                speech = data["VALIDATION_ALMOST_CORRECT_SENTENCE"].format(practice_item_words[wrong_index], practice_item)
                handler_input.response_builder.speak(speech).ask(speech)
                return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        data = handler_input.attributes_manager.request_attributes["_"]
        speak_output = data["HELP_MSG"]

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        data = handler_input.attributes_manager.request_attributes["_"]
        speak_output = data["QUIT_MSG"]

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        data = handler_input.attributes_manager.request_attributes["_"]
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = data["REFLECTOR_MSG"].format(intent_name)

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        data = handler_input.attributes_manager.request_attributes["_"]
        speak_output = data["ERROR_MSG"]

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


class LocalizationInterceptor(AbstractRequestInterceptor):
    """
    Add function to request attributes, that can load locale specific data.
    """

    def process(self, handler_input):
        skill_locale = handler_input.request_envelope.request.locale

        # localized strings stored in language_strings.json
        with open("language_strings.json") as language_prompts:
            language_data = json.load(language_prompts)
        # set default translation data to broader translation
        data = language_data[skill_locale[:2]]
        # if a more specialized translation exists, then select it instead
        # example: "fr-CA" will pick "fr" translations first, but if "fr-CA" translation exists,
        #          then pick that instead
        if skill_locale in language_data:
            data.update(language_data[skill_locale])
        handler_input.attributes_manager.request_attributes["_"] = data

        # configure the runtime to treat time according to the skill locale
        skill_locale = skill_locale.replace('-','_')
        locale.setlocale(locale.LC_TIME, skill_locale)
        
        global practice_collection
        with open("collection.json") as collection:
            practice_collection = json.load(collection)
        

sb = CustomSkillBuilder(persistence_adapter=s3_adapter)

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(AlphabetOptionsRepeatHandler())
sb.add_request_handler(SetAlphabetHandler())
sb.add_request_handler(CreatePracticeHandler())
sb.add_request_handler(StartPracticeHandler())
sb.add_request_handler(ContinuePracticeHandler())
sb.add_request_handler(ValidationHandler())
# sb.add_request_handler(QuitHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn’t override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

sb.add_global_request_interceptor(LocalizationInterceptor())


lambda_handler = sb.lambda_handler()