import logging
from shared_code.variables import CONTAINER_NAME_BRA_A, CAMADA_CR_NAME
from shared_code.functions import read_lake

from azure.functions import HttpRequest, HttpResponse


def main(req: HttpRequest) -> HttpResponse:
    filename_output = '{0}/campeonato_brasileiro.csv'.format(CAMADA_CR_NAME)
    df = read_lake(CONTAINER_NAME_BRA_A, filename_output)
    json_data = df.to_json(orient='records')

    return HttpResponse(json_data)
