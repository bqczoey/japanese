import streamlit as st
import pandas as pd
from sudachipy import dictionary
import os

tokenizer = dictionary.Dictionary().create()

FILE = "vocab.csv"

st.title("日文單字查詢")

word = st.text_input("請輸入日文")

if st.button("查詢"):

    tokens = tokenizer.tokenize(word)

    for token in tokens:

        result = {
            "輸入": token.surface(),
            "原形": token.dictionary_form(),
            "讀音": token.reading_form(),
            "詞性": token.part_of_speech()[0]
        }

        st.write(result)

        if os.path.exists(FILE):
            df = pd.read_csv(FILE)
        else:
            df = pd.DataFrame()

        new_row = pd.DataFrame([result])

        if len(df) == 0:
            df = new_row
        else:
            exists = (
                (df["輸入"] == result["輸入"])
                &
                (df["原形"] == result["原形"])
            ).any()

            if not exists:
                df = pd.concat(
                    [df, new_row],
                    ignore_index=True
                )

        df.to_csv(FILE, index=False)

st.subheader("查詢紀錄")

if os.path.exists(FILE):
    history = pd.read_csv(FILE)
    st.dataframe(history)