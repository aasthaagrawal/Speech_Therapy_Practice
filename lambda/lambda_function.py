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
from random import randint
from datetime import datetime
from pytz import timezone
from ask_sdk_s3.adapter import S3Adapter
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

PHRASES = [
     "i live in india",
     "read a book",
     "finish my work",
     "i like my coffee cup"]

class LaunchRequestHandler(AbstractRequestHandler):
    """
    Handler for Skill Launch
    """
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        data = handler_input.attributes_manager.request_attributes["_"]
        speech = data["WELCOME_MSG"]
        reprompt = data["WELCOME_REPROMPT_MSG"]
        handler_input.response_builder.speak(speech).ask(reprompt)
        return handler_input.response_builder.response

class CreatePracticeHandler(AbstractRequestHandler):
    
    #Handler for Capturing the Birthday
    
    def can_handle(self, handler_input):
        return is_intent_name("CreatePracticeIntent")(handler_input)
    
    def handle(self, handler_input):
        data = handler_input.attributes_manager.request_attributes["_"]
        slots = handler_input.request_envelope.request.intent.slots
        topic = slots["topic"].value
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr['topic'] = topic
        
        speech = "Say start my session to proceed"
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response

class StartPracticeHandler(AbstractRequestHandler):
    
    #Handler for Capturing the Birthday
    
    def can_handle(self, handler_input):
        return is_intent_name("StartPracticeIntent")(handler_input)
    
    def handle(self, handler_input):
        data = handler_input.attributes_manager.request_attributes["_"]
        session_attr = handler_input.attributes_manager.session_attributes
        if "topic" not in session_attr:
            speech = data["TOPIC_MISSING_MSG"]
            handler_input.response_builder.speak(speech).ask(speech)
            return handler_input.response_builder.response
        
        topic = session_attr["topic"]
        practice_sentence_index = randint(0,len(PHRASES)-1)
        practice_sentence = PHRASES[practice_sentence_index]
        session_attr['practice_sentence'] = practice_sentence
        speech = data["START_PRACTICE_MSG"].format(practice_sentence)
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response

class ValidationHandler(AbstractRequestHandler):
    
    #Handler for Capturing the Birthday
    
    def can_handle(self, handler_input):
        return is_intent_name("ValidationIntent")(handler_input)
    
    def handle(self, handler_input):
        data = handler_input.attributes_manager.request_attributes["_"]
        slots = handler_input.request_envelope.request.intent.slots
        session_attr = handler_input.attributes_manager.session_attributes
        user_sentence = slots["sentence"].value
        practice_sentence = session_attr["practice_sentence"]
        
        if practice_sentence!=user_sentence:
            speech = data["VALIDATION_INCORRECT_USER_SENTENCE"].format(user_sentence, practice_sentence)
            handler_input.response_builder.speak(speech).ask(speech)
            return handler_input.response_builder.response
        else:
            speech = data["VALIDATION_CORRECT_USER_SENTENCE"]
            handler_input.response_builder.speak(speech).ask(speech)
            return handler_input.response_builder.response
"""        
class QuitContinueHandler(AbstractRequestHandler):
    
    #Handler for Capturing the Birthday
    
    def can_handle(self, handler_input):
        return is_intent_name("QuitContinueIntent")(handler_input)
    
    def handle(self, handler_input):
        data = handler_input.attributes_manager.request_attributes["_"]
        slots = handler_input.request_envelope.request.intent.slots
        user_response = slots["quit_continue"].value
        
        if user_response == "quit":
            speech = data["VALIDATION_INCORRECT_USER_SENTENCE"].format(practice_sentence)
            handler_input.response_builder.speak(speech).ask(speech)
            return handler_input.response_builder.response
        else:
            speech = data["VALIDATION_CORRECT_USER_SENTENCE"]
            handler_input.response_builder.speak(speech).ask(speech)
            return handler_input.response_builder.response
"""

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
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        data = handler_input.attributes_manager.request_attributes["_"]
        speak_output = data["GOODBYE_MSG"]

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
        

sb = CustomSkillBuilder(persistence_adapter=s3_adapter)

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CreatePracticeHandler())
sb.add_request_handler(StartPracticeHandler())
sb.add_request_handler(ValidationHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn’t override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

sb.add_global_request_interceptor(LocalizationInterceptor())


lambda_handler = sb.lambda_handler()