import logging
from azure.functions import HttpRequest, HttpResponse
from shared_code.brasileirao_serie_a_etl import transform
from shared_code.functions import (read_lake,
                                   get_current_date,
                                   check_prlm_temp_round,
                                   upload_lake,
                                   refresh_status,)
from shared_code.variables import (CONTAINER_CONTROLE,
                                   PRLM_BRA_A,
                                   CAMADA_RAW_NAME,
                                   CAMADA_PR_NAME,
                                   CONTAINER_NAME_BRA_A,
                                   STATUS_CONLUSAO_TRANSFORM,
                                   STATUS_CONCLUSAO_EXTRAC,
                                   STATUS_ERROR_UPLOAD,
                                   STATUS_CONCLUSAO_FUNC,
                                   STATUS_INCOMPLETO_FUNC)


def main(req: HttpRequest) -> HttpResponse:

    # Parametros de entrada
    filename_control = f'{get_current_date()}_{PRLM_BRA_A}_prlm.json'
    parameters = read_lake(container_name=CONTAINER_CONTROLE, filename=filename_control)
    
    parm1 = parameters.get('parm1')
    parm2 = parameters.get('parm2')

    filename_input = '{0}/{1}/{1}{2:02}.csv'.format(CAMADA_RAW_NAME, parm1, parm2)
    filename_output = '{0}/{1}/{1}{2:02}.csv'.format(CAMADA_PR_NAME, parm1, parm2)

    
    if parameters.get('status') == STATUS_CONCLUSAO_EXTRAC or parameters.get('status') == STATUS_ERROR_UPLOAD:
        valid, message = check_prlm_temp_round(parm1, parm2)
        if valid is not True:
            refresh_status(control=parameters, filename=filename_control, status=STATUS_INCOMPLETO_ERROR)
            return HttpResponse(message, status_code=COD_ERROR_PARAMETERS)

        logging.info('|=== Transform - Campeonato Brasileiro Serie A ===|')
        logging.info('|       Temporada: {0}       Rodada: {1}       |'.format(parm1, parm2))

        # transform
        df = read_lake(CONTAINER_NAME_BRA_A, filename_input)
        df_processed = transform(df)

        try:
            upload_lake(
                data=df_processed,
                filename=filename_output,
                container_name=CONTAINER_NAME_BRA_A,
                overwrite=True
            )
            refresh_status(control=parameters, filename=filename_control, status=STATUS_CONLUSAO_TRANSFORM)
            return HttpResponse("OK")
        
        except Exception as error_fun:
            refresh_status(control=parameters, filename=filename_control, status=STATUS_ERROR_UPLOAD)
            error_message = "Erro ao fazer upload: {0}".format(error_fun)
            logging.error(error_message.encode())  # Convertendo a mensagem em bytes
            return HttpResponse(status_code=STATUS_INCOMPLETO_FUNC)
