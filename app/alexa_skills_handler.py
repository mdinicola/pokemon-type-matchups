from ask_sdk_core.dispatch_components import AbstractRequestHandler
from alexa_client import AlexaClient, IntentReflectorHandler, CancelOrStopIntentHandler, SessionEndedRequestHandler, CatchAllExceptionHandler
from type_matchups import get_defense_matchups
from os import environ
import ask_sdk_core.utils as ask_utils
import json
import logging

_logger = logging.getLogger(__name__)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):       
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = "Welcome to Pokemon Type Matchups. You can say 'recommend a movie'."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class GetDefenseMatchupsIntentHandler(AbstractRequestHandler):
    """Handler for GetDefenseMatchups Intent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("GetDefenseMatchups")(handler_input)

    def handle(self, handler_input):
        slot_value = ask_utils.get_slot_value_v2(handler_input,'pokemonTypes')
        slot_values = list(map(lambda x: x.value, ask_utils.get_simple_slot_values(slot_value)))

        matchups = get_defense_matchups(slot_values)

        supereffective_matchups = list(map(lambda x: x.offense_type, filter(lambda y: y.effectiveness in [4, 2], matchups)))
        effective_matchups = list(map(lambda x: x.offense_type, filter(lambda y: y.effectiveness in [1], matchups)))
        noneffective_matchups = list(map(lambda x: x.offense_type, filter(lambda y: y.effectiveness in [0.25, 0.5], matchups)))

        message = f"Takes super effective damage from: {','.join(supereffective_matchups)}; "
        message += f"Takes normal damage from: {','.join(effective_matchups)}; "
        message += f"Resists: {','.join(noneffective_matchups)}"

        return (
            handler_input.response_builder
                .speak(message)
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

def handle_api_request(event, context):
    handler = get_alexa_client().get_webservice_handler()
    response = handler.verify_request_and_dispatch(event['headers'], event['body'])
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def handle_skill_request(event, context):
    handler = get_alexa_client().get_lambda_handler()
    return handler(event, context)