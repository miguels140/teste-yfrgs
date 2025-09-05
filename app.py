import streamlit as st
import gradio as gr
from transformers import pipeline

# Configuração do modelo de IA para correção
# NOTA: O modelo 'text-classification' é um exemplo. 
# Para uma correção mais precisa, você precisaria de um modelo de linguagem (LLM) 
# com ajuste fino (fine-tuning) em dados de redações reais da UFRGS.
# Para este exemplo, usaremos um modelo genérico de classificação de texto.
# Recomendo usar um modelo maior e mais específico se o seu hardware permitir.
try:
    corrector_pipeline = pipeline("text-classification", model="unitary/toxic-bert", device=-1)
except Exception as e:
    st.warning(f"Não foi possível carregar o modelo de IA. Verifique as dependências. Erro: {e}")
    corrector_pipeline = None

# --- Interface com Gradio ---
def corrigir_redacao(texto_redacao, palavras_chave_desejadas):
    """
    Função principal que simula a correção da redação.
    """
    # Verificação de limites de linhas
    linhas = texto_redacao.split('\n')
    num_linhas = len(linhas)
    min_linhas_ufrgs = 30  # Exemplo, ajuste conforme a regra oficial
    max_linhas_ufrgs = 45  # Exemplo, ajuste conforme a regra oficial

    if num_linhas < min_linhas_ufrgs:
        return (f"Sua redação tem {num_linhas} linhas. O mínimo exigido é de {min_linhas_ufrgs} linhas.", 0, [])
    if num_linhas > max_linhas_ufrgs:
        return (f"Sua redação tem {num_linhas} linhas. O máximo exigido é de {max_linhas_ufrgs} linhas.", 0, [])

    # Simulação da avaliação da UFRGS (0 a 30)
    # Aqui, a "nota" é gerada de forma simplificada.
    # Em um projeto real, essa parte seria feita por um modelo de IA treinado.
    
    # Simulação da nota (0-30)
    # A nota pode ser gerada com base na análise do texto.
    # Por exemplo, uma pontuação aleatória para simular um primeiro resultado.
    import random
    nota_simulada = random.randint(10, 30)  # Gera uma nota entre 10 e 30
    
    erros = []
    acertos_por_peso = {}

    # Simulação de análise por IA
    if corrector_pipeline:
        try:
            # Essa é uma simulação bem básica. Um modelo real faria uma análise mais profunda.
            analise_ia = corrector_pipeline(texto_redacao)
            
            # Exemplo de como você poderia usar o resultado da IA
            # (isso é apenas um exemplo e não reflete a realidade da correção da UFRGS)
            if 'LABEL_1' in analise_ia[0]['label']: # Exemplo de rótulo 'ruim'
                erros.append("A IA detectou um tom inadequado ou falta de argumentação. Revise seus argumentos.")
                nota_simulada -= 5
            
            # Simulação de avaliação de competências
            # (Exemplos de pesos, ajuste conforme a UFRGS)
            acertos_por_peso = {
                "Argumentação e Coerência": f"{random.randint(5, 10)}/10",
                "Domínio da norma padrão": f"{random.randint(5, 10)}/10",
                "Proposta de Intervenção": f"{random.randint(0, 5)}/5"
            }
            
        except Exception as e:
            erros.append(f"Erro na análise de IA: {e}")
    else:
        erros.append("O modelo de IA não está disponível. A correção é apenas uma simulação.")

    # Verificação de palavras-chave
    palavras_encontradas = [
        palavra for palavra in palavras_chave_desejadas.split(',') 
        if palavra.strip().lower() in texto_redacao.lower()
    ]
    
    # Ajuste da nota final
    nota_final = max(0, min(30, nota_simulada)) # Garante que a nota esteja entre 0 e 30
    
    return (
        f"Agradecemos o envio da sua redação. Abaixo, a análise simulada da banca.",
        nota_final,
        erros,
        acertos_por_peso,
        palavras_encontradas,
        num_linhas
    )


# --- Criação da interface com Gradio e integração no Streamlit ---
def run_app():
    st.title("Corretor de Redação UFRGS")
    st.subheader("Simulação de correção com IA")
    
    st.write("""
        Esta ferramenta é uma **simulação** de um corretor de redação para o vestibular da UFRGS. 
        Ela serve como um protótipo para o seu projeto e não garante a precisão da nota oficial. 
        Para obter resultados precisos, um modelo de IA robusto e treinado em dados reais é necessário.
    """)

    # Definir a interface Gradio
    iface = gr.Interface(
        fn=corrigir_redacao,
        inputs=[
            gr.Textbox(lines=45, label="Cole sua redação aqui (mín. 30, máx. 45 linhas)", placeholder="Escreva sua redação aqui..."),
            gr.Textbox(label="Palavras-chave (separe por vírgula)", placeholder="argumento, sociedade, meio ambiente")
        ],
        outputs=[
            gr.Textbox(label="Mensagem"),
            gr.Number(label="Nota Final (0-30)"),
            gr.JSON(label="Erros e Recomendações da IA"),
            gr.JSON(label="Índice de Acerto por Competência"),
            gr.JSON(label="Palavras-chave Encontradas"),
            gr.Number(label="Número de Linhas")
        ],
        title="Corretor de Redação UFRGS (Protótipo)",
        description="""
        Esta ferramenta simula a correção de uma redação do vestibular da UFRGS. 
        A nota é gerada por um modelo de IA simples e por regras de negócio. 
        Ajuste o código para melhorar a precisão.
        """
    )

    # Iniciar a interface Gradio
    iface.launch()

if __name__ == '__main__':
    run_app()
