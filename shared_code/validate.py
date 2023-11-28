import jwt
from shared_code.variables import TOKEN

def validate_jwt(token):
    try:
        decoded = jwt.decode(token, TOKEN, algorithms=['HS256'])
        return decoded
    except jwt.ExpiredSignatureError:
        # Token expirado
        return {"error": "Token expirado"}
    except jwt.InvalidTokenError:
        # Token inválido
        return {"error": "Token inválido"}
    except jwt.DecodeError:
        # Erro de decodificação
        return {"error": "Erro de decodificação do token"}
    except jwt.InvalidAlgorithmError:
        # Algoritmo inválido
        return {"error": "Algoritmo de token inválido"}
    except Exception as e:
        # Lidar com outros erros inesperados
        return {"error": f"Erro inesperado: {str(e)}"}