from azure.functions import HttpRequest, HttpResponse, Out
import logging
from shared_code.brasileirao_serie_a_etl import load
from shared_code.functions import (read_lake,
                                   get_current_date,
                                   check_prlm_temp_round,
                                   list_files,
                                   refresh_status,
                                   upload_lake)
from shared_code.variables import (CONTAINER_CONTROLE,
                                   PRLM_BRA_A,
                                   CAMADA_PR_NAME,
                                   CONTAINER_NAME_BRA_A,
                                   CAMADA_CR_NAME,
                                   STATUS_CONCLUSAO_FUNC,
                                   STATUS_CONLUSAO_LOAD,
                                   STATUS_ERROR_UPLOAD,
                                   STATUS_INCOMPLETO_FUNC)

from shared_code.connection_az import AzureStore
from pandas import concat

def main(req: HttpRequest) -> HttpResponse:
    
    # Parametros de entrada
    filename_control = f'{get_current_date()}_{PRLM_BRA_A}_prlm.json'
    parameters = read_lake(container_name=CONTAINER_CONTROLE, filename=filename_control)

    filenames_input = list_files(container_name=CONTAINER_NAME_BRA_A, layer=CAMADA_PR_NAME)
    filename_output = '{0}/campeonato_brasileiro.csv'.format(CAMADA_CR_NAME)
        
    logging.info('|=== Load - Campeonato Brasileiro Serie A ===|')
    logging.info('|       output: {0}       |'.format(filename_output))

    df_load = load(mode='lake', files=filenames_input, file=None)
        
    try:
        upload_lake(
            data=df_load,
            filename=filename_output,
            container_name=CONTAINER_NAME_BRA_A,
            overwrite=True
        )
        refresh_status(control=parameters, filename=filename_control, status=STATUS_CONLUSAO_LOAD)
        return HttpResponse("OK")
        
    except Exception as error_fun:
        refresh_status(control=parameters, filename=filename_control, status=STATUS_ERROR_UPLOAD)
        error_message = "Erro ao fazer upload: {0}".format(error_fun)
        logging.error(error_message.encode())  # Convertendo a mensagem em bytes
        return HttpResponse(status_code=STATUS_INCOMPLETO_FUNC)