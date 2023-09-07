import logging
from azure.functions import HttpRequest, HttpResponse
from shared_code.brasileirao_serie_a_etl import extract
from shared_code.functions import check_prlm_temp_round, upload_lake, read_lake, get_current_date
from shared_code.variables import CONTAINER_NAME_BRA_A, CAMADA_RAW_NAME, CONTAINER_CONTROLE, PRLM_BRA_A, STATUS_CONCLUSAO_EXTRAC
from time import sleep

def main(req: HttpRequest) -> HttpResponse:
    parameters = read_lake(CONTAINER_CONTROLE, f'{get_current_date()}_{PRLM_BRA_A}_prlm.json')

    # Parametros de entrada
    parm1 = parameters.get('parm1') #req.params.get('parm1'.upper())
    parm2 = parameters.get('parm2') #req.params.get('parm2'.upper())

    valid_parms = check_prlm_temp_round(parm1, parm2)
    if valid_parms != True:
        return valid_parms
    
    logging.info('|= Extrac - Campeonato Brasileiro Serie A =|')
    logging.info('| Temporada: {0}      Rodada: {1}           |'.format(parm1, parm2))    

    # Incializa a estracao dos dados
    sleep(5)
    parm1, parm2 = int(parm1), int(parm2)
    df = extract(parm1, parm2)

    # Load dados brutos
    try:
       upload_lake(df, '{0}/{1}/{1}{2:02}.csv'.format(CAMADA_RAW_NAME, parm1, parm2), CONTAINER_NAME_BRA_A, overwrite=True)

    except Exception as error_insert:
        logging.info('Error: {0}'.format(error_insert))

    parameters['status'] = STATUS_CONCLUSAO_EXTRAC
    upload_lake(parameters, f'{get_current_date()}_{PRLM_BRA_A}_prlm.json', CONTAINER_CONTROLE, overwrite=True)


    return "OK"
