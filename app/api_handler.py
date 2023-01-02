from json_encoders import EnhancedJSONEncoder
import json
import logging

_logger = logging.getLogger(__name__)

def handle_response(status_code, body):
    return {
            'statusCode': status_code,
            'body': body
        }

def example(event, context):
    try:
        response = {
            'data': 'hello world'
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