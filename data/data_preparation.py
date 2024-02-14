import json
import os
from datetime import datetime
from pathlib import Path

import pandas as pd


def find_folders(path: Path = Path("./messages")) -> None:
    for folder in os.listdir(path):
        if "mess" in folder:
            for inner_folder in os.listdir(os.path.join(path, folder, "messages")):
                if inner_folder == "inbox":
                    print(
                        f"Keeping {inner_folder} inside {os.path.join(path, folder, 'messages')}"
                    )
                else:
                    print(
                        f"Deleted {inner_folder} inside {os.path.join(path, folder, 'messages')}"
                    )
                    os.system(
                        f"rm -rf {os.path.join(folder, 'messages', inner_folder)}"
                    )

    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if dir in ("gifs", "photos", "videos", "audio", "files"):
                print(f"Deleting {os.path.join(root, dir)}")
                os.system(f"rm -rf {os.path.join(root, dir)}")
        for file in files:
            if file in (
                "autofill_information.json",
                "messenger_contacts_you've_blocked.json",
                "previously_removed_contacts.json",
                "secret_conversations.json",
                "secret_groups.json",
                "support_messages.json",
                "your_cross-app_messaging_settings.json",
            ):
                print(f"Deleting {os.path.join(root, file)}")
                os.system(f'rm -rf "{os.path.join(root, file)}"')


def prepare_dataset(path: Path = Path("./messages")) -> None:
    message_id = 1
    output = []

    person = input(
        "Enter your name (just to filter your messages and treat you as an author): "
    )
    for folder in os.listdir(path):
        subfolder = os.path.join(path, folder, "messages", "inbox")
        for conversation_folder in os.listdir(subfolder):
            conversation_directory = os.path.join(subfolder, conversation_folder)
            for f in os.listdir(conversation_directory):
                if f.endswith("json") and "message" in f:
                    filepath = os.path.join(conversation_directory, f)
                    with open(filepath) as jfile:
                        data = json.load(jfile)
                        messages = data["messages"]
                        if len(data["participants"]) == 2:
                            participants = [
                                v.encode("iso-8859-1").decode("utf-8")
                                for el in data["participants"]
                                for k, v in el.items()
                            ]
                        message_type = (
                            "Generic"
                            if len(data["participants"]) == 2 and person in participants
                            else "Group"
                        )  # Group type not supported
                        for message in messages:
                            if message_type == "Generic":
                                author = (
                                    message["sender_name"]
                                    .encode("iso-8859-1")
                                    .decode("utf-8")
                                )
                                sex = (
                                    "female"
                                    if author != ""
                                    and author != "Kuba"
                                    and author.split(" ")[0][-1] == "a"
                                    else "male"
                                )
                                if author != "Mikołaj Gałkowski":
                                    author = ""
                                dt = datetime.fromtimestamp(
                                    message["timestamp_ms"] // 1000
                                )
                                whole_date = dt.isoformat()
                                year = dt.year
                                month = dt.month
                                day = dt.day
                                hour = dt.hour
                                minute = dt.minute
                                second = dt.second
                                content = message.get("content")
                                enc = ""
                                if content:
                                    enc = content.encode("iso-8859-1").decode("utf-8")
                                output.append(
                                    [
                                        message_id,
                                        author,
                                        sex,
                                        whole_date,
                                        year,
                                        month,
                                        day,
                                        hour,
                                        minute,
                                        second,
                                        enc,
                                    ]
                                )
                                message_id += 1
    df = pd.DataFrame(
        output,
        columns=[
            "id",
            "author",
            "sex",
            "date",
            "year",
            "month",
            "day",
            "hour",
            "minute",
            "second",
            "content",
        ],
    )
    print(
        f"There are {df.loc[df.author == person].shape[0]} messages from {person} in the dataset."
    )
    if df.loc[df.author == person].shape[0] > 0:
        df.to_csv("messages.csv", sep="\t", index=False)
    else:
        print(
            "No messages from you in the dataset. You should check the author name. Not saving the dataset."
        )


if __name__ == "__main__":
    path = Path("./messages")
    find_folders(path)
    prepare_dataset(path)
