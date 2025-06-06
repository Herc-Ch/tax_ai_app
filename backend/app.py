from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory store (for demonstration)
tax_data = {}


@app.route("/api/submit-tax", methods=["GET", "POST", "PUT", "DELETE"])
def submit_tax():
    if request.method == "POST":
        data = request.json
        name = data.get("name", "Unknown")
        # Save/overwrite user data (using 'name' as a simple key)
        tax_data[name] = data
        response = {"message": f"Received tax info for {name}.", "received": data}
        return jsonify(response), 201

    elif request.method == "GET":
        # Return all tax data (for demonstration)
        return jsonify(list(tax_data.values())), 200

    elif request.method == "PUT":
        data = request.json
        name = data.get("name")
        if name and name in tax_data:
            tax_data[name] = data  # Update existing entry
            return jsonify({"message": f"Updated tax info for {name}."}), 200
        else:
            return jsonify({"error": "Name not found"}), 404

    elif request.method == "DELETE":
        name = request.args.get("name")
        if name and name in tax_data:
            del tax_data[name]
            return jsonify({"message": f"Deleted tax info for {name}."}), 200
        else:
            return jsonify({"error": "Name not found"}), 404


if __name__ == "__main__":
    app.run(port=5000, debug=True)
