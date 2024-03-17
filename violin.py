#!/usr/bin/env python3
if __name__ == "__main__":
    metrics = {
        "conciseness": ("Conciseness", 1, 10),
        "fre_deutsch": ("FRE_deutsch", 0, 150),
        "german": ("Deutsch", 0.0, 1.0),
        "jugendsprache": ("Jugendsprache", 1, 10),
        "latin": ("Latin", 0.0, 1.0),
        "latin_sayings": ("Redewendungen", 1, 10),
        "length": ("Länge", 1, 200),
        "understandability": ("Verstehbarkeit", 1, 10),
    }

    import json

    import matplotlib.pyplot as plt
    import seaborn as sns

    for experiment in (1, 2, 3, 4, 5, 6):
        with open(f"experiments/{experiment}/experiment.json") as file:
            a = json.loads(file.read())

            for key in metrics.keys():
                data = []

                caption, xmin, xmax = metrics[key]
                for question, answers in a.items():
                    for answer in answers:
                        data.append(answer[key])
                sns.set(style="whitegrid")
                plt.figure(figsize=(10, 6))

                ax = sns.violinplot(
                    x=data,
                    inner_kws=dict(box_width=15, whis_width=2, color="lightblue"),
                    palette="muted",
                )
                ax.set_xlim(xmin, xmax)

                plt.xlabel("Wertung")
                plt.ylabel("Häufigkeit")
                plt.title(caption)
                plt.savefig(f"experiments/{experiment}/rating_{key}.png")
