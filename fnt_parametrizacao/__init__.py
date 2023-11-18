import logging
from azure.functions import HttpRequest, HttpResponse
from shared_code.functions import (get_current_year,
                                   get_current_round,
                                   get_current_date,
                                   upload_lake,
                                   check_prlm_sistema,
                                   check_prlm_temp_round,)
from shared_code.variables import (CONTAINER_CONTROLE,
                                   CAMADA_RAW_NAME,
                                   STATUS_INICIO,
                                   STATUS_CONCLUSAO_FUNC,
                                   STATUS_INCOMPLETO_FUNC,
                                   COD_ERROR_PARAMETERS,)


def main(req: HttpRequest) -> HttpResponse:
    """Função principal que faz o controle das arquiteturas ETL dos sistemas."""
    sistema = req.headers.get('sistema'.upper())

    if req.headers.get('loop'.upper()):
        temporada_obs = int(req.headers.get('loop'.upper()))
    else:
        temporada_obs = get_current_year()

    valid, message = check_prlm_sistema(sistema)
    if valid is not True:
        return HttpResponse(message, status_code=COD_ERROR_PARAMETERS)

    control_data = {
        'odate': get_current_date(),
        'sistema': sistema,
        'parm1': temporada_obs,
        'parm2': get_current_round(container_name=sistema, layer=CAMADA_RAW_NAME, year=temporada_obs) + 1,
        'status': STATUS_INICIO
    }

    valid, message = check_prlm_temp_round(control_data.get('parm1'), control_data.get('parm2'))
    if valid is not True:
        return HttpResponse(message, status_code=COD_ERROR_PARAMETERS)

    try:
        upload_lake(
            data=control_data,
            filename=f'{get_current_date()}_{sistema}_prlm.json',
            container_name=CONTAINER_CONTROLE,
            overwrite=True
        )
        return HttpResponse("OK")
    
    except Exception as error_fun:
        logging.error(f"main (error_fun): Erro ao fazer upload do JSON de controle: {str(error_fun)}")
        return HttpResponse(status_code=STATUS_INCOMPLETO_FUNC)
