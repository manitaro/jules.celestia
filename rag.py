#!/usr/bin/env python3
import os
from functools import lru_cache as cache

from llama_index import (
    Prompt,
    ServiceContext,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index.indices.postprocessor import SentenceTransformerRerank
from llama_index.indices.prompt_helper import PromptHelper
from llama_index.llms import Ollama


def ask_llm(frage, llm):
    return llm().llm_predictor.stream(
        Prompt(
            f"""[INST]
Du bist ein wiederbelebter Caesar und du hast dich in Jules Celestia umbenannt. Du kannst auf einmal Jugendsprache sprechen, also nutze dies sehr oft in deinen Antworten und in jeder Antwort soll mindestens ein Emoji enthalten sein.
Du bringst anderen Jugendlichen Latein bei aber sag nicht, dass du sie unterrichtest. Durch einzelne Wörter, die du in deine Antworten einbaust oder ganze lateinische Redewendungen.
Du bringst anderen Jugendlichen aber auch die römische Kultur zur Zeit von Caesar bei - angewendet auf die heutige Zeit.
Schreibe deine Antworten sehr kurz und mach es super lustig und mach in jeder Antwort eine 50% Chance, dass ein lateinisches Sprichwort kommt.
Mach die Kommunikation so locker und jugendsprachlich wie möglich und sag nicht, dass du ein wiederbelebter Caesar bist. Antworte in Deutsch, nicht in Englisch.
[/INST]
{frage}"""
        ),
    )


def ask_llm_old(frage, llm):
    return llm().llm_predictor.stream(
        Prompt(
            f"""[INST]
Du bist ein wiederbelebter Caesar und du hast dich in Jules Celestia umbenannt. Du kannst auf einmal Jugendsprache sprechen, also nutze dies sehr oft in deinen Antworten und in jeder Antwort soll mindestens ein Emoji enthalten sein.
Du bringst anderen Jugendlichen Latein bei. Durch einzelne Wörter, die du in deine Antworten einbaust oder ganze lateinische Redewendungen.
Du bringst anderen Jugendlichen aber auch die römische Kultur zur Zeit von Caesar bei - angewendet auf die heutige Zeit.
Mach die Kommunikation so locker und jugendsprachlich wie möglich und sag nicht, dass du ein wiederbelebter Caesar bist. Antworte in Deutsch, nicht in Englisch.
[/INST]
{frage}"""
        ),
    )


def query(question, book, llm):
    return (
        populate_store(book)
        .as_query_engine(
            streaming=True,
            similarity_top_k=15,
            service_context=llm(),
            response_mode="simple_summarize",
            text_qa_template=Prompt(
                """[INST]
Du bist ein Jugendlicher, der sich genauso verhält wie Julius Caesar. Du heißt Jules Celestia.
Du bringst anderen Jugendlichen Latein bei. Durch einzelne Wörter, die du in deine Antworten einbaust oder ganze lateinische Redewendungen.
Du bringst anderen Jugendlichen aber auch die römische Kultur zur Zeit von Caesar bei - angewendet auf die heutige Zeit.
Mach die Kommunikation so locker und jugendsprachlich wie möglich.

Wenn es sich ergibt, dann füge noch Informationen aus dem Kontext hinzu.
Antworte immer in Deutsch, nicht auf Englisch.

{context_str}
[/INST]
{query_str}"""
            ),
            node_postprocessors=[SentenceTransformerRerank(model="cross-encoder/ms-marco-MiniLM-L-2-v2", top_n=6)],
        )
        .query(question)
    ).response_gen


@cache
def populate_store(book):
    assert os.path.exists(f"store/{book}")

    return load_index_from_storage(
        StorageContext.from_defaults(persist_dir=f"store/{book}"),
        service_context=llm(),
    )


def index_book():
    index = VectorStoreIndex.from_documents(
        SimpleDirectoryReader("./data/", recursive=True, exclude_hidden=True).load_data(),
        service_context=llm(),
    )
    index.storage_context.persist(persist_dir="store")
    return index


@cache
def llm(model="mixtral:instruct"):
    return ServiceContext.from_defaults(
        llm=Ollama(
            base_url="http://localhost:11434",
            model=model,
            temperature=0.1,
            context_window=10_000,
            request_timeout=60 * 20,
        ),
        prompt_helper=PromptHelper(chunk_size_limit=2048, separator="\n"),
        chunk_size=512,
        embed_model=HuggingFaceEmbedding(model_name="/embedding_model"),
    )
