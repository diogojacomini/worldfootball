# World Football Data Pipeline ⚽

Um pipeline de dados completo para extração, transformação e carregamento de dados do Campeonato Brasileiro Série A, implementado com Azure Functions e Python.

## 🏗️ Arquitetura

Este projeto implementa uma arquitetura ETL moderna usando Azure Functions serverless para processar dados de futebol em tempo real:

```
[worldfootball.net] → [Azure Functions] → [Azure Blob Storage] → [API REST]
```

### Componentes Principais

- **`fnt_extraction`**: Extração de dados da worldfootball.net
- **`fnt_transformation`**: Transformação e limpeza dos dados
- **`fnt_load`**: Carregamento para storage definitivo
- **`getwf`**: API REST para consulta dos dados processados
- **`fnt_parametrizacao`**: Configuração e parametrização do pipeline

## 🚀 Funcionalidades

- ✅ Extração automatizada de dados do Brasileirão Série A
- ✅ Pipeline ETL completo com controle de status
- ✅ API REST para consulta de dados consolidados
- ✅ Armazenamento em camadas (Raw, Processed, Curated)
- ✅ Controle de execução e retry automático
- ✅ Deploy automatizado via GitHub Actions
- ✅ Monitoramento e logging detalhado

## 📊 Dados Extraídos

O pipeline coleta e processa:
- Posição na tabela
- Nome dos times
- Estatísticas por rodada (vitórias, empates, derrotas)
- Gols marcados e sofridos
- Diferença de gols
- Pontuação total
- Dados históricos por temporada

## 🛠️ Stack Tecnológica

- **Python 3.9+** - Linguagem principal
- **Azure Functions** - Computação serverless
- **Azure Blob Storage** - Data Lake
- **Pandas** - Processamento de dados
- **Requests + lxml** - Web scraping
- **GitHub Actions** - CI/CD

## 📁 Estrutura do Projeto

```
worldfootball/
├── fnt_extraction/          # Função de extração
├── fnt_transformation/      # Função de transformação  
├── fnt_load/               # Função de carregamento
├── fnt_parametrizacao/     # Função de parametrização
├── getwf/                  # API REST
├── shared_code/            # Código compartilhado
│   ├── brasileirao_serie_a_etl/  # Lógica ETL específica
│   ├── functions.py        # Funções utilitárias
│   ├── variables.py        # Configurações e constantes
│   └── connection_az.py    # Conexões Azure
├── .github/workflows/      # Pipelines CI/CD
├── requirements.txt        # Dependências Python
└── host.json              # Configuração Azure Functions
```

## ⚙️ Configuração e Deploy

### Pré-requisitos
- Python 3.9+
- Azure CLI
- Azure Functions Core Tools
- Conta Azure com Blob Storage

### Setup Local

1. **Clone o repositório:**
```bash
git clone https://github.com/diogojacomini/worldfootball.git
cd worldfootball
```

2. **Crie e ative o ambiente virtual:**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente:**
Crie um arquivo `local.settings.json`:
```json
{
    "IsEncrypted": false,
    "Values": {
        "AzureWebJobsStorage": "UseDevelopmentStorage=true",
        "FUNCTIONS_WORKER_RUNTIME": "python"
    }
}
```

5. **Execute localmente:**
```bash
func start
```

### Deploy para Azure

O projeto está configurado com CI/CD automático via GitHub Actions. Push para as branches `main` ou `develop` dispara o deploy automaticamente.

**Deploy manual:**
```bash
func azure functionapp publish <nome-da-function-app>
```

## 🔄 Fluxo de Execução

1. **Parametrização**: Define temporada e rodada a serem processadas
2. **Extração**: Coleta dados da worldfootball.net
3. **Transformação**: Limpa e estrutura os dados
4. **Carregamento**: Armazena na camada curated
5. **API**: Disponibiliza dados via endpoint REST

## 📡 Endpoints da API

- **GET** `/api/getwf` - Retorna dados consolidados do Brasileirão

## 🧪 Testes e Monitoramento

- Logs detalhados em cada etapa do pipeline
- Controle de status para retry automático
- Validação de parâmetros de entrada
- Monitoramento via Azure Application Insights

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🔗 Links Úteis

- [Azure Functions Documentation](https://learn.microsoft.com/pt-br/azure/azure-functions/)
- [Azure Functions Core Tools](https://learn.microsoft.com/pt-br/azure/azure-functions/functions-core-tools-reference)
- [World Football](https://www.worldfootball.net/)

---

**Desenvolvido por:** [Diogo Jacomini](https://github.com/diogojacomini)  
**Última atualização:** Julho 2025