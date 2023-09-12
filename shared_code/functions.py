from azure.functions import HttpResponse
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from pandas import read_csv, DataFrame
from datetime import datetime
import logging
import json
import io
from shared_code.connection_az import AzureStore
from shared_code.variables import SISTEMAS, CONTAINER_CONTROLE

azure = AzureStore()


def check_prlm_temp_round(parm1, parm2):
    """
    Valida os parâmetros de temporada e rodada.

    Args:
        parm1 (str): O valor da temporada a ser validado.
        parm2 (str): O valor da rodada a ser validado.

    Returns:
        tuple: Uma tupla contendo um valor booleano que indica se a validação foi bem-sucedida
               e uma mensagem de erro, se aplicável. 
    """
    if not parm1 or not parm2:
        return False, "check_prlm_temp_round: Parâmetros 'Temporada' e 'Rodada' são obrigatórios!"

    try:
        temporada = int(parm1)
        rodada = int(parm2)
    except ValueError:
        return False, "check_prlm_temp_round: Parâmetros 'Temporada' e 'Rodada' devem ser números inteiros válidos."

    if temporada < 2003:
        return False, "check_prlm_temp_round: A temporada deve ser maior ou igual a 2003."

    if not (1 <= rodada <= 38):
        return False, "check_prlm_temp_round: A rodada deve estar no intervalo de 1 a 38."

    return True, None


def check_prlm_sistema(sistema):
    """
    Verifica se o parâmetro 'sistema' é válido.

    Args:
        sistema (str): O sistema a ser verificado.

    Returns:
        bool: True se o sistema for válido, caso contrário, retorna uma mensagem de erro.
    """
    if not sistema:
        return False, "check_prlm_sistema: Parâmetro 'SISTEMA' é obrigatório!"

    if sistema not in SISTEMAS:
        return False, f"check_prlm_sistema: Parâmetro 'SISTEMA' é inválido. Favor " \
                       "configurar com um dos seguintes sistemas: {0}".format(', '.join(SISTEMAS))

    return True, None


def upload_lake(data, filename, container_name, overwrite=True):
    """
    Faz o upload de dados para um contêiner no Azure Blob Storage.

    Args:
        data: Os dados a serem carregados, que podem ser um DataFrame do Pandas ou um dicionário.
        filename (str): O nome do arquivo no qual os dados serão salvos no Blob Storage.
        container_name (str): O nome do contêiner no Azure Blob Storage.
        overwrite (bool, optional): Se True, o arquivo será substituído se já existir no Blob Storage. Padrão é True.

    Raises:
        ValueError: Se o tipo de arquivo não é suportado (apenas '.csv' e '.json' são suportados).
    
    Exemplo: upload_lake(dataset, 'example.csv', 'my-container')
    """
    logging.info(f"upload_lake: Uploading {filename} to container {container_name}, overwrite={overwrite}")
    blob_client = azure.get_container(container_name).get_blob_client(filename)

    if filename.endswith('.csv'):
        file_content = data.to_csv(index=False, encoding='utf-8').encode('utf-8')

    elif filename.endswith('.json'):
        file_content = json.dumps(data)
    else:
        logging.info("upload_lake: !Warning! tipo do arquivo .{0} ".format(filename.split(".")[-1]))
        raise ValueError("Unsupported file type. Only '.csv' and '.json' are supported.")

    blob_client.upload_blob(file_content, overwrite=overwrite)
    logging.info("upload_lake: Upload successful")


def read_lake(container_name, filename):
    """
    Lê um arquivo de um contêiner no Azure Blob Storage.

    Args:
        container_name (str): O nome do contêiner no Azure Blob Storage.
        filename (str): O nome do arquivo a ser lido.

    Returns:
        DataFrame or dict or None: Os dados lidos do arquivo, dependendo do tipo do arquivo.
                                   Retorna None em caso de erro.
    """
    file_client = azure.get_file(container_name, filename)
    try:
        data = file_client.download_blob()
        content = data.readall()

        if filename.endswith('.csv'):
            return read_csv(io.StringIO(content.decode('utf-8')))

        elif filename.endswith('.json'):
            return json.loads(content)
        else:
            logging.warning("read_lake: Warning! Tipo de arquivo diferente de csv ou json.")
            logging.warning("Se novo tipo de arquivo for adicionado, é preciso atualizar a function: read_lake")

    except Exception as error_read_lake:
        logging.error('read_lake: error_read_lake: {0}'.format(str(error_read_lake)))
        return None

def get_current_year() -> int:
    """Retorna o ano atual."""
    return datetime.now().year


def get_current_date() -> int:
    """Retorna a data atual no formato 'AAAAMMDD'."""
    return datetime.now().strftime("%Y%m%d")


def get_current_round(container_name, layer, year) -> int:
    """
    Retorna o número de arquivos em um diretório específico dentro de um contêiner no Azure Blob Storage.

    Args:
        container_name (str): O nome do contêiner no Azure Blob Storage.
        layer (str): A camada (ou diretório) dentro do contêiner (raw, processed).
        year (str): O ano a ser verificado dentro da camada.
    """
    try:
        container_client = azure.get_container(container_name)
        file_count = len(list(container_client.list_blobs(name_starts_with=f'{layer}/{year}')))

        logging.info('get_current_round: Número de arquivos em {0}/{1}/{2}: {3}'.format(container_name, layer, year, file_count))
        return file_count
    
    except Exception as eror_round:
        logging.error("get_current_round: Erro ao contar arquivos: {0}".format(str(eror_round)))
        return -1

def refresh_status(control, filename, status):
    """Atualiza o status do controle no Azure Blob Storage."""
    control['status'] = status
    upload_lake(
            data=control,
            filename=filename,
            container_name=CONTAINER_CONTROLE,
            overwrite=True
        )

def list_files(container_name, layer):
    container_client = azure.get_container(container_name)
    list_dict_files = list(container_client.list_blobs(name_starts_with=f'{layer}'))
    lista_de_nomes = [d.get('name') for d in list_dict_files]
    
    return list(map(lambda nome_arquivo: read_lake(container_name, nome_arquivo), lista_de_nomes))