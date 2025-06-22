from flask import current_app
import jwt

def verificar_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
class PilhaLivros:
    def __init__(self):
        self.itens = []

    def push(self, livro):
        self.itens.append(livro)

    def pop(self):
        if not self.is_empty():
            return self.itens.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.itens[-1]
        return None

    def is_empty(self):
        return len(self.itens) == 0

    def tamanho(self):
        return len(self.itens)

    def listar(self):
        return list(reversed(self.itens))  
