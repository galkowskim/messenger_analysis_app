import string
from collections import Counter

import emojis
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from wordcloud import WordCloud


@st.experimental_memo(show_spinner=False)
def prepare_emoji_cloud_data(df: pd.DataFrame, person: str) -> str:
    data = df.loc[(df["author"] == person) & (df["content"].notna()), "content"]
    flattened = [
        item
        for sublist in data.str.split()
        for item in sublist
        if isinstance(item, str) or isinstance(item, float)
    ]

    valid_characters = set(
        string.ascii_lowercase + string.ascii_uppercase + string.digits
    )
    non_alphanumeric = set(",./;'[]-=)(*&^%$#@!:\"?><\{\}|+–'")

    filtered = filter(
        lambda mess: len(mess) == 1
        and mess not in valid_characters
        and mess not in non_alphanumeric,
        flattened,
    )

    emoji = " ".join(filtered)

    return emoji


@st.experimental_memo(show_spinner=False)
def prepare_heatmap_data(
    data: pd.DataFrame, starting_date: str, ending_date: str
) -> pd.DataFrame:
    starting_date = pd.to_datetime(starting_date)
    ending_date = pd.to_datetime(ending_date)

    filtered_data = data[
        (data["specific_date"] >= starting_date)
        & (data["specific_date"] <= ending_date)
    ].copy()

    filtered_data["specific_date"] = filtered_data["specific_date"].dt.strftime(
        "%Y-%m-%d"
    )
    filtered_data = filtered_data.loc[filtered_data["author"] != ""]
    grouped_data = filtered_data.groupby(["specific_date", "hour"], as_index=False).agg(
        {"id": "count"}
    )

    days = (
        pd.date_range(start=starting_date, end=ending_date, freq="1D")
        .strftime("%Y-%m-%d")
        .tolist()
    )
    hours = list(range(24)) * len(days)
    all_dates = pd.DataFrame({"specific_date": sorted(days * 24), "hour": hours})

    result = pd.merge(
        all_dates, grouped_data, how="left", on=["specific_date", "hour"]
    ).fillna(0)

    result["week_day"] = pd.to_datetime(result["specific_date"]).dt.dayofweek

    result = (
        result.groupby(["week_day", "hour"], as_index=False)
        .agg({"id": "mean"})
        .rename(columns={"id": "sum_mean_id"})
    )

    return result


@st.experimental_memo(show_spinner=False)
def prepare_word_cloud_data(df: pd.DataFrame, length: int):
    data = df.loc[df["author"] != ""]
    flattened = [
        word
        for content in data["content"].str.split()
        if isinstance(content, list)
        for word in content
    ]

    alphabet = "qwertyuiopasdfghjklzxcvbnmżłąęćźó"
    alphabet_upper = alphabet.upper()
    digits = "1234567890"
    symbols = ",./;'[]-=)(*&^%$#@!:\"?><\{\}|+–'"

    flattened = [word for word in flattened if not isinstance(word, float)]

    filtered = filter(
        lambda message: (len(message) > length)
        and (message not in alphabet)
        and (message not in alphabet_upper)
        and (message != "\n")
        and (message not in digits)
        and (message not in symbols)
        and ("https" not in message),
        flattened,
    )

    return " ".join(filtered)


@st.experimental_singleton
class EmojiCloud:
    def __init__(
        self,
        font_path="Symbola.otf",
        mask=None,
        contour_width=None,
        contour_color=None,
        background_color=None,
        maxwords=200,
    ):
        self.font_path = font_path
        self.background_color = background_color
        self.mask = mask
        self.contour_width = contour_width
        self.contour_color = contour_color
        self.maxwords = maxwords
        self.word_cloud = self.initialize_wordcloud()
        self.emoji_probability = None

    def initialize_wordcloud(self):
        return WordCloud(
            font_path=self.font_path,
            width=500,
            height=500,
            max_words=self.maxwords,
            background_color=self.background_color,
            random_state=42,
            collocations=False,
            mask=self.mask,
            contour_width=self.contour_width,
            contour_color=self.contour_color,
        )

    def color_func(
        self, word, font_size, position, orientation, random_state=None, **kwargs
    ):
        hue_saturation = "60, 60%"

        current_emoji_probability = self.emoji_probability[word]
        opacity = min(75, 50 + (0.1 - current_emoji_probability) / 0.2 * 25)

        return f"hsl({hue_saturation},{opacity}%)"

    def generate(self, text):
        emoji_frequencies = Counter(emojis.iter(text))
        total_count = sum(emoji_frequencies.values())

        self.emoji_probability = {
            emoji: count / total_count for emoji, count in emoji_frequencies.items()
        }
        wc = self.word_cloud.generate_from_frequencies(emoji_frequencies)

        plt.figure(figsize=(6, 3))
        plt.imshow(wc.recolor(color_func=self.color_func, random_state=42))
        plt.axis("off")

    def recolor(self, color):
        self.word_cloud.recolor(color)
