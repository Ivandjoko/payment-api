from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/solde', methods=['GET'])
def get_solde():
    return jsonify({
        "compte": "FR76-XXXX-XXXX-XXXX",
        "solde": 1000000.30,
        "devise": "EUR"
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200


# Justification : le container doit écouter sur toutes ses interfaces pour que
# le Service Kubernetes puisse l'atteindre. L'exposition réelle est contrôlée
# par Kubernetes (Service, NetworkPolicy) et le Security Group, pas par Flask.


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
