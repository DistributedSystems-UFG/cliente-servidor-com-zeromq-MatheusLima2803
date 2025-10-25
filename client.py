# cliente.py
import zmq
import json
from const import ENDERECO_SERVIDOR

def enviar_requisicao(socket, operacao, argumentos=None):
    """Estrutura, envia a requisição ZeroMQ e processa a resposta."""
    if argumentos is None:
        argumentos = []
        
    # Estrutura a mensagem no formato de dicionário esperado pelo servidor
    dados_requisicao = {
        "operacao": operacao,
        "args": argumentos
    }
    
    # Serializa o dicionário para uma string JSON
    requisicao_str = json.dumps(dados_requisicao)
    
    print(f"\n[CLIENTE] Solicitando '{operacao}' com argumentos: {argumentos}")
    
    # Envia a solicitação (REQ)
    socket.send_string(requisicao_str)

    # Recebe a resposta (REP)
    resposta_str = socket.recv_string()
    
    # Deserializa a string JSON para um dicionário Python
    dados_resposta = json.loads(resposta_str)
    
    # Exibe o resultado ou erro
    if dados_resposta.get("status") == "sucesso":
        print(f"-> SUCESSO. Resultado: {dados_resposta['resultado']}")
    else:
        print(f"-> ERRO. Mensagem: {dados_resposta['mensagem']}")
    
    return dados_resposta

def iniciar_cliente():
    """Configura e executa o cliente ZeroMQ REQ (Request)."""
    contexto = zmq.Context()
    # O socket REQ é usado pelo lado "Cliente" no padrão REQ/REP
    socket = contexto.socket(zmq.REQ)
    # Conecta-se ao endereço do servidor
    socket.connect(ENDERECO_SERVIDOR)

    print(f"Cliente ZeroMQ (REQ) conectado ao {ENDERECO_SERVIDOR}")

    # --- DEMONSTRAÇÃO DAS CHAMADAS DOS SERVIÇOS ---

    # 1. Chamar o serviço 'somar'
    enviar_requisicao(socket, "somar", [35, 7]) 

    # 2. Chamar o serviço 'multiplicar'
    enviar_requisicao(socket, "multiplicar", [15, 6]) 

    # 3. Chamar o serviço 'dividir' (caso de sucesso)
    enviar_requisicao(socket, "dividir", [100, 25]) 

    # 4. Chamar o serviço 'dividir' (caso de ERRO de divisão por zero)
    enviar_requisicao(socket, "dividir", [50, 0]) 

    # 5. Chamar o serviço 'tamanho_string'
    enviar_requisicao(socket, "tamanho_string", ["Mensagem Distribuída"])

    # 6. Chamar uma operação desconhecida (erro de dispatcher no servidor)
    enviar_requisicao(socket, "inverter_texto", ["test"])


if __name__ == "__main__":
    iniciar_cliente()
