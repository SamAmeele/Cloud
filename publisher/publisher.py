import paho.mqtt.client as mqtt
import time, json, random, os

broker = os.getenv("HOST", "mosquitto")
port = int(os.getenv("PORT", "3500"))
interval = float(os.getenv("INTERVAL", "0.2"))
client_id = "controller-sim"

client = mqtt.Client(client_id)

while True:
    try:
        # probeer verbinding te maken (max. 3 s)
        client.connect(broker, port, 60)
        print(f"🔌 Connected to MQTT broker at {broker}:{port}")
        break
    except Exception as e:
        print(f"⚠️  MQTT connect failed ({e}), retrying in 2s...")
        time.sleep(2)

# blijf publiceren, en herconnect indien fout
while True:
    try:
        # willekeurige controllerdata
        jx = random.uniform(-1, 1)
        jy = random.uniform(-1, 1)
        payload = {
            "device_id": "ctrl-001",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "joystick": {"x": jx, "y": jy},
            "buttons": {"A": random.choice([True, False]),
                        "B": random.choice([True, False])},
            "battery": random.uniform(0, 100)
        }
        client.publish("controller/telemetry", json.dumps(payload))
        time.sleep(interval)

    except Exception as e:
        print(f"⚠️  Publish error ({e}), reconnecting...")
        try:
            client.reconnect()
            print("✅ Reconnected.")
        except Exception as e2:
            print(f"❌ Reconnect failed ({e2}), retrying in 3s...")
            time.sleep(3)
