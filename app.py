# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import openai
import json

# Configurar a chave da OpenAI de forma segura
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Análise de Transbordos do Chatbot", layout="wide")

st.title("🤖 Análise de Transbordos do Chatbot")
st.write("Faça upload de uma base contendo os **assuntos** e os respectivos **números de transbordos** para gerar uma análise com IA.")

# Upload do arquivo
uploaded_file = st.file_uploader("📤 Envie o arquivo CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📌 Primeiras linhas do arquivo")
    st.dataframe(df.head())

    def gerar_prompt(df):
        # Converte o DataFrame inteiro em JSON (atenção ao tamanho do prompt para não estourar o limite da API)
        exemplos = df.to_dict(orient="records")

        prompt = f"""
Você é um especialista em análise de chatbot. Abaixo estão dados com assuntos e suas respectivas quantidades de transbordos.

Dados:
{json.dumps(exemplos, indent=2, ensure_ascii=False)}

Tarefa:
- Liste os assuntos que mais geram transbordo.
- Sugira possíveis motivos para os altos volumes de transbordo.
- Proponha melhorias práticas para reduzir os transbordos e melhorar a experiência do usuário.

Responda de forma clara, objetiva e organizada.
        """
        return prompt

    def analisar_transbordos(df):
        prompt = gerar_prompt(df)

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um especialista em análise de chatbot."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    if st.button("🔍 Analisar Transbordos"):
        with st.spinner("Analisando com inteligência artificial..."):
            resultado = analisar_transbordos(df)
        st.subheader("📊 Resultado da Análise")
        st.markdown(resultado)
