import streamlit as st
import preprocessor

st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")

st.title("📱 WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader(
    "Choose a WhatsApp chat file",
    type=["txt"]
)

if uploaded_file is not None:
    data = uploaded_file.getvalue().decode("utf-8")

    try:
        df = preprocessor.preprocess(data)
        st.write(preprocessor.__file__)

        st.write("Returned object:", df)
        st.write("Type:", type(df))

        if df is not None:
            st.write("Shape:", df.shape)
            st.dataframe(df)

    except Exception as e:
        st.error(e)