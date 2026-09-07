import json
import logging
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from ghostme.device import list_devices, reset_location, set_location

logger = logging.getLogger(__name__)

app = Flask(
    __name__,
    template_folder=str(Path(__file__).parent / "templates"),
    static_folder=str(Path(__file__).parent / "static"),
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/devices", methods=["GET"])
def api_devices():
    try:
        devices = list_devices()
        return jsonify({
            "success": True,
            "devices": [
                {
                    "udid": d.udid,
                    "name": d.name,
                    "model": d.model,
                    "ios_version": d.ios_version,
                }
                for d in devices
            ],
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/set-location", methods=["POST"])
def api_set_location():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No JSON body"}), 400

    lat = data.get("lat")
    lon = data.get("lon")
    udid = data.get("udid")

    if lat is None or lon is None:
        return jsonify({"success": False, "error": "lat and lon are required"}), 400

    try:
        lat = float(lat)
        lon = float(lon)
    except (ValueError, TypeError):
        return jsonify({"success": False, "error": "lat and lon must be numbers"}), 400

    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        return jsonify({"success": False, "error": "Invalid coordinates"}), 400

    try:
        result = set_location(lat, lon, udid)
        return jsonify(result)
    except ConnectionError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/reset-location", methods=["POST"])
def api_reset_location():
    data = request.get_json() or {}
    udid = data.get("udid")

    try:
        result = reset_location(udid)
        return jsonify(result)
    except ConnectionError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/favorites", methods=["GET"])
def api_get_favorites():
    fav_path = Path.home() / ".ghostme" / "favorites.json"
    if fav_path.exists():
        favorites = json.loads(fav_path.read_text())
    else:
        favorites = []
    return jsonify({"success": True, "favorites": favorites})


@app.route("/api/favorites", methods=["POST"])
def api_save_favorite():
    data = request.get_json()
    if not data or "name" not in data or "lat" not in data or "lon" not in data:
        return jsonify({"success": False, "error": "name, lat, and lon required"}), 400

    fav_dir = Path.home() / ".ghostme"
    fav_dir.mkdir(exist_ok=True)
    fav_path = fav_dir / "favorites.json"

    if fav_path.exists():
        favorites = json.loads(fav_path.read_text())
    else:
        favorites = []

    favorites.append({
        "name": str(data["name"])[:100],
        "lat": float(data["lat"]),
        "lon": float(data["lon"]),
    })

    fav_path.write_text(json.dumps(favorites, indent=2))
    return jsonify({"success": True, "favorites": favorites})


@app.route("/api/favorites/<int:idx>", methods=["DELETE"])
def api_delete_favorite(idx):
    fav_path = Path.home() / ".ghostme" / "favorites.json"
    if not fav_path.exists():
        return jsonify({"success": False, "error": "No favorites"}), 404

    favorites = json.loads(fav_path.read_text())
    if idx < 0 or idx >= len(favorites):
        return jsonify({"success": False, "error": "Invalid index"}), 400

    favorites.pop(idx)
    fav_path.write_text(json.dumps(favorites, indent=2))
    return jsonify({"success": True, "favorites": favorites})


def run(host="127.0.0.1", port=5000, debug=False):
    app.run(host=host, port=port, debug=debug)
