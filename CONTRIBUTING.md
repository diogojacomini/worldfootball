# Guia de Contribuição

Obrigado por considerar contribuir para o World Football Data Pipeline! 🎉

## Como Contribuir

### Reportando Bugs

Antes de reportar um bug, verifique se ele já não foi reportado. Se não foi, crie uma issue com:

- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs atual
- Screenshots (se aplicável)
- Informações do ambiente (SO, versão Python, etc.)

### Sugerindo Melhorias

Para sugerir melhorias:

- Use uma descrição clara e descritiva
- Explique por que essa melhoria seria útil
- Inclua exemplos de como a funcionalidade funcionaria

### Contribuindo com Código

1. **Fork** o repositório
2. **Clone** seu fork localmente
3. **Crie** uma branch para sua feature (`git checkout -b feature/nova-feature`)
4. **Configure** o ambiente de desenvolvimento
5. **Faça** suas mudanças
6. **Teste** suas mudanças
7. **Commit** suas mudanças com mensagens descritivas
8. **Push** para sua branch (`git push origin feature/nova-feature`)
9. **Abra** um Pull Request

## Configuração do Ambiente de Desenvolvimento

1. **Python 3.9+** é obrigatório
2. **Azure Functions Core Tools** v4
3. **Azure CLI** (opcional, mas recomendado)

```bash
# Clone o repositório
git clone https://github.com/diogojacomini/worldfootball.git
cd worldfootball

# Crie ambiente virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Instale dependências
pip install -r requirements.txt

# Configure settings locais
cp local.settings.json.example local.settings.json
# Edite local.settings.json com suas configurações
```

## Padrões de Código

- Use **PEP 8** para estilo Python
- Documente funções com **docstrings**
- Inclua **type hints** onde apropriado
- Escreva **testes** para novas funcionalidades
- Use **nomes descritivos** para variáveis e funções

### Exemplo de Função

```python
def extract_team_data(season: int, round_number: int) -> pd.DataFrame:
    """
    Extrai dados de times para uma temporada e rodada específicas.
    
    Args:
        season: Ano da temporada (ex: 2024)
        round_number: Número da rodada (1-38)
        
    Returns:
        DataFrame com dados dos times
        
    Raises:
        ValueError: Se parâmetros inválidos
        RequestException: Se falha na requisição
    """
    # implementação...
```

## Testes

Execute os testes antes de submeter:

```bash
# Testes unitários (quando implementados)
python -m pytest tests/

# Verificação de estilo
flake8 .

# Type checking
mypy .
```

## Estrutura de Commit

Use commits claros e descritivos:

```
tipo(escopo): descrição curta

Descrição mais detalhada se necessário.

- Lista de mudanças específicas
- Outra mudança importante
```

**Tipos de commit:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação, sem mudança de lógica
- `refactor`: Refatoração de código
- `test`: Adição/modificação de testes
- `chore`: Tarefas de manutenção

### Exemplos:
```
feat(extraction): adiciona suporte a múltiplas ligas
fix(api): corrige erro de serialização JSON
docs(readme): atualiza instruções de instalação
```

## Review Process

1. **Automated checks** devem passar (CI/CD)
2. **Code review** por mantenedores
3. **Testes** em ambiente de staging
4. **Merge** após aprovação

## Questões?

- Abra uma **issue** para discussões
- Entre em contato via **email** (se fornecido)
- Verifique a **documentação** existente

Obrigado por contribuir! 🚀
