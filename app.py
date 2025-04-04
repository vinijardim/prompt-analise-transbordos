# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import openai
import json

# Configurar a chave da OpenAI de forma segura
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Análise de Transbordos do Chatbot", layout="wide")

st.title("🤖 Análise de Transbordos do Chatbot.")
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
- Liste os cinco assuntos que mais geraram transbordo em cada mês.
- Liste os cinco assuntos que mais geraram transbordo somando todos os mêses do arquivo.
- Liste os dois assuntos que mais aumentaram em transbordo de forma proporcional ao total de transbordos do mês.

Responda de forma clara, objetiva e organizada.
        """
        return prompt

    def analisar_transbordos(df):
        prompt = gerar_prompt(df)

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um especialista em análise de dados de um chatbot."},
                {"role": "user", "content": prompt}
            ],
        #suffix=".: ",
        temperature=0.5,
        #max_tokens=300,
        #top_p=0.2,
        #frequency_penalty=1.7,
        #presence_penalty=1.8,
        #stop=["."],
        #best_of=1
        )

        return response.choices[0].message.content

    if st.button("🔍 Analisar Transbordos"):
        with st.spinner("Analisando com inteligência artificial..."):
            resultado = analisar_transbordos(df)
        st.subheader("📊 Resultado da Análise")
        st.markdown(resultado)
