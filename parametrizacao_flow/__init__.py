import logging
from azure.functions import HttpRequest, HttpResponse
from shared_code.functions import (get_current_year,
                                   get_current_round,
                                   get_current_date,
                                   upload_lake,
                                   check_prlm_sistema,)
from shared_code.variables import (CONTAINER_CONTROLE,
                                   CAMADA_RAW_NAME,
                                   STATUS_PARAMETRIZADO)


def main(req: HttpRequest) -> HttpResponse:
    sistema = req.headers.get('sistema'.upper())

    valid_parms = check_prlm_sistema(sistema)
    if valid_parms is not True:
        return valid_parms

    json_control = {
        'odate': get_current_date(),
        'sistema': sistema,
        'parm1': get_current_year(),
        'parm2': get_current_round(sistema, CAMADA_RAW_NAME) + 1,
        'status': STATUS_PARAMETRIZADO
    }
    upload_lake(json_control, f'{get_current_date()}_{sistema}_prlm.json', CONTAINER_CONTROLE, overwrite=True)

    return "OK"
