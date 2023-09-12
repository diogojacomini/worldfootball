# sistemas
SISTEMAS = [
    'campeonato-brasileiro'
]

# utils
URL = 'https://www.worldfootball.net'
HEADER = {'User-Agent': 'Mozilla/5.0'}

# codigos de resposta de erro
COD_ERROR_PARAMETERS = 23  # para erros de parametro

# STORE
CONNECTION_STRING = "DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=worldfootballrepo;AccountKey=P0LCNpIcHOfYGSKi4TVzv+3pfSmevdE9PVaAzaJi/p0cZJZtgSWSPHrcVRVe0chKB1y3aLl2VxW/+ASt1i9YsQ==;BlobEndpoint=https://worldfootballrepo.blob.core.windows.net/;FileEndpoint=https://worldfootballrepo.file.core.windows.net/;QueueEndpoint=https://worldfootballrepo.queue.core.windows.net/;TableEndpoint=https://worldfootballrepo.table.core.windows.net/"
LOAD_OPTIONS = 'lake'

# Containers
CONTAINER_NAME_BRA_A = 'campeonato-brasileiro'
CONTAINER_CONTROLE = 'controle'

# Parametro de sistemas
PRLM_BRA_A = 'campeonato-brasileiro'

# Camadas de dados
CAMADA_RAW_NAME = 'raw'
CAMADA_PR_NAME = 'processed'
CAMADA_CR_NAME = 'curated'

# Status de execucao
STATUS_INICIO = 'IN' # Pronto para a proxima etapa!
STATUS_CONCLUSAO_EXTRAC = 'OKE'
STATUS_CONLUSAO_TRANSFORM = 'OKT'
STATUS_CONLUSAO_LOAD = 'OKL'
STATUS_INCOMPLETO_ERROR = 'ERROR'
STATUS_WARNING = 'WARNING'
STATUS_ERROR_UPLOAD = 'ERUP' # Falha no upload, pode tentar novamente.
STATUS_CONCLUSAO_FUNC = 1
STATUS_INCOMPLETO_FUNC = 2

