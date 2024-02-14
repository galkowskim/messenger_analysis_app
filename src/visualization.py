import random

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import seaborn as sns
import streamlit as st
from matplotlib.dates import DayLocator
from matplotlib.ticker import FixedLocator
from streamlit_lottie import st_lottie
from wordcloud import WordCloud

from data_utils import (
    EmojiCloud,
    prepare_emoji_cloud_data,
    prepare_heatmap_data,
    prepare_word_cloud_data,
)


def load_lottieurl(url: str) -> dict:
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def load_lottie() -> dict:
    downloaded_url = load_lottieurl(
        "https://assets3.lottiefiles.com/private_files/lf30_d9lonffd.json"
    )
    return downloaded_url


def display_header() -> None:
    downloaded_url = load_lottie()
    _, mess_logo, _, title, _ = st.columns((0.05, 0.65, 0.1, 1.35, 0.05))

    with mess_logo:
        st_lottie(downloaded_url, height=200)

    with title:
        st.markdown("# Messenger Analysis")
        st.markdown(
            "#### Created by: [Mikołaj Gałkowski](https://github.com/galkowskim), [Laura Hoang](https://github.com/hoanganhlinh), [Wiktor Jakubowski]("
            "https://github.com/WJakubowsk)"
        )


def display_activity_chart(data: pd.DataFrame) -> None:
    st.markdown(
        "##### Firstly, let's explore your activity on Messenger. Below there is a line plot presenting number of "
        "messages sent to you by your friends. The data is categorized by gender in order to compare your activity with"
        " men and women respectively."
    )

    column_1, column_2 = st.columns((1, 3))

    with column_1:
        st.markdown("")
        st.markdown("")
        st.markdown("")

        femalebox = st.checkbox("Female", key="femalebox", value=True)
        malebox = st.checkbox("Male", key="malebox", value=True)

        df_count_messages_per_sex = (
            data.groupby(["specific_date", "sex"]).size().reset_index(name="count")
        )

        starting = st.date_input(
            "Starting date",
            key="starting",
            min_value=data["specific_date"].min(),
            value=data["specific_date"].min(),
            max_value=data["specific_date"].max(),
        )
        ending = st.date_input(
            "Ending date",
            key="ending",
            min_value=data["specific_date"].min(),
            value=data["specific_date"].max(),
            max_value=data["specific_date"].max(),
        )

    with column_2:
        plt.figure(figsize=(12, 4), dpi=1000, facecolor="#3A5094")

        ax = plt.gca()
        ax.set_facecolor("#3A5094")
        plt.grid()

        if femalebox and malebox:
            palette = ["#FE5A75", "#148BFF"]
            sns.lineplot(
                x="specific_date",
                y="count",
                hue="sex",
                palette=palette,
                data=df_count_messages_per_sex,
                ax=ax,
            )
        if femalebox and not malebox:
            sns.lineplot(
                x="specific_date",
                y="count",
                color="#FE5A75",
                data=df_count_messages_per_sex.loc[
                    df_count_messages_per_sex["sex"] == "female"
                ],
                ax=ax,
            )
        if malebox and not femalebox:
            sns.lineplot(
                x="specific_date",
                y="count",
                color="#148BFF",
                data=df_count_messages_per_sex.loc[
                    df_count_messages_per_sex["sex"] == "male"
                ],
                ax=ax,
            )

        legend = plt.legend()
        frame = legend.get_frame()
        frame.set_facecolor("white")
        plt.locator_params(axis="x", nbins=50)

        ax.xaxis.set_major_locator(DayLocator(1))
        ax.spines["top"].set_color("white")
        ax.spines["right"].set_color("white")
        ax.spines["bottom"].set_color("white")
        ax.spines["left"].set_color("white")
        plt.setp(plt.gca().get_xticklabels(), rotation=70, ha="right")
        plt.tight_layout()
        plt.xlim((starting, ending))
        plt.ylim(0)
        plt.margins(0, 0)
        st.set_option("deprecation.showPyplotGlobalUse", False)
        ax.tick_params(colors="white")
        ax.set_xlabel("", color="white")
        ax.set_ylabel("No. messages", color="white")
        ax.set_title(
            "Number of my messages sent to me from other users by their gender",
            color="white",
        )
        sns.set(rc={"axes.facecolor": "#3A5094", "axes.edgecolor": "white"})
        plt.grid()
        st.pyplot()


def display_heatmap(data: pd.DataFrame) -> None:
    st.markdown(
        "##### After research of numbers of messages sent to you, it would be an interesing idea to "
        " explore your own numbers. Below there is a heatmap displaying mean of messages sent throughout each "
        "hour by you. Data is categorized by weekday."
    )

    with st.container():
        _, column_1, _, column_2, _ = st.columns([0.1, 0.93, 0.2, 2.3, 0.20])

        with column_1:
            st.markdown("Select time period no shorter than 7 days.")
            starting_date = st.date_input(
                "Starting date",
                key="starting2",
                min_value=data["specific_date"].min(),
                value=data["specific_date"].min(),
                max_value=data["specific_date"].max(),
            )
            ending_date = st.date_input(
                "Ending date",
                key="ending2",
                min_value=data["specific_date"].min(),
                value=data["specific_date"].max(),
                max_value=data["specific_date"].max(),
            )

        if (ending_date != starting_date) and (
            int(str(ending_date - starting_date).split(" ")[0]) >= 7
        ):

            dfHeatmap = prepare_heatmap_data(data, starting_date, ending_date)

            with column_2:
                st.set_option("deprecation.showPyplotGlobalUse", False)

                DAYS = ["Mon.", "Tues.", "Wed.", "Thurs.", "Fri.", "Sat.", "Sun."]

                heatmap = np.zeros((7, 24))

                for hour in range(24):
                    for week_day in range(7):
                        heatmap[week_day, hour] = dfHeatmap.loc[
                            (dfHeatmap["week_day"] == week_day)
                            & (dfHeatmap["hour"] == hour)
                        ]["sum_mean_id"]

                x = np.arange(24 + 1) - 0.5
                y = np.arange(7 + 1) - 0.5

                _, ax = plt.subplots()
                mesh = ax.pcolormesh(x, y, heatmap, edgecolor="white", alpha=0.8)

                ax.invert_yaxis()
                ax.grid(False)
                ax.set_aspect("equal")

                ax.set_yticks(np.arange(7))
                ax.set_yticklabels(DAYS, color="white", size=5)

                ax.set_xticks(np.arange(24))
                ax.set_xticklabels(np.arange(24), color="white", size=5)

                ax.set_title(
                    "Heatmap presenting my hourly acitivity throughout the day",
                    color="white",
                    size=9,
                )

                plt.sca(ax)
                plt.sci(mesh)

                cb = plt.colorbar(ax=ax, shrink=0.5)
                cmap = mpl.colormaps.get_cmap("Blues")

                cb.ax.set_yticklabels(
                    np.arange(-0.5, max(dfHeatmap.sum_mean_id) + 0.5),
                    color="white",
                    size=5,
                )
                cb.ax.set_title("Mean no. \nmessages", color="white", size=6)

                plt.set_cmap(cmap)

                cb.ax.yaxis.set_major_locator(FixedLocator(cb.get_ticks()))
                cb.ax.tick_params(size=0)
                cb.outline.set_edgecolor("white")

                ax.tick_params(size=0)
                ax.spines["top"].set_color("white")
                ax.spines["right"].set_color("white")
                ax.spines["bottom"].set_color("white")
                ax.spines["left"].set_color("white")

                plt.savefig(
                    "heatmap.png", dpi=300, bbox_inches="tight", transparent=True
                )
                st.image(
                    "heatmap.png"
                )  # Tried st.pyplot(), but it does not support transparency, so that's why the plot is saved as a file and then displayed.
        else:
            st.markdown(
                "<font color='red'> Selected time period is too short. Must be at least 7 days long. </font>",
                unsafe_allow_html=True,
            )


def display_emoji_word_cloud(data: pd.DataFrame) -> None:
    st.markdown(
        "##### Finally, let's take a closer look at the content of the messages. They split into two categories:"
        " words and emojis. Below there is a WordCloud consiting of the most frequently sent words by you."
        " On the other hand, after switching the button, your most popular emojis are shown on an EmojiCloud."
    )

    with st.container():
        st.set_option("deprecation.showPyplotGlobalUse", False)
        _, column_1, _, column_2, _ = st.columns([0.3, 1.5, 0.3, 1.5, 0.3])

        with column_1:
            for _ in range(10):
                st.markdown("")

            cloudType = st.radio(
                "Select cloud type:", ("Emoji", "Word"), key="cloudType", index=0
            )

            if cloudType == "Emoji":
                st.slider(
                    label="Select maximum number of emojies on EmojiCloud",
                    min_value=10,
                    max_value=100,
                    key="emojis",
                    value=50,
                )
            else:
                st.slider(
                    label="Select minimal word length",
                    key="min_word_length",
                    min_value=3,
                    value=4,
                    max_value=10,
                )
        with column_2:

            def grey_color_func(
                word, font_size, position, orientation, random_state=None, **kwargs
            ):
                return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

            if cloudType == "Emoji":
                emoji = prepare_emoji_cloud_data(data, "Mikołaj Gałkowski")
                emoji_cloud2 = EmojiCloud(
                    font_path="./fonts/Symbola.otf",
                    contour_width=50,
                    contour_color="#6a80c4",
                    background_color="#3A5094",
                    maxwords=int(st.session_state.emojis),
                )
                emoji_cloud2.generate(emoji)
                plt.imshow(
                    emoji_cloud2.word_cloud.recolor(
                        color_func=grey_color_func, random_state=42
                    )
                )
                plt.tight_layout(pad=0)
                st.pyplot()
            else:

                messages = prepare_word_cloud_data(
                    data, int(st.session_state.min_word_length)
                )
                wordcloud = WordCloud(
                    font_path="./fonts/Symbola.otf",
                    width=500,
                    height=400,
                    max_font_size=100,
                    max_words=100,
                    background_color="#6a80c4",
                ).generate(messages)
                plt.tight_layout(pad=0)
                plt.figure(figsize=(6, 3))
                plt.imshow(
                    wordcloud.recolor(color_func=grey_color_func, random_state=3),
                    interpolation="bilinear",
                )
                plt.axis("off")
                st.pyplot()
