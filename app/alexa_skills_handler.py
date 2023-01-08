from ask_sdk_core.dispatch_components import AbstractRequestHandler
from os import environ
from alexa_client import AlexaClient, IntentReflectorHandler, CancelOrStopIntentHandler, SessionEndedRequestHandler, CatchAllExceptionHandler
import ask_sdk_core.utils as ask_utils
import json
import logging

_logger = logging.getLogger(__name__)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):       
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = "Welcome to the Watch Wizard. You can say 'recommend a movie'."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class GetDefenseMatchupsIntentHandler(AbstractRequestHandler):
    """Handler for Recommend Movie Intent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("GetDefenseMatchups")(handler_input)

    def handle(self, handler_input):
        message = "hello world"
        speak_output = message

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "You can ask me to recommend a movie"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

###############################

### Lambda functions start

_ALEXA_SKILL_ID = environ.get('AlexaSkillId')

# Configures and returns an AlexaClient
def get_alexa_client():
    # Creates AlexaClient and verifies configured skill_id matches incoming Alexa requests
    alexa_client = AlexaClient(_ALEXA_SKILL_ID)

    # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
    alexa_client.add_request_handlers([ LaunchRequestHandler(), GetDefenseMatchupsIntentHandler(), HelpIntentHandler(),
                                        CancelOrStopIntentHandler(), SessionEndedRequestHandler(), IntentReflectorHandler() ])

    alexa_client.add_exception_handler(CatchAllExceptionHandler())
    return alexa_client

def handle_skill_request(event, context):
    handler = get_alexa_client().get_lambda_handler()
    return handler(event, context)

def handle_api_request(event, context):
    handler = get_alexa_client().get_webservice_handler()
    response = handler.verify_request_and_dispatch(event['headers'], event['body'])
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }