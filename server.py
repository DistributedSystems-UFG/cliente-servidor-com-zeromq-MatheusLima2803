# servidor.py
import zmq
import time
import json
# Importa a constante de endereço
from const import ENDERECO_SERVIDOR

# --- NOVOS SERVIÇOS (Funcionalidades) ---

def somar(a, b):
    """Realiza a soma de dois números."""
    return a + b

def multiplicar(a, b):
    """Realiza a multiplicação de dois números."""
    return a * b

def dividir(a, b):
    """Divide dois números, com tratamento para divisão por zero."""
    if b == 0:
        # Lança um erro que será capturado e enviado ao cliente
        raise ValueError("ERRO: Divisão por zero não permitida.")
    return a / b

def calcular_tamanho_string(texto):
    """Calcula o tamanho (em caracteres) de uma string."""
    # Garante que o argumento é tratado como string
    return len(str(texto))

# Mapeamento de nome da operação (string) para a função real (objeto)
SERVICOS = {
    "somar": somar,
    "multiplicar": multiplicar,
    "dividir": dividir,
    "tamanho_string": calcular_tamanho_string
}

# --- LÓGICA DE PROCESSAMENTO DO SERVIDOR ---

def processar_requisicao(requisicao_json):
    """Processa a solicitação JSON do cliente, despacha para a função apropriada."""
    try:
        # Deserializa a string JSON para um dicionário Python
        dados = json.loads(requisicao_json)
        operacao = dados.get("operacao")
        # Pega a lista de argumentos. Se 'args' não existir, usa uma lista vazia.
        argumentos = dados.get("args", [])

        if operacao not in SERVICOS:
            return {"status": "erro", "mensagem": f"Operação desconhecida: {operacao}"}
        
        # Obtém a função a ser executada
        funcao = SERVICOS[operacao]
        
        # Chama a função usando os argumentos desempacotados
        resultado = funcao(*argumentos)
        
        # Retorna uma resposta de sucesso no formato de dicionário
        return {"status": "sucesso", "operacao": operacao, "resultado": resultado}

    except json.JSONDecodeError:
        return {"status": "erro", "mensagem": "Formato da requisição JSON é inválido."}
    except ValueError as ve:
        # Captura erros lançados pelas funções (ex: Divisão por zero)
        return {"status": "erro", "mensagem": str(ve)}
    except TypeError:
        # Captura erros se o número ou tipo de argumentos for incorreto
        return {"status": "erro", "mensagem": "Argumentos incorretos para a operação especificada."}
    except Exception as e:
        # Captura outros erros inesperados
        return {"status": "erro", "mensagem": f"Erro de processamento inesperado no servidor: {e}"}


def iniciar_servidor():
    """Configura e inicia o servidor ZeroMQ REP (Reply)."""
    contexto = zmq.Context()
    # O socket REP é usado pelo lado "Servidor" no padrão REQ/REP
    socket = contexto.socket(zmq.REP)
    
    # Obtém a porta do endereço configurado (ex: "tcp://127.0.0.1:5555" -> "5555")
    porta = ENDERECO_SERVIDOR.split(':')[-1]
    # Vincula o socket a todas as interfaces (*) na porta especificada
    endereco_vinculacao = f"tcp://*:{porta}"
    socket.bind(endereco_vinculacao)

    print(f"Servidor ZeroMQ (REP) rodando em {endereco_vinculacao}. Aguardando requisições...")

    while True:
        # Recebe a mensagem (string) da requisição
        mensagem_str = socket.recv_string()

        # Processa a requisição
        dados_resposta = processar_requisicao(mensagem_str)

        # Simula um pequeno tempo de processamento
        time.sleep(0.1)

        # Serializa o dicionário de resposta para string JSON
        resposta_str = json.dumps(dados_resposta)
        # Envia a resposta de volta ao cliente
        socket.send_string(resposta_str)

if __name__ == "__main__":
    iniciar_servidor()
