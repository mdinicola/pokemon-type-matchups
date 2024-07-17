from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.event_handler.openapi.params import Query
from aws_lambda_powertools.shared.types import Annotated
from aws_lambda_powertools.event_handler.openapi.exceptions import RequestValidationError

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
def handle_validation_error(e: RequestValidationError):
    logger.error(e.errors())
    return Response(
        status_code = HTTPStatus.BAD_REQUEST,
        content_type = content_types.APPLICATION_JSON,
        body = {
            'errors': e.errors()
        }
    )

@app.get("/matchups/defense")
def get_defensive_matchups(pokemon_types: Annotated[list[str], Query(alias = 'type')]) -> dict:       
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