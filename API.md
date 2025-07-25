# Documentação da API

## Visão Geral

A API do World Football fornece acesso aos dados consolidados do Campeonato Brasileiro Série A através de endpoints REST.

## Base URL

```
https://fnt-worldfoot-de.azurewebsites.net
```

## Endpoints

### GET /api/getwf

Retorna os dados consolidados da tabela do Campeonato Brasileiro.

**Resposta de Sucesso:**

```json
[
  {
    "posicao": 1,
    "time": "Flamengo",
    "rodada": 38,
    "vitoria": 25,
    "empate": 8,
    "derrota": 5,
    "gols": 68,
    "gols_sofridos": 42,
    "diferenca_gols": 26,
    "pontos": 83,
    "temporada": 2024
  }
]
```

**Campos de Resposta:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `posicao` | integer | Posição atual do time na tabela |
| `time` | string | Nome do time |
| `rodada` | integer | Número da rodada atual |
| `vitoria` | integer | Total de vitórias |
| `empate` | integer | Total de empates |
| `derrota` | integer | Total de derrotas |
| `gols` | integer | Total de gols marcados |
| `gols_sofridos` | integer | Total de gols sofridos |
| `diferenca_gols` | integer | Diferença entre gols marcados e sofridos |
| `pontos` | integer | Total de pontos acumulados |
| `temporada` | integer | Ano da temporada |

## Códigos de Status

| Código | Descrição |
|--------|-----------|
| 200 | Sucesso |
| 404 | Dados não encontrados |
| 500 | Erro interno do servidor |

## Exemplos de Uso

### JavaScript (Fetch API)

```javascript
fetch('https://fnt-worldfoot-de.azurewebsites.net/api/getwf')
  .then(response => response.json())
  .then(data => {
    console.log('Tabela do Brasileirão:', data);
  })
  .catch(error => {
    console.error('Erro:', error);
  });
```

### Python (requests)

```python
import requests

response = requests.get('https://fnt-worldfoot-de.azurewebsites.net/api/getwf')
data = response.json()

for time in data:
    print(f"{time['posicao']}° - {time['time']} - {time['pontos']} pts")
```

### cURL

```bash
curl -X GET "https://fnt-worldfoot-de.azurewebsites.net/api/getwf" \
     -H "Accept: application/json"
```

## Rate Limiting

Atualmente não há limitação de taxa, mas recomendamos não fazer mais de 60 requisições por minuto.

## Suporte

Para suporte ou dúvidas sobre a API, abra uma issue no [repositório GitHub](https://github.com/diogojacomini/worldfootball/issues).
