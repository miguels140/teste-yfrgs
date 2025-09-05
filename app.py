import streamlit as st
from corrector_logic import corrigir_redacao

st.set_page_config(page_title="Corretor de Redação UFRGS", layout="wide")

st.title("Corretor de Redação UFRGS")
st.markdown("---")

st.info("Esta ferramenta é uma **simulação** de um corretor de redação. A nota e o feedback são gerados com base em modelos de IA e regras de negócio para fins de demonstração.")

# Campos de entrada para a redação e o tema
tema_redacao = st.text_input("Qual é o tema da sua redação?", placeholder="Ex: O papel da tecnologia na sociedade moderna")
texto_redacao = st.text_area("Cole sua redação aqui (mín. 30, máx. 45 linhas)", height=500, placeholder="Comece a escrever sua redação...")

if st.button("Corrigir Redação", type="primary"):
    if not texto_redacao or not tema_redacao:
        st.warning("Por favor, preencha o tema e cole a redação para começar a correção.")
    else:
        with st.spinner("Analisando sua redação..."):
            resultados = corrigir_redacao(texto_redacao, tema_redacao)

        st.markdown("---")
        st.subheader("Resultados da Análise")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Nota Final (0-30)", resultados["nota"])
            st.metric("Relevância do Tema", resultados["relevancia_tema"])
            st.info(f"Número de Linhas: {len(texto_redacao.split('\n'))}")

        with col2:
            st.markdown(f"**Mensagem:** {resultados['mensagem']}")
            
            st.subheader("Índice de Acerto por Competência")
            st.json(resultados["acertos_competencia"])
            
            st.subheader("Erros e Recomendações da IA")
            if resultados["erros_ia"]:
                for erro in resultados["erros_ia"]:
                    st.warning(f"⚠️ {erro}")
            else:
                st.success("✅ Nenhuma recomendação importante foi detectada. Parabéns!")
