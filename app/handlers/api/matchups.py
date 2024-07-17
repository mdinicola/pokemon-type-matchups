from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.event_handler.openapi.params import Query
from aws_lambda_powertools.shared.types import Annotated
from aws_lambda_powertools.event_handler.openapi.exceptions import RequestValidationError, ValidationException

from http import HTTPStatus

from type_matchups import get_defense_matchups

logger = Logger()
app = APIGatewayRestResolver(enable_validation=True)

@app.exception_handler(Exception)
def handle_exception(e: Exception):
    logger.error(e)
    return Response(
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR,
        content_type = content_types.APPLICATION_JSON,
        body = {
            'error': {
                'msg': str(e)
            }
        }
    )

@app.exception_handler(RequestValidationError)
@app.exception_handler(ValidationException)
def handle_validation_error(e: ValidationException):
    logger.error(e.errors())
    return Response(
        status_code = HTTPStatus.BAD_REQUEST,
        content_type = content_types.APPLICATION_JSON,
        body = {
            'errors': e.errors()
        }
    )

def validate(pokemon_types: list[str]):
    if len(pokemon_types) > 2:
        raise ValidationException([{
            'type': 'too_many',
            'loc': ['query', 'type'],
            'msg': 'Too many values.  Only 1-2 types are allowed',
        }])

@app.get("/matchups/defense")
def get_defensive_matchups(pokemon_types: Annotated[list[str], Query(alias = 'type')]) -> dict:       
    validate(pokemon_types)
    matchups = get_defense_matchups(pokemon_types)
    response = {
        'meta': {
            'count': len(matchups)
        },
        'matchups': matchups
    }
    return response

def lambda_handler(event: dict, context: LambdaContext):
    return app.resolve(event, context)