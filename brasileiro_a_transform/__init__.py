import logging
from azure.functions import HttpRequest, HttpResponse
from shared_code.brasileirao_serie_a_etl import transform
from shared_code.functions import (read_lake,
                                   get_current_date,
                                   check_prlm_temp_round,
                                   upload_lake,)
from shared_code.variables import (CONTAINER_CONTROLE,
                                   PRLM_BRA_A,
                                   CAMADA_RAW_NAME,
                                   CAMADA_PR_NAME,
                                   CONTAINER_NAME_BRA_A,
                                   STATUS_CONLUSAO_TRANSFORM)


def main(req: HttpRequest) -> HttpResponse:

    # Parametros de entrada
    parameters = read_lake(CONTAINER_CONTROLE, f'{get_current_date()}_{PRLM_BRA_A}_prlm.json')
    parm1 = parameters.get('parm1')
    parm2 = parameters.get('parm2')

    valid_parms = check_prlm_temp_round(parm1, parm2)
    if valid_parms is not True:
        return valid_parms

    filename_input = '{0}/{1}/{1}{2:02}.csv'.format(CAMADA_RAW_NAME, parm1, parm2)
    filename_output = '{0}/{1}/{1}{2:02}.csv'.format(CAMADA_PR_NAME, parm1, parm2)

    # transform
    df = read_lake(CONTAINER_NAME_BRA_A, filename_input)
    df_processed = transform(df)

    # save on processed
    try:
        upload_lake(df_processed, filename_output, CONTAINER_NAME_BRA_A, overwrite=True)

    except Exception as error_insert:
        logging.info('Error: {0}'.format(error_insert))

    parameters['status'] = STATUS_CONLUSAO_TRANSFORM
    upload_lake(parameters, f'{get_current_date()}_{PRLM_BRA_A}_prlm.json', CONTAINER_CONTROLE, overwrite=True)

    return "OK"
