from azure.functions import HttpRequest, HttpResponse, Out
import logging
from shared_code.functions import (read_lake,
                                   get_current_date,
                                   check_prlm_temp_round,)
from shared_code.variables import (CONTAINER_CONTROLE,
                                   PRLM_BRA_A,
                                   CAMADA_PR_NAME,
                                   CONTAINER_NAME_BRA_A,)


def main(req: HttpRequest) -> HttpResponse:

    # Configuração da conexão com o banco de dados usando autenticação gerenciada
    server = 'servidortestes-dg.database.windows.net'
    database = 'worldfootball'
    driver = '{ODBC Driver 17 for SQL Server}'

    # Parametros de entrada
    parameters = read_lake(CONTAINER_CONTROLE, f'{get_current_date()}_{PRLM_BRA_A}_prlm.json')
    parm1 = parameters.get('parm1')
    parm2 = parameters.get('parm2')

    valid_parms = check_prlm_temp_round(parm1, parm2)
    if valid_parms != True:
        return valid_parms

    filename_input = '{0}/{1}/{1}{2:02}.csv'.format(CAMADA_PR_NAME, parm1, parm2)
    df = read_lake(CONTAINER_NAME_BRA_A, filename_input)
    logging.info(df)
    return "OK"
