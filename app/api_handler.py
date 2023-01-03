from json_encoders import EnhancedJSONEncoder
from type_matchups import get_defense_matchups
import json
import logging

_logger = logging.getLogger(__name__)

def handle_response(status_code, body):
    return {
            'statusCode': status_code,
            'body': body
        }

def get_defensive_matchups(event, context):
    try:
        query_parameters = event.get('queryStringParameters', None)
        if query_parameters is None:
            raise RuntimeError("Types are required")
        types = list(filter(None, query_parameters.get('types', '').split(' ')))
        matchups = get_defense_matchups(types)
        response = {
            'meta': {
                'count': len(matchups)
            },
            'data': matchups
        }
        return handle_response(200, json.dumps(response, cls=EnhancedJSONEncoder))
    except Exception as e:
        _logger.exception(e)
        message = 'An unexpected error ocurred.  See log for details.'
        response = {
            'error': {
                'message': message
            }
        }
        return handle_response(500, json.dumps(response))