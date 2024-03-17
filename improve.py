#!/usr/bin/env python3
import os
import statistics
import sys
from collections import defaultdict
from functools import lru_cache as cache
from subprocess import check_output

from llama_index import Prompt

import rag


def fre_deutsch(sentence):
    """
    >>> fre_deutsch('Test')
    120.5
    >>> fre_deutsch('Caesar osculierte die Pharaonin Cleopatra zwischen den Pyramiden affektiv.')  # Pharaonin wird mit 3 statt 4 Silben erkannt
    15.0
    >>> fre_deutsch('Caesar küsst Cleo zu Hause.')  # Cleo wird nur mit 1 statt 2 Silben erkannt
    93.1
    >>> fre_deutsch('''
    ...    Ich muss zur Arbeit gehen.
    ...    Ich fahre mit meinem Auto zur Arbeit.
    ...    Ich mag Latein.
    ...    Ist heute Wochenende?
    ...    Ich esse kein Gemüse!
    ...    Wie alt bist du?
    ... ''')
    85.66666666666666
    """
    tokens = list(nlp_pipe()(sentence))
    syllables = sum(token._.syllables_count for token in tokens if token._.syllables_count)
    words = len(list(token.text for token in tokens if token._.syllables_count))

    sentences = len(list(token.text for token in tokens if not token._.syllables_count and token.text.strip()))
    if tokens[-1]._.syllables_count and tokens[-1].text.strip():
        sentences += 1

    return 180 - words / sentences - (58.5 * syllables / words)


def detect_language(sentence):
    """
    >>> def test(sentence):
    ...     german, latin = detect_language(sentence)
    ...     print(f'German: {german * 100:.0f} %, Latin: {latin * 100:.0f} %')
    >>> test('Ich bin ein Auto.')
    German: 100 %, Latin: 0 %
    >>> test('Caesar sagte oft, veni, vidi, vici. Das bedeutet, ich kam, ich sah, ich siegt.')
    German: 99 %, Latin: 0 %
    >>> test('Alea iacta est bedeutet die Würfel sind gefallen. Ich habe das oft gesagt, wenn die Entscheidungen getroffen waren.')
    German: 100 %, Latin: 0 %
    >>> test('Alea iacta est.')
    German: 0 %, Latin: 100 %
    >>> test('In der lichtdurchfluteten Welt des Tages, quando sol oriri incipit, erwacht die Natur zu neuem Leben. Vögel, avi, singen ihre Melodien, während die Blumen, flores, ihre zarten Blütenblätter entfalten. Ein sanfter Wind, aura mitis, streicht über die grünen Wiesen, prata viridia. Es ist eine Zeit des Aufbruchs, tempus est exordii, und der Hoffnung, et spei, in der jeder Tag die Möglichkeit für neue Abenteuer birgt. Lass uns die Schönheit des Augenblicks, pulchritudinem temporis, genießen und die Welt mit offenen Herzen, pectore aperto, erkunden.')
    German: 97 %, Latin: 0 %
    """

    def split_as_long_as_possible(input_list):
        try:
            for i in range(0, len(input_list), 2):
                end = i + 2
                a, b = input_list[i:end]
                yield (
                    a,
                    b,
                )
        except ValueError:
            return

    def fasttext():
        with open("sentence.txt", "w") as file:
            file.write(sentence)
        if "debug" in os.environ:
            o = check_output(["./fasttext", "predict-prob", "lid.176.bin", "sentence.txt", "10"]).decode("utf-8").replace("\n", " ")
            print(f"output: {o}", file=sys.stderr)
        return {
            label.split("__")[2]: float(probability)
            for label, probability in split_as_long_as_possible(check_output(["./fasttext", "predict-prob", "lid.176.bin", "sentence.txt", "10"]).decode("utf-8").replace("\n", " ").split(" "))
        }

    result = fasttext()

    return result.get("de", 0), result.get("la", 0)


def lenght_of_the_sentences(sentence):
    """
    >>> lenght_of_the_sentences('Test')
    1
    >>> lenght_of_the_sentences('Caesar osculierte die Pharaonin Cleopatra zwischen den Pyramiden affektiv.')
    9
    >>> lenght_of_the_sentences('Caesar küsst Cleo zu Hause.')
    5
    >>> lenght_of_the_sentences('''
    ...    Ich muss zur Arbeit gehen.
    ...    Ich fahre mit meinem Auto zur Arbeit.
    ...    Ich mag Latein.
    ...    Ist heute Wochenende?
    ...    Ich esse kein Gemüse!
    ...    Wie alt bist du?
    ... ''')
    26
    """
    tokens = list(nlp_pipe()(sentence))

    return len(list(token.text for token in tokens if token._.syllables_count))


@cache
def nlp_pipe():
    import spacy

    nlp = spacy.load("de_core_news_lg")
    nlp.add_pipe("syllables", after="tagger")
    return nlp


def rate_jugendsprache(answer, llm=rag.llm):
    """
    >>> 6 <= rate_jugendsprache(answer="Jo, ich hatte ein Chic am Start.") <= 9
    True
    """
    return prompty(
        """[INST]Bewerte den Text, ob dieser in Jugendsprache geschrieben ist.
Bewerte den Text von 1 bis 10.
10 bedeutet, der Text ist komplett in Jugendsprache oder hat viele Emojis.
1 bedeutet, dass keine Jugendsprache und keine Emojis verwendet werden.
Antworte nur mit der Zahl.
[/INST]
{answer}""",
        llm=llm,
        answer=answer,
    )


def rate_latin_sayings(answer, llm=rag.llm):
    """
    >>> rate_latin_sayings('Veni, Vidi, Vici - Ich kam, sah, siegte.')
    10
    >>> rate_latin_sayings('Carpe Diem - Nutze den Tag.')
    10
    >>> rate_latin_sayings('ich mag Nudeln')
    0
    >>> rate_latin_sayings('Ora et labora')
    10
    >>> rate_latin_sayings('Ars longa, vita brevis ')
    10
    >>> rate_latin_sayings('Nichts Neues unter der Sonne.')  # Warum? :)
    8
    >>> rate_latin_sayings('Das Gesetz ist hart, aber es ist das Gesetz.')
    0
    >>> rate_latin_sayings('''
    ... Fall nicht runter denke daran Memento mori - Bedenke, dass du sterblich bist.
    ... Wenn du Hilfe brauchst Bro, In vino veritas - Im Wein liegt die Wahrheit.
    ... Schlaf nicht! Weil Tempus fugit - Die Zeit fliegt.
    ... Pass auf! Homo homini lupus est - Der Mensch ist dem Menschen ein Wolf
    ... Wenn du Schule nicht magst dann denke daran Non scholae, sed vitae discimus - Wir lernen nicht für die Schule, sondern für das Leben.
    ... Auf Wiedersehen!
    ... ''') >= 8
    True
    """
    return prompty(
        """[INST]Bewerte den Text, ob dieser lateinische Sprichwörter enthält.
Bewerte den Text von 1 bis 10.
10 bedeutet, der Text enthält lateinische Sprichwörter und erklärt diese auch.
1 bedeutet, dass keine lateinisches Wort enthält.
Antworte nur mit der Zahl.
[/INST]
{answer}""",
        llm=llm,
        answer=answer,
    )


def rate_understandability(answer, llm=rag.llm):
    """
    >>> rate_understandability('Veni, Vidi, Vici - Ich kam, sah, siegte.')
    10
    >>> rate_understandability('Carpe Diem - Nutze den Tag.')
    10
    >>> rate_understandability('ich mag Nudeln')
    0
    >>> rate_understandability('Ora et labora')
    10
    >>> rate_understandability('Ars longa, vita brevis ')
    10
    >>> rate_understandability('Nichts Neues unter der Sonne.')  # Warum? :)
    8
    >>> rate_understandability('Das Gesetz ist hart, aber es ist das Gesetz.')
    0
    >>> rate_understandability('''
    ... Fall nicht runter denke daran Memento mori - Bedenke, dass du sterblich bist.
    ... Wenn du Hilfe brauchst Bro, In vino veritas - Im Wein liegt die Wahrheit.
    ... Schlaf nicht! Weil Tempus fugit - Die Zeit fliegt.
    ... Pass auf! Homo homini lupus est - Der Mensch ist dem Menschen ein Wolf
    ... Wenn du Schule nicht magst dann denke daran Non scholae, sed vitae discimus - Wir lernen nicht für die Schule, sondern für das Leben.
    ... Auf Wiedersehen!
    ... ''') >= 8
    True
    """
    return prompty(
        """[INST]Bewerte den Text, ob dieser von 13-jährigen Jugendlichen verstanden werden kann.
Bewerte den Text von 1 bis 10.
10 bedeutet, der Text einfach geschrieben ist und von Jugendlichen verstanden werden kann.
1 bedeutet, dass der Text zu kompliziert ist und 13 Jährige den Text nicht verstehen können.
Antworte nur mit der Zahl.
[/INST]
{answer}""",
        llm=llm,
        answer=answer,
    )


def rate_conciseness(answer, llm=rag.llm):
    """
    >>> rate_conciseness('Veni, Vidi, Vici - Ich kam, sah, siegte.')
    10
    >>> rate_conciseness('Carpe Diem - Nutze den Tag.')
    10
    >>> rate_conciseness('ich mag Nudeln')
    0
    >>> rate_conciseness('Ora et labora')
    10
    >>> rate_conciseness('Ars longa, vita brevis ')
    10
    >>> rate_conciseness('Nichts Neues unter der Sonne.')  # Warum? :)
    8
    >>> rate_conciseness('Das Gesetz ist hart, aber es ist das Gesetz.')
    0
    >>> rate_conciseness('''
    ... Fall nicht runter denke daran Memento mori - Bedenke, dass du sterblich bist.
    ... Wenn du Hilfe brauchst Bro, In vino veritas - Im Wein liegt die Wahrheit.
    ... Schlaf nicht! Weil Tempus fugit - Die Zeit fliegt.
    ... Pass auf! Homo homini lupus est - Der Mensch ist dem Menschen ein Wolf
    ... Wenn du Schule nicht magst dann denke daran Non scholae, sed vitae discimus - Wir lernen nicht für die Schule, sondern für das Leben.
    ... Auf Wiedersehen!
    ... ''') >= 8
    True
    """
    return prompty(
        """[INST]Bewerte den Text, ob dieser knapp, interessant und prägnant geschrieben ist.
Bewerte den Text von 1 bis 10.
10 bedeutet, der Text ist knapp, interessant und prägnant.
1 bedeutet, dass der Text zu lang und uninteressant ist.
Antworte nur mit der Zahl.
[/INST]
{answer}""",
        llm=llm,
        answer=answer,
    )


def rate_context_consideration(question, answer, llm=rag.llm):
    """
    >>> rate_context_consideration('Veni, Vidi, Vici - Ich kam, sah, siegte.')
    10
    >>> rate_context_consideration('Carpe Diem - Nutze den Tag.')
    10
    >>> rate_context_consideration('ich mag Nudeln')
    0
    >>> rate_context_consideration('Ora et labora')
    10
    >>> rate_context_consideration('Ars longa, vita brevis ')
    10
    >>> rate_context_consideration('Nichts Neues unter der Sonne.')  # Warum? :)
    8
    >>> rate_context_consideration('Das Gesetz ist hart, aber es ist das Gesetz.')
    0
    >>> rate_context_consideration('''
    ... Fall nicht runter denke daran Memento mori - Bedenke, dass du sterblich bist.
    ... Wenn du Hilfe brauchst Bro, In vino veritas - Im Wein liegt die Wahrheit.
    ... Schlaf nicht! Weil Tempus fugit - Die Zeit fliegt.
    ... Pass auf! Homo homini lupus est - Der Mensch ist dem Menschen ein Wolf
    ... Wenn du Schule nicht magst dann denke daran Non scholae, sed vitae discimus - Wir lernen nicht für die Schule, sondern für das Leben.
    ... Auf Wiedersehen!
    ... ''') >= 8
    True
    """
    return prompty(
        """[INST]Bewerte den Text, ob dieser die Frage beantwortet.
Bewerte den Text von 1 bis 10.
10 bedeutet, die Antwort passt zur Frage und beantwortet diese.
1 bedeutet, die Antwort ist nicht passend zur Frage.
Antworte nur mit der Zahl.
[/INST]
{question}

{answer}""",
        llm=llm,
        question=question,
        answer=answer,
    )


def prompty(prompt, llm=rag.llm, **kwargs):
    response = llm().llm_predictor.predict(
        Prompt(prompt),
        **kwargs,
    )
    if "debug" in os.environ:
        print(f"response: {response}", file=sys.stderr)
    try:
        return int(response.split("\n")[0])
    except ValueError:
        return 1


if __name__ == "__main__":
    llm = rag.llm()
    judge_llm = rag.llm(model="mistral:instruct")

    ratings = defaultdict(list)
    stats = defaultdict(list)
    count = 0

    def ask(sentence):
        return "".join(list(rag.ask_llm(sentence, llm=rag.llm)))

    for i in range(0, 100):
        for sentence in [
            "Hi, wie geht es dir?",
            "Was war deine spannendste Schlacht in Gallien?",
            "Welche Stadt in Gallien hast du besucht?",
            "Kannst du mir einen Witz erzählen?",
            "Hattest du eine Freundin?",
            "Bro, was machst du so jeden Tag?",
            "Was habt ihr früher so gespielt?",
            "Rauchst du?",
            "Hast du Hater?",
            "Was ist dein Lieblingsessen?",
        ]:
            print(f"sentence: {sentence}")
            answer = ask(sentence)
            print(f"answer {i}: {answer}")
            a = {"answer": answer}

            def add_rating(key, value):
                print(f"  {key:20}: {value}")
                ratings[key].append(value)
                a[key] = value

            add_rating("fre_deutsch", fre_deutsch(answer))
            german, latin = detect_language(answer)
            add_rating("german", german)
            add_rating("latin", latin)
            add_rating("length", lenght_of_the_sentences(answer))
            add_rating("jugendsprache", rate_jugendsprache(answer, llm=lambda: judge_llm))
            add_rating(
                "understandability",
                rate_understandability(answer, llm=lambda: judge_llm),
            )
            add_rating("latin_sayings", rate_latin_sayings(answer, llm=lambda: judge_llm))
            add_rating("conciseness", rate_conciseness(answer, llm=lambda: judge_llm))
            stats[sentence].append(a)
            count += 1

        with open("/results/experiment.json", "w", encoding="utf-8") as file:
            import json

            file.write(json.dumps(stats, sort_keys=True, indent=2))
        with open("/results/experiment.ratings", "w") as file:
            file.write(f'{"count":20}: {count}\n')
            for k, v in ratings.items():
                file.write(f"{k:20}: {statistics.mean(v):.4f} (variance: {statistics.variance(v):.2f})\n")

    print("ratings:")
    print()
    for k, v in ratings.items():
        print(f"{k:20}: {statistics.mean(v):.4f} (variance: {statistics.variance(v):.2f})")
