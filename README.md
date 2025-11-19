ADit project toont een volledige IoT-dataketen voor een controller met joystick, knoppen en batterij. Data wordt verzonden via MQTT, verwerkt in Node-RED, opgeslagen in InfluxDB en gevisualiseerd in zowel Node-RED Dashboard als InfluxDB. Alles draait via Docker Compose.

PROJECT STARTEN

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
Portainer (Docker beheeromgeving)

Services stoppen:
docker compose down

OVERZICHT VAN SERVICES EN URLS

Node-RED Editor:
http://localhost:3501

Node-RED Dashboard:
http://localhost:3501/ui

InfluxDB UI:
http://localhost:3502

MQTT Broker:
mqtt://localhost:3500

Portainer (Docker beheeromgeving):
https://localhost:5004

of
http://localhost:5005

INFLUXDB LOGIN

De logingegevens staan in docker-compose.yml en worden aangemaakt via deze variabelen:
DOCKER_INFLUXDB_INIT_USERNAME = admin
DOCKER_INFLUXDB_INIT_PASSWORD = Admin!234

Log in op:
http://localhost:3502

Organisatie: waarde uit DOCKER_INFLUXDB_INIT_ORG (ameel)
Bucket: controller
Token: waarde van DOCKER_INFLUXDB_INIT_ADMIN_TOKEN

Node-RED gebruikt dezelfde token om data weg te schrijven.

MQTT DATA DIE WORDT VERZONDEN

De controller-simulator stuurt elke seconde een bericht naar het topic:
controller/telemetry

De payload bevat:
battery → batterijpercentage
jx → joystick X waarde (tussen -1 en 1)
jy → joystick Y waarde (tussen -1 en 1)
btnA → knop A (0 of 1)
btnB → knop B (0 of 1)

NODE-RED (FLOWS EN DASHBOARD)

Node-RED openen op:
http://localhost:3501

Node-RED bevat al flows die luisteren op MQTT topic controller/#. Het JSON-bericht wordt opgesplitst in batterij, joystick X/Y en knoppen. De waarden worden daarna naar InfluxDB geschreven en gebruikt in het dashboard.

Node-RED dashboard openen op:
http://localhost:3501/ui

Het dashboard toont:
Live batterij gauge
Gemiddelde batterij via InfluxDB query
Joystick X-Y scatter (laatste positie)
Button A en B (status + historiek)

INFLUXDB QUERIES (DATA EXPLORER)

Laatste status van een knop:
Open Data Explorer
Selecteer bucket controller
Filter measurement controller
Filter field btnA of btnB
Range instellen op start = -10m
Sorteren op tijd in dalende volgorde
limit 1 nemen voor de laatste waarde

btnA = 1 betekent knop A ingedrukt
btnA = 0 betekent knop A losgelaten
btnB werkt identiek

Button B uitlezen:
Open Data Explorer
Selecteer bucket controller
Filter measurement controller
Filter field btnB
Tijdsperiode bijv. range start = -1min
Grafiek toont statusveranderingen

Gemiddelde batterij laatste minuut:
Open Data Explorer
Selecteer bucket controller
Filter measurement controller
Filter field battery
Range start = -1h
Gebruik mean om het gemiddelde te berekenen

Gemiddelde batterij laatste 24 uur:
Range start = -24h
Filter measurement controller
Filter field battery
Gebruik mean als aggregatie

Laatste joystickpositie voor X-Y scatter:
Open Data Explorer
Selecteer bucket controller
Filter measurement controller
Filter fields jx en jy
Range start = -10m
Pivot uitvoeren zodat jx en jy in één rij staan
Sorteren op tijd (nieuwste eerst)
limit 1 nemen

Scatter-instellingen voor joystick:
X-as domain instellen van -1 tot 1
X-as interval instellen op 0.5
Y-as domain instellen van -1 tot 1
Y-as interval instellen op 0.5

PORTAINER (DOCKER BEHEER)

Portainer is een webinterface om Docker containers te beheren. Het maakt het eenvoudig om te zien welke containers draaien en om logs, poorten en status te controleren. Portainer wordt in dit project automatisch opgestart via docker-compose.

Portainer openen kan via:
https://localhost:5004/#!/3/docker/networks/taak_cloud_sensor-net

of
http://localhost:5005/#!/3/docker/networks/taak_cloud_sensor-net

Bij de eerste keer openen werd een admin gebruiker aangemaakt.
Het ingestelde wachtwoord is:
123456789123

In Portainer zie je de containers van dit project:
mqtt-broker
controller-sim
node-red
influxdb
portainer

Portainer helpt bij:
Controleren van containerstatus
Bekijken van logs
Starten en stoppen van containers
Controleren van poorten zoals 3500, 3501, 3502 en 5004
Nakijken of de volledige IoT stack correct draait

Doordat Portainer in docker-compose is opgenomen, start het automatisch mee met:
docker compose up -d

CONTAINERS BEHEREN

Herstarten van alle containers:
docker compose up -d --build

Stoppen:
docker compose down

Logs bekijken:
docker compose logs -f node-red
docker compose logs -f influxdb
docker compose logs -f mqtt-broker

SAMENVATTING

Download de repo via git clone
Start het project met docker compose up -d
Open Node-RED op localhost:3501
Open het dashboard op localhost:3501/ui
Open InfluxDB op localhost:3502
Open Portainer op localhost:5004
De controller-simulator stuurt automatisch data
Alles verschijnt live in het dashboard en in InfluxDB