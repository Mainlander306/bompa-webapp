#!/usr/bin/env python3
import sqlite3
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

DB = "/home/mainlander/oly_progress.db"
app = Flask(__name__)
CORS(app)


def get_db():
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id      INTEGER PRIMARY KEY CHECK (id = 1),
            sets    TEXT NOT NULL DEFAULT '{}',
            workouts TEXT NOT NULL DEFAULT '{}'
        )
    """)
    conn.execute("INSERT OR IGNORE INTO progress (id, sets, workouts) VALUES (1, '{}', '{}')")
    conn.commit()
    return conn


@app.get("/progress")
def get_progress():
    conn = get_db()
    row = conn.execute("SELECT sets, workouts FROM progress WHERE id = 1").fetchone()
    conn.close()
    return jsonify({"sets": json.loads(row[0]), "workouts": json.loads(row[1])})


@app.post("/progress")
def save_progress():
    data = request.get_json(force=True)
    sets = json.dumps(data.get("sets", {}))
    workouts = json.dumps(data.get("workouts", {}))
    conn = get_db()
    conn.execute("UPDATE progress SET sets = ?, workouts = ? WHERE id = 1", (sets, workouts))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
