from shared_code.brasileirao_serie_a_etl import extract
from azure.functions import HttpRequest, HttpResponse
import logging
from time import sleep
from shared_code.functions import (check_prlm_temp_round,
                                   upload_lake,
                                   read_lake,
                                   get_current_year,
                                   refresh_status,
                                   get_current_round,
                                   get_current_date,)
from shared_code.variables import (PRLM_BRA_A,
                                   CONTAINER_CONTROLE,
                                   STATUS_INICIO,
                                   STATUS_INCOMPLETO_ERROR,
                                   COD_ERROR_PARAMETERS,
                                   CAMADA_RAW_NAME,
                                   CONTAINER_NAME_BRA_A,
                                   STATUS_CONCLUSAO_EXTRAC,
                                   STATUS_CONCLUSAO_FUNC,
                                   STATUS_INCOMPLETO_FUNC,
                                   STATUS_WARNING,
                                   STATUS_ERROR_UPLOAD)


def main(req: HttpRequest) -> HttpResponse:
    temporada_obs = get_current_year()
    filename_control = f'{get_current_date()}_{PRLM_BRA_A}_prlm.json'
    parameters = read_lake(container_name=CONTAINER_CONTROLE, filename=filename_control)

    # Parametros de entrada
    parm1 = parameters.get('parm1')
    parm2 = parameters.get('parm2')
    
    if  parameters.get('status') == STATUS_CONCLUSAO_EXTRAC:

        qtd_extraido = get_current_round(container_name=parameters.get('sistema'), layer=CAMADA_RAW_NAME, year=temporada_obs)
        
        if qtd_extraido == parameters.get('parm2'):
            logging.info("main extraction: Dados já foram extraidos..")
            return HttpResponse(status_code=STATUS_CONCLUSAO_FUNC)
        
        elif qtd_extraido == (parameters.get('parm2') - 1):
            logging.info("main extraction: Houve algum erro na extracao, realizando novamente..")
            refresh_status(control=parameters, filename=filename_control, status=STATUS_INICIO)
    
    if parameters.get('status') == STATUS_INICIO or parameters.get('status') == STATUS_ERROR_UPLOAD:
        valid, message = check_prlm_temp_round(parm1, parm2)
        if valid is not True:
            refresh_status(control=parameters, filename=filename_control, status=STATUS_INCOMPLETO_ERROR)
            return HttpResponse(message, status_code=COD_ERROR_PARAMETERS)

        logging.info('|=== Extrac - Campeonato Brasileiro Serie A ===|')
        logging.info('|       Temporada: {0}       Rodada: {1}       |'.format(parm1, parm2))

        # Incializa a estracao dos dados
        sleep(5)
        parm1, parm2 = int(parm1), int(parm2)
        df = extract(parm1, parm2)
        logging.info(df)
        filename_output = '{0}/{1}/{1}{2:02}.csv'.format(CAMADA_RAW_NAME, parm1, parm2)
        
        # Load dados brutos
        try:
            upload_lake(
                data=df,
                filename=filename_output,
                container_name=CONTAINER_NAME_BRA_A,
                overwrite=True
            )
            refresh_status(control=parameters, filename=filename_control, status=STATUS_CONCLUSAO_EXTRAC)
            return HttpResponse("OK") # return if ok
        
        except Exception as error_fun:
            refresh_status(control=parameters, filename=filename_control, status=STATUS_ERROR_UPLOAD)
            error_message = "Erro ao fazer upload: {0}".format(error_fun)
            logging.error(error_message.encode())  # Convertendo a mensagem em bytes
            return HttpResponse(status_code=STATUS_INCOMPLETO_FUNC)
