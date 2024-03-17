#!/usr/bin/env python3
import base64
from functools import partial

import streamlit

import rag


@streamlit.cache_resource
def llm():
    return rag.llm()


if "messages" not in streamlit.session_state:
    streamlit.session_state.messages = []


def clear_messages():
    streamlit.session_state.messages = []


streamlit.set_page_config(
    page_title="Jules Celestia",
    page_icon="images/favicon.png",
    layout="wide",
)


@streamlit.cache_resource
def cache_image(path):
    with open(path, "rb") as file:
        return base64.b64encode(file.read()).decode()


def colored_container(id, color="#E4F2EC"):
    container = streamlit.container()
    streamlit.markdown("<div id = 'my_div_outer'></div>", unsafe_allow_html=True)

    with container:
        container.markdown(f"<div id = 'my_div_inner_{id}'></div>", unsafe_allow_html=True)

    streamlit.markdown(
        f"""
        <style>
            div[data-testid='stVerticalBlock']:has(div#my_div_inner_{id}):not(:has(div#my_div_outer)) {{
                background-color: {color};
                border-radius: 20px;
                padding: 0px;
                text-align: center;
            }};

            #my_div_inner_{id} img {{
                width: 75%;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    return container


with streamlit.sidebar:
    streamlit.title("Jules Celestia")
    streamlit.divider()
    streamlit.markdown("Ich bin ein neugeborener Julius Caesar in der heutigen Zeit. Lass uns reden.")

    streamlit.subheader("Zusatzwissen", divider=True)
    streamlit.write("Soll ich Zusatzwissen aus Büchern nutzen?")

    books = [
        ("De bello Gallico", "images/book_de_bello_gallico.jpg"),
        ("Bellum Civile", "images/book_bellum_civile_primus.png"),
        ("Bellum Alexandrinum", "images/book_bellum_alexandrinum.jpg"),
    ]
    knowledge = {}

    def change_book(title):
        for book, _image in books:
            if book == title:
                continue
            streamlit.session_state[book] = False

    for col, title_with_image in zip(streamlit.columns(len(books)), books):
        title, image = title_with_image
        with col:
            knowledge[title] = streamlit.toggle(
                key=title,
                label=title,
                label_visibility="collapsed",
                value=False,
                disabled=title == "Bellum Alexandrinum",
                on_change=partial(change_book, title),
            )
            streamlit.markdown(
                f'<img src="data:image/jpeg;base64,{cache_image(image)}" style="width:90px; height:120px" alt="Wissen von {title}"/>',
                unsafe_allow_html=True,
            )
            streamlit.write(title)

    streamlit.divider()
    with streamlit.expander("Weitere Erklärungen"):
        streamlit.write(
            "Hab Spaß dich mit mir zu unterhalten. Stell mir merkwürdige, lustige, interessante, doofe, lange, kurze Fragen. Oder erzähl mir einfach was heutzutage so üblich ist. Ich hab 2.000 Jahre geschlafen, da hab ich einiges verpasst."
        )
        with colored_container("jugendsprache", color="#e0efffff"):
            streamlit.subheader("Jugendsprache")
            streamlit.image("images/chat_jugendsprache.png")
            streamlit.write("Antwort soll für Jugendliche Spaß machen und verständlich sein.")
        with colored_container("history", color="#fff2ccff"):
            streamlit.subheader("Historische Fakten")
            streamlit.image("images/chat_historie.png")
            streamlit.write("Antwort soll Fakten aus Caesars Werken wie “De Bello Gallico” enthalten um damit spielend zu lernen.")
        with colored_container("zitate", color="#d9d3e9ff"):
            streamlit.subheader("Zitate und Weisheiten")
            streamlit.image("images/chat_zitate.png")
            streamlit.write("Antwort soll gespickt sein mit Zitaten und Weisheiten aus der Zeit um die damalige Zeit näherzubringen.")
        with colored_container("latein", color="#d9ead3ff"):
            streamlit.subheader("Lateinische Wörter")
            streamlit.image("images/chat_latein.png")
            streamlit.write("Antwort soll vereinzelt lateinische Wörter enthalten um spielend Latein beizubringen.")
        with colored_container("fakten", color="#f4cdccff"):
            streamlit.subheader("Fakten von Caesar")
            streamlit.image("images/chat_fakten.png")
            streamlit.write("Antwort soll interessante Fakten von Caesar enthalten um eine persönliche Nähe herzustellen.")

    with streamlit.expander("Beispiele"):
        streamlit.subheader("Frag mich was lustiges")
        with streamlit.chat_message("user", avatar="user"):
            streamlit.markdown("Welche Witze kennst du? Kannst du mir einen Witz von damals erzählen?")

        streamlit.subheader("Frag mich was historisches")
        with streamlit.chat_message("user", avatar="user"):
            streamlit.markdown("Was haben die Arvenier über dich gedacht?")

        streamlit.subheader("Frag mich Lateinisch")
        with streamlit.chat_message("user", avatar="user"):
            streamlit.markdown("Bring mir bitte ein lateinisches Sprichwort bei.")

        streamlit.subheader("Frag mich was dummes")
        with streamlit.chat_message("user", avatar="user"):
            streamlit.markdown("Hast du mit Brutus schon einmal Schach gespielt?")

        streamlit.subheader("Frag mich was emotionales")
        with streamlit.chat_message("user", avatar="user"):
            streamlit.markdown("Was hälst du von Hannibal?")

    with streamlit.expander("Wie funktioniere ich?"):
        streamlit.image("images/page_1.png", caption="Plakat Seite 1")
        streamlit.image("images/page_2.png", caption="Plakat Seite 2")
        streamlit.image("images/page_3.png", caption="Plakat Seite 3")
        streamlit.image("images/page_4.png", caption="Plakat Seite 4")
        streamlit.image("images/page_5.png", caption="Plakat Seite 5")
        streamlit.image("images/page_6.png", caption="Plakat Seite 6")
        streamlit.image("images/page_7.png", caption="Plakat Seite 7")
        streamlit.image("images/page_8.png", caption="Plakat Seite 8")

    with streamlit.expander("Zukunft"):
        streamlit.info("Bis jetzt geht leider nur De Bello Gallico als Zusatzwissen. Geplant ist auch die anderen beiden Bücher zu finden und einzulesen.")
        streamlit.info("Ich will ein größeres und neueres Sprachmodell ausprobieren um noch besser zu werden.")
        streamlit.info("Ich will einen LLM Agent implementieren um besser auf Wissen zugreifen zu können.")
        streamlit.info("Ich will Antworten automatisch prüfen, damit Jules nicht soviel Quatsch erzählt.")


def set_background(path):
    streamlit.markdown(
        f"""
        <style>
            body {{
                background-image: url("data:image/png;base64,{cache_image(path)}");
                background-size: cover;
            }}

            div[data-testid="stApp"] {{
                background-image: url("data:image/png;base64,{cache_image(path)}");
                background-repeat: no-repeat;
                background-attachment: fixed;
                background-size: cover;
                background-color: #cccccc;
                background-blend-mode: color-burn;
                opacity: 0.99;
            }}

        </style>""",
        unsafe_allow_html=True,
    )


set_background("images/background2.jpg")

if not streamlit.session_state.messages:
    streamlit.session_state.messages.append(
        {
            "role": "images/favicon.png",
            "content": """Hi. Ich bin Jules. Interessierst du dich für Latein oder römische Geschichte? Ich kann dir vielleicht interessante Geschichten erzählen. Lass quatschen.""",
        }
    )
for message in streamlit.session_state.messages:
    with streamlit.chat_message(message["role"], avatar=message["role"]):
        streamlit.markdown(message["content"])

if prompt := streamlit.chat_input("rede mit mir - mihi loquere"):
    with streamlit.chat_message("user"):
        streamlit.markdown(prompt)
    streamlit.session_state.messages.append({"role": "user", "content": prompt})

    answer = ""
    with streamlit.chat_message(image, avatar="images/favicon.png"):
        message_placeholder = streamlit.empty()

        asker = partial(rag.ask_llm, prompt, llm=llm)
        for book, value in knowledge.items():
            if not value:
                continue
            asker = partial(rag.query, prompt, book=book.replace(" ", "_").lower(), llm=llm)

        for word in asker():
            answer += word
            message_placeholder.markdown(answer + "▌")
        message_placeholder.markdown(answer)
    streamlit.session_state.messages.append({"role": "images/favicon.png", "content": answer})
