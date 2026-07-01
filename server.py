import os
import json
import threading
import time
import queue
from datetime import datetime
from flask import Flask, render_template, jsonify, request, Response, stream_with_context
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

ACCOUNTS_FILE = "accounts.json"

log_queue = queue.Queue(maxsize=500)
bot_status = {}
bot_threads = {}
active_team_code = None

def load_accounts():
    try:
        if os.path.exists(ACCOUNTS_FILE):
            with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        add_log(f"Gagal baca accounts.json: {e}", "error")
    return []

def add_log(message, level="info"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = {"time": timestamp, "msg": message, "level": level}
    try:
        log_queue.put_nowait(entry)
    except queue.Full:
        log_queue.get_nowait()
        log_queue.put_nowait(entry)

def run_bot(uid, password, name):
    try:
        add_log(f"[{name}] Menghubungkan...", "info")
        bot_status[uid] = "connecting"
        from app import FF_CLIENT
        bot_status[uid] = "online"
        add_log(f"[{name}] Bot online!", "success")
        FF_CLIENT(uid, password)
    except Exception as e:
        bot_status[uid] = "error"
        add_log(f"[{name}] Error: {str(e)}", "error")

@app.route("/")
def index():
    accounts = load_accounts()
    return render_template("index.html", accounts=accounts)

@app.route("/api/accounts")
def api_accounts():
    accounts = load_accounts()
    for acc in accounts:
        uid = acc.get("uid")
        acc["status"] = bot_status.get(uid, "offline")
    return jsonify(accounts)

@app.route("/api/start/<uid>", methods=["POST"])
def start_bot(uid):
    accounts = load_accounts()
    acc = next((a for a in accounts if a["uid"] == uid), None)
    if not acc:
        return jsonify({"ok": False, "msg": "Akun tidak ditemukan"})
    if bot_status.get(uid) in ("online", "connecting"):
        return jsonify({"ok": False, "msg": "Bot sudah berjalan"})
    t = threading.Thread(
        target=run_bot,
        args=(acc["uid"], acc["password"], acc["name"]),
        daemon=True
    )
    bot_threads[uid] = t
    t.start()
    return jsonify({"ok": True, "msg": f"Bot {acc['name']} dimulai"})

@app.route("/api/stop/<uid>", methods=["POST"])
def stop_bot(uid):
    bot_status[uid] = "offline"
    add_log(f"[UID:{uid}] Bot dihentikan", "warning")
    return jsonify({"ok": True, "msg": "Bot dihentikan"})

@app.route("/api/start-all", methods=["POST"])
def start_all():
    accounts = load_accounts()
    started = 0
    for acc in accounts:
        uid = acc["uid"]
        if bot_status.get(uid) in ("online", "connecting"):
            continue
        t = threading.Thread(
            target=run_bot,
            args=(acc["uid"], acc["password"], acc["name"]),
            daemon=True
        )
        bot_threads[uid] = t
        t.start()
        started += 1
        time.sleep(0.3)
    add_log(f"{started} bot dimulai sekaligus", "success")
    return jsonify({"ok": True, "msg": f"{started} bot dimulai"})

@app.route("/api/stop-all", methods=["POST"])
def stop_all():
    accounts = load_accounts()
    for acc in accounts:
        uid = acc["uid"]
        if bot_status.get(uid) in ("online", "connecting"):
            bot_status[uid] = "offline"
    add_log("Semua bot dihentikan", "warning")
    return jsonify({"ok": True, "msg": "Semua bot dihentikan"})

@app.route("/api/teamcode", methods=["POST"])
def set_teamcode():
    global active_team_code
    data = request.json or {}
    code = data.get("code", "").strip()
    if not code.isdigit():
        return jsonify({"ok": False, "msg": "Team code harus angka"})
    active_team_code = code
    add_log(f"Team code diset: {code} — kirim /lw di game untuk aktivasi", "success")
    return jsonify({"ok": True, "msg": f"Team code {code} aktif"})

@app.route("/api/status")
def api_status():
    accounts = load_accounts()
    total = len(accounts)
    online = sum(1 for a in accounts if bot_status.get(a["uid"]) == "online")
    connecting = sum(1 for a in accounts if bot_status.get(a["uid"]) == "connecting")
    return jsonify({
        "total": total,
        "online": online,
        "connecting": connecting,
        "offline": total - online - connecting,
        "team_code": active_team_code
    })

@app.route("/api/logs")
def stream_logs():
    def generate():
        while True:
            try:
                entry = log_queue.get(timeout=15)
                yield f"data: {json.dumps(entry)}\n\n"
            except queue.Empty:
                yield f"data: {json.dumps({'ping': True})}\n\n"
    return Response(stream_with_context(generate()), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

if __name__ == "__main__":
    add_log("🔥 Free Fire Bot Dashboard dimulai", "success")
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
