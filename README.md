# Jules Celestia

Jules Celestia ist ein ChatBot. Ein Experiment für Jugend forscht 2024. Jules ist einen wiedergeborenen Julius Caesar mit Spezialwissen aus Caesars Büchern.
Jules antwortet in Jugendsprache und soll Spaß machen.

Aktuell ist Jules als Web-App umgesetzt.
Ein Screenshot siehst du hier:

![Screenshot](https://github.com/manitaro/jules.celestia/blob/e5ef22447a9cf7a96e31d48d5c81f16d0ff149b1/images/screenshot.png?raw=true)

Du kannst direkt mit Jules chatten. Wenn du dich über bestimmte Kapitel in Julius Caesar seinem Leben interessierst, dann kannst du diese Bücher / das Spezialwissen anklicken, dann wird es für die Antwort berücksichtigt. So kannst du auch erleben wie sich Caesar von Krieg zu Krieg entwickelt hat.

## Ziele

Ich hatte die folgenden 5 Ziele bei der Entwicklung und dem Design des Chatbots.

### Jugendsprachlichkeit

Jules soll locker antworten.

![Jugendsprache](https://github.com/manitaro/jules.celestia/blob/e5ef22447a9cf7a96e31d48d5c81f16d0ff149b1/images/chat_jugendsprache.png)

### Historische Fakten

Jules soll historische Fakten einbinden.

![Jugendsprache](https://github.com/manitaro/jules.celestia/blob/e5ef22447a9cf7a96e31d48d5c81f16d0ff149b1/images/chat_historie.png)

### Zitate und Weisheiten

Jules soll Zitate nutzen.

![Jugendsprache](https://github.com/manitaro/jules.celestia/blob/e5ef22447a9cf7a96e31d48d5c81f16d0ff149b1/images/chat_zitate.png)

### Lateinische Wörter

Jules soll spielend Latein in Antworten einflechten.

![Jugendsprache](https://github.com/manitaro/jules.celestia/blob/e5ef22447a9cf7a96e31d48d5c81f16d0ff149b1/images/chat_latein.png)

### Fakten von Caesar

Jules soll Fakten von Caesar berichten.

![Fakten](https://github.com/manitaro/jules.celestia/blob/e5ef22447a9cf7a96e31d48d5c81f16d0ff149b1/images/chat_fakten.png)

## Wie funktioniert das?

Der Code ist in 3 Teile aufgetrennt.

* _rag.py_ - hier ist sämtlicher LLM Code enthalten
* _jules_celestia.py_ - hier ist die Web App von Jules enthalten
* _improve.py_ - hier ist das Skript um Experimente mit LLMs durchzuführen
  * _violin.py_ - ist nur eine Hilfdatei um die Experimente in Violin-Plots auswerten zu können 

### rag.py

Hier ist sämtlicher Code um das LLM zu nutzen. Sowohl per Retrieval-Augmented Generation (RAG) oder auch direkt. Hier werden auch Bücher per Vector Encoding / Word embedding indiziert.
Es wird _llama_index_ genutzt.

### jules_celestia.py

Hier ist sämtlicher Code für die Web-App, die du oben im Screenshot gesehen hast. Dazu habe ich _streamlit_ genutzt. _Streamlit_ erlaubt es einfach Web-Apps zu erstellen.
Enthalten sind auch Referenzen auf Doku und technische Details.

### improve.py

Hier ist der Experimentiercode. Ändere dein Prompt in _rag.py_ ab und führe dann _improve.py_ aus. Dein neuer Prompt wird dann bewertet. Werden die Ergebnisse besser, dann nutze deinen neuen Prompt, ansonsten geh zurück zu deinem alten Prompt.

## Was ist sonst noch im Repository?

### store/

Hier sind Caesars Bücher. In indizierter Form, so dass sie direkt von _rag.py_ genutzt werden können.

### experiments/

Dort sind alle 6 Experimente aus der Jugend forscht Arbeit. Bis zu 5.000 Durchläufe. Erste Analysen sind in meiner Jugend forscht Arbeit dazu.

### ci

Ein Skript um den Code zu prüfen und zu formatieren.

### Dockerfile

## Feedback

Probiere gerne den Bot aus, gibt mir Feedback. Entweder direkt oder per Github Issue.
Danke.

Eine Möglichkeit den Bot nicht lokal, sondern reproduzierbarer und abgeschotteter in einem Docker container laufen zu lassen. Dort werden dann alle nötigen Details installiert.

