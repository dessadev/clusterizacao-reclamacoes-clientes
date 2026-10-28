"""Gera reclamações sintéticas de clientes de uma loja online, em português.

Os textos são simulados a partir de modelos de frase: nenhum dado real é usado.
"""
import numpy as np
import pandas as pd

CANAIS = ["android", "ios", "site", "whatsapp", "email", "telefone"]
TEMAS = {
    "cobranca_indevida": (["cobranca duplicada", "valor cobrado errado", "cobranca nao reconhecida", "estorno nao realizado", "taxa indevida"],
                          ["na fatura", "no cartao", "no boleto", "no pagamento", "na assinatura"]),
    "entrega": (["pedido atrasado", "entrega nao realizada", "produto extraviado", "rastreio parado", "entregue no endereco errado"],
                ["na entrega", "no frete", "na transportadora", "no prazo de entrega", "no rastreamento"]),
    "produto_defeito": (["produto com defeito", "item quebrado", "produto diferente do anunciado", "peca faltando", "produto nao funciona"],
                        ["na caixa", "no pedido recebido", "na embalagem", "no item comprado", "na compra"]),
    "app_travando": (["app travando", "tela em branco", "app fechando sozinho", "lentidao para carregar", "erro ao abrir"],
                     ["no aplicativo", "no celular", "na tela inicial", "no carrinho de compras", "na versao nova do app"]),
    "acesso_conta": (["nao consigo entrar", "senha nao aceita", "codigo de verificacao nao chega", "conta bloqueada", "erro de login"],
                     ["na minha conta", "no acesso", "no cadastro", "na verificacao em duas etapas", "no login"]),
    "atendimento": (["demora no atendimento", "sem resposta do suporte", "atendente nao resolveu", "protocolo sem retorno", "chat encerrado sem solucao"],
                    ["no atendimento", "no chat", "no sac", "no suporte", "na central de ajuda"]),
}
COMPLEMENTOS = ["", "", " ja reclamei antes", " preciso de ajuda", " pela segunda vez", " desde ontem", " muito insatisfeito", " urgente"]
RUIDO = ["elogio ao servico", "gostaria de uma informacao", "obrigado pela ajuda", "sugestao de melhoria",
         "quero falar com alguem", "mensagem enviada por engano", "acompanhando meu pedido", "favor retornar"]


def gerar_textos(n_por_tema=250, n_ruido=120, seed=3):
    rng = np.random.default_rng(seed)
    linhas = []
    for tema, modelos in TEMAS.items():
        sintomas, objetos = modelos
        for _ in range(n_por_tema):
            txt = f"{rng.choice(sintomas)} {rng.choice(objetos)} via {rng.choice(CANAIS)}" + rng.choice(COMPLEMENTOS)
            linhas.append((txt, tema))
    for _ in range(n_ruido):
        linhas.append((rng.choice(RUIDO) + rng.choice(COMPLEMENTOS), "ruido"))
    df = pd.DataFrame(linhas, columns=["descricao", "tema_real"])
    return df.sample(frac=1, random_state=seed).reset_index(drop=True)
