import pandas as pd
import streamlit as st

from visualization import (
    display_activity_chart,
    display_emoji_word_cloud,
    display_header,
    display_heatmap,
)

st.set_page_config(layout="wide", page_title="Messenger Analysis", page_icon="💬")


def main():
    display_header()
    file = st.file_uploader("Upload csv file with your data.", key="file")

    if file is not None:
        data = pd.read_csv(file, sep="\t")
        data["author"] = data["author"].fillna("")
        data["date"] = pd.to_datetime(data["date"])
        data["specific_date"] = pd.to_datetime(data["date"].dt.date)
        display_activity_chart(data)
        display_heatmap(data)
        display_emoji_word_cloud(data)


if __name__ == "__main__":
    main()
