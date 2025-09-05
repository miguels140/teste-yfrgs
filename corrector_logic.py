from transformers import pipeline
import random

# Configuração do modelo de IA para correção e similaridade.
# Para análise de similaridade, um modelo de "sentence-transformers" seria ideal.
# Para simplificar, vamos usar um modelo de classificação genérico.
try:
    corrector_pipeline = pipeline("text-classification", model="unitary/toxic-bert", device=-1)
    
    # Modelo para verificação de relevância do tema (simulação)
    relevance_pipeline = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst2-english", device=-1)
except Exception as e:
    print(f"Não foi possível carregar o modelo de IA. Verifique as dependências. Erro: {e}")
    corrector_pipeline = None
    relevance_pipeline = None

def corrigir_redacao(texto_redacao, tema_redacao):
    """
    Função principal que simula a correção da redação, incluindo a verificação de tema.
    """
    linhas = texto_redacao.split('\n')
    num_linhas = len(linhas)
    min_linhas_ufrgs = 30
    max_linhas_ufrgs = 45

    if num_linhas < min_linhas_ufrgs:
        return {
            "mensagem": f"Sua redação tem {num_linhas} linhas. O mínimo exigido é de {min_linhas_ufrgs} linhas.",
            "nota": 0,
            "erros_ia": [],
            "acertos_competencia": {},
            "relevancia_tema": "Baixa"
        }
    if num_linhas > max_linhas_ufrgs:
        return {
            "mensagem": f"Sua redação tem {num_linhas} linhas. O máximo exigido é de {max_linhas_ufrgs} linhas.",
            "nota": 0,
            "erros_ia": [],
            "acertos_competencia": {},
            "relevancia_tema": "Baixa"
        }

    # Simulação da avaliação da UFRGS (0 a 30)
    nota_simulada = random.randint(10, 30)
    erros = []
    acertos_por_peso = {}
    relevancia_tema = "Não avaliado"
    
    # Análise de relevância do tema
    if relevance_pipeline:
        try:
            # Essa é uma simulação. Um modelo real usaria similaridade semântica.
            # Aqui, apenas verificamos se a redação e o tema têm um "sentimento" positivo.
            # É uma forma bem simplificada de mostrar a lógica.
            redacao_sentimento = relevance_pipeline(texto_redacao)
            tema_sentimento = relevance_pipeline(tema_redacao)
            
            if redacao_sentimento[0]['label'] == tema_sentimento[0]['label'] and redacao_sentimento[0]['score'] > 0.8:
                relevancia_tema = "Alta"
            elif redacao_sentimento[0]['score'] > 0.5:
                relevancia_tema = "Média"
            else:
                relevancia_tema = "Baixa"

            if relevancia_tema == "Baixa":
                nota_simulada -= 10
                erros.append("A redação parece ter baixa relevância com o tema proposto. Revise os argumentos.")
            
        except Exception as e:
            erros.append(f"Erro na análise de relevância: {e}")

    # Simulação da análise de qualidade da redação
    if corrector_pipeline:
        try:
            analise_ia = corrector_pipeline(texto_redacao)
            if 'LABEL_1' in analise_ia[0]['label']:
                erros.append("A IA detectou um tom inadequado ou falta de argumentação. Revise seus argumentos.")
                nota_simulada -= 5
            
            acertos_por_peso = {
                "Argumentação e Coerência": f"{random.randint(5, 10)}/10",
                "Domínio da norma padrão": f"{random.randint(5, 10)}/10",
                "Proposta de Intervenção": f"{random.randint(0, 5)}/5"
            }
        except Exception as e:
            erros.append(f"Erro na análise de IA: {e}")
    else:
        erros.append("O modelo de IA não está disponível. A correção é apenas uma simulação.")

    nota_final = max(0, min(30, nota_simulada))

    return {
        "mensagem": "Agradecemos o envio da sua redação. Abaixo, a análise simulada da banca.",
        "nota": nota_final,
        "erros_ia": erros,
        "acertos_competencia": acertos_por_peso,
        "relevancia_tema": relevancia_tema
    }
