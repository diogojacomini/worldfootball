from azure.functions import HttpResponse
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from datetime import datetime
from pandas import read_csv
import logging
import json
import io
from shared_code.connection_az import AzureStore
from shared_code.variables import (COD_ERROR_PARAMETERS,
                                   CONNECTION_STRING,
                                   SISTEMAS,)

azure = AzureStore()


def check_prlm_temp_round(parm1, parm2):

    if not parm1 or not parm2:
        return HttpResponse("Parâmetros 'Temporada' e 'Rodada' são obrigatórios!", status_code=COD_ERROR_PARAMETERS)

    try:
        temporada = int(parm1)
        rodada = int(parm2)
    except ValueError:
        return HttpResponse("Parâmetros 'Temporada' e 'Rodada' devem ser números inteiros válidos.", status_code=COD_ERROR_PARAMETERS)

    if temporada <= 2003:
        return HttpResponse("A temporada deve ser maior que 2003.", status_code=COD_ERROR_PARAMETERS)

    if not (1 <= rodada <= 38):
        return HttpResponse("A rodada deve estar no intervalo de 1 a 38.", status_code=COD_ERROR_PARAMETERS)

    return True


def check_prlm_sistema(sistema):
    if not sistema:
        return HttpResponse("Parâmetro 'SISTEMA' é obrigatório!")

    if sistema not in SISTEMAS:
        return HttpResponse("Parâmetro 'SISTEMA' é inválido. Favor configurar com um dos sequintes sistemas: {0}".format(SISTEMAS))

    return True


def upload_lake(data, filename, container, overwrite=True):
    logging.info("upload_lake: output={} container={} overwrite={}".format(filename, container, overwrite))
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(container)
    blob_client = container_client.get_blob_client(filename)

    if filename.endswith('.csv'):
        file_up = data.to_csv(index=False)
    elif filename.endswith('.json'):
        file_up = json.dumps(data)
    else:
        logging.info("Warning! Tipo de arquivo diferente de csv ou json.")

    blob_client.upload_blob(file_up, overwrite=overwrite)

    logging.info("upload_lake: OK")


def read_lake(conteiner, filename):
    file_client = azure.get_file(conteiner, filename)
    try:
        data = file_client.download_blob()
        content = data.readall()

        if filename.endswith('.csv'):
            return read_csv(io.StringIO(content.decode('utf-8')))

        elif filename.endswith('.json'):
            return json.loads(content)
        else:
            logging.info("Warning! Tipo de arquivo diferente de csv ou json.")

    except Exception as error_read_lake:
        logging.info('ERROR: error_read_lake: {0}'.format(error_read_lake))


def get_current_year():
    return datetime.now().year


def get_current_date():
    return datetime.now().strftime("%Y%m%d")


def get_current_round(conteiner, layer):
    container_client = azure.get_container(conteiner)

    blob_list = container_client.list_blobs(f'{layer}/{get_current_year()}')

    logging.info('list: {0}'.format(blob_list))
    numero_de_arquivos = len(list(blob_list))
    logging.info('qtd: {0}'.format(numero_de_arquivos))
    return numero_de_arquivos
