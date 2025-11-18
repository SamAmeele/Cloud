Dit project toont een volledige IoT-dataketen voor een controller met joystick, knoppen en batterij.
Data wordt verzonden via MQTT, verwerkt in Node-RED, opgeslagen in InfluxDB en gevisualiseerd in zowel Node-RED Dashboard als InfluxDB.

Alles draait via Docker Compose.

Project starten

Project downloaden via:
git clone https://github.com/SamAmeele/Cloud.git
cd Cloud
Services starten:
docker compose up -d --build

Dit start automatisch:

MQTT Broker (Mosquitto)
Node-RED
InfluxDB v2
Controller-simulator (Python script dat elke seconde data stuurt)

Services stoppen:
docker compose down

Overzicht van services en URLs

Node-RED Editor
http://localhost:3501

Node-RED Dashboard
http://localhost:3501/ui

InfluxDB UI
http://localhost:3502

MQTT Broker
mqtt://localhost:3500

InfluxDB login
De logingegevens staan in docker-compose.yml en worden aangemaakt via deze variabelen:

DOCKER_INFLUXDB_INIT_USERNAME = admin
DOCKER_INFLUXDB_INIT_PASSWORD = Admin!234

Log in op:
http://localhost:3502
Organisatie: waarde uit DOCKER_INFLUXDB_INIT_ORG
Bucket: controller
Token: waarde van DOCKER_INFLUXDB_INIT_ADMIN_TOKEN
Node-RED gebruikt dezelfde token om data weg te schrijven.
MQTT data die wordt verzonden
De controller-simulator stuurt elke seconde een bericht naar het topic:
controller/telemetry

De payload bevat:
battery → batterijpercentage
jx → joystick X waarde (tussen -1 en 1)
jy → joystick Y waarde (tussen -1 en 1)
btnA → knop A (0 of 1)
btnB → knop B (0 of 1)

Node-RED (flows en dashboard)
Node-RED editor openen op:
http://localhost:3501
Node-RED bevat al flows die:
luisteren op MQTT topic controller/#

het JSON bericht opsplitsen in: batterij, joystick X/Y, knoppen
waarden naar InfluxDB schrijven

het dashboard aanmaken
Node-RED dashboard openen op:
http://localhost:3501/ui

Dit dashboard toont:
Live batterij gauge
Gemiddelde batterij via InfluxDB query
Joystick X-Y scatter die de laatste positie toont
Button A en B (status en historiek)

InfluxDB queries (Data Explorer)

Laatste status van een knop:
Open Data Explorer.
Selecteer bucket controller.
Filter measurement controller.
Filter field btnA of btnB.
Gebruik range start = -10m.
Sorteer op tijd in dalende volgorde.
Gebruik limit 1 om de meest recente waarde te krijgen.
Dit toont de laatste knopstatus.

In dashboard of grafiek betekent:
btnA = 1 is knop A ingedrukt.
btnA = 0 is knop A losgelaten.
btnB werkt op dezelfde manier.

Button B uitlezen:
Open Data Explorer.
Selecteer bucket controller.
Filter measurement controller.
Filter field btnB.
Kies een tijdsperiode, bijvoorbeeld range start = -1min.
De grafiek toont de status van knop B.

Gemiddelde batterij laatste minuut:
Open Data Explorer.
Selecteer bucket: controller.
Filter op measurement: controller.
Filter op field: battery.
Zet de tijdsperiode op: range start = -1h.
Gebruik daarna de functie mean om het gemiddelde te berekenen.
Dit toont het gemiddelde batterijpercentage van het laatste uur.

Gemiddelde batterij laatste 24 uur:
Open Data Explorer.
Selecteer bucket: controller.
Filter op measurement: controller.
Filter op field: battery.
Zet de tijdsperiode op: range start = -24h.
Gebruik mean om het gemiddelde te berekenen.
Dit toont het gemiddelde batterijpercentage van de laatste 24 uur.

Laatste joystickpositie (voor scatter X-Y):
Open Data Explorer.
Selecteer bucket: controller.
Filter op measurement: controller.
Filter op fields: jx en jy.
Tijdperiode instellen op range start = -10m.
Pivot uitvoeren zodat jx en jy in één record terechtkomen.
Sorteer op tijd, nieuwste bovenaan (sort descending).
Neem daarna slechts één record via limit 1.
Dit geeft de laatste joystickpositie.

Scatter-instellingen voor joystick X-Y:
X-as domain instellen van -1 tot 1.
X-as tick interval instellen op 0.5.
Y-as domain instellen van -1 tot 1.
Y-as tick interval instellen op 0.5.

Containers beheren

Herstarten van alle containers:
docker compose up -d --build

Stoppen:
docker compose down

Logs bekijken:
docker compose logs -f node-red
docker compose logs -f influxdb
docker compose logs -f mqtt-broker

Samenvatting (simpel)

Download repo via git clone
Start het project met docker compose up -d
Open Node-RED op localhost:3501
Open het dashboard op localhost:3501/ui
Open InfluxDB op localhost:3502
De controller-simulator stuurt automatisch data

Alles verschijnt live in het dashboard en InfluxDB
