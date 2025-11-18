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

DOCKER_INFLUXDB_INIT_USERNAME
DOCKER_INFLUXDB_INIT_PASSWORD
DOCKER_INFLUXDB_INIT_ORG
DOCKER_INFLUXDB_INIT_BUCKET
DOCKER_INFLUXDB_INIT_ADMIN_TOKEN

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

Joystick X en Y grafieken

Joystick X-Y scatter die de laatste positie toont

Button A en B (status en historiek)

InfluxDB queries (Data Explorer)

Gemiddelde batterij laatste uur:
Filter measurement “controller”, field “battery”, range -1h, daarna mean.

Gemiddelde batterij laatste 24 uur:
Filter measurement “controller”, field “battery”, range -24h, mean.

Laatste joystickpositie (voor scatter X-Y):
Range -10m
Measurement controller
Fields jx en jy
Pivot jx en jy tot één record
Sorteren op tijd (desc)
Limit 1

Scatter-instellingen:
X-as domain -1 tot 1, tick interval 0.5
Y-as domain -1 tot 1, tick interval 0.5

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