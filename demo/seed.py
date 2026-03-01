#!/usr/bin/env python3
"""Pre-seed Home Assistant recorder database with 24h of historical sensor data."""

import json
import math
import os
import sqlite3
import time

def _default_db_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Inside the container seed.py lives at /config/seed.py
    if os.path.isfile(os.path.join(script_dir, "home-assistant_v2.db")):
        return os.path.join(script_dir, "home-assistant_v2.db")
    # Running locally from the demo/ directory
    return os.path.join(script_dir, "config", "home-assistant_v2.db")


DB_PATH = os.environ.get("DB_PATH", _default_db_path())
HOURS_BACK = 24
INTERVAL_MINUTES = 5
MARKER = "arctic_night_seeded"


def fnv1a_32(data: bytes) -> int:
    hash_val = 0x811C9DC5
    for byte in data:
        hash_val ^= byte
        hash_val = (hash_val * 0x01000193) & 0xFFFFFFFF
    return hash_val


def get_or_create_states_meta(cur, entity_id):
    cur.execute("SELECT metadata_id FROM states_meta WHERE entity_id = ?", (entity_id,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO states_meta (entity_id) VALUES (?)", (entity_id,))
    return cur.lastrowid


def get_or_create_state_attributes(cur, attrs_dict):
    attrs_json = json.dumps(attrs_dict, separators=(",", ":"), sort_keys=True)
    attrs_bytes = attrs_json.encode("utf-8")
    hash_val = fnv1a_32(attrs_bytes)
    cur.execute(
        "SELECT attributes_id FROM state_attributes WHERE hash = ? AND shared_attrs = ?",
        (hash_val, attrs_json),
    )
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        "INSERT INTO state_attributes (hash, shared_attrs) VALUES (?, ?)",
        (hash_val, attrs_json),
    )
    return cur.lastrowid


def get_or_create_statistics_meta(cur, statistic_id, unit, has_mean, has_sum):
    cur.execute(
        "SELECT id FROM statistics_meta WHERE statistic_id = ?", (statistic_id,)
    )
    row = cur.fetchone()
    if row:
        return row[0]
    # Detect schema: HA 2026.2+ has mean_type column
    cur.execute("PRAGMA table_info(statistics_meta)")
    columns = {row[1] for row in cur.fetchall()}
    if "mean_type" in columns:
        mean_type = 1 if has_mean else 0
        cur.execute(
            "INSERT INTO statistics_meta (statistic_id, source, unit_of_measurement, has_sum, mean_type, name) "
            "VALUES (?, 'recorder', ?, ?, ?, NULL)",
            (statistic_id, unit, has_sum, mean_type),
        )
    else:
        cur.execute(
            "INSERT INTO statistics_meta (statistic_id, source, unit_of_measurement, has_mean, has_sum, name) "
            "VALUES (?, 'recorder', ?, ?, ?, NULL)",
            (statistic_id, unit, has_mean, has_sum),
        )
    return cur.lastrowid


def temp_value(hour_of_day):
    """Diurnal temperature curve: ~5C at 05:00, ~20C at 14:00."""
    base = 12.0
    amplitude = 8.0
    val = base + amplitude * math.sin((hour_of_day - 8) * math.pi / 12)
    val += math.sin(hour_of_day * 7.3) * 0.5
    return round(val, 1)


def humidity_value(hour_of_day):
    """Roughly inverse of temperature: ~80% at night, ~50% midday."""
    base = 65.0
    amplitude = 15.0
    val = base - amplitude * math.sin((hour_of_day - 8) * math.pi / 12)
    val += math.sin(hour_of_day * 5.1) * 2
    return round(max(30, min(95, val)), 0)


SENSORS = [
    {
        "entity_id": "sensor.outside_temperature",
        "attrs": {
            "device_class": "temperature",
            "friendly_name": "Outside Temperature",
            "state_class": "measurement",
            "unit_of_measurement": "\u00b0C",
        },
        "unit": "\u00b0C",
        "value_fn": temp_value,
        "fmt": lambda v: str(v),
    },
    {
        "entity_id": "sensor.outside_humidity",
        "attrs": {
            "device_class": "humidity",
            "friendly_name": "Outside Humidity",
            "state_class": "measurement",
            "unit_of_measurement": "%",
        },
        "unit": "%",
        "value_fn": humidity_value,
        "fmt": lambda v: str(int(v)),
    },
]


def is_seeded(cur):
    """Check if we already seeded by looking for our marker table."""
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (MARKER,)
    )
    return cur.fetchone() is not None


def mark_seeded(cur):
    cur.execute(f"CREATE TABLE IF NOT EXISTS {MARKER} (ts FLOAT)")
    cur.execute(f"INSERT INTO {MARKER} VALUES (?)", (time.time(),))


def wait_for_db(timeout=120):
    """Wait for HA to create the database and its tables."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if not os.path.exists(DB_PATH):
            time.sleep(2)
            continue
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT count(*) FROM states_meta")
            conn.close()
            return True
        except sqlite3.OperationalError:
            time.sleep(2)
    return False


def seed():
    print(f"Waiting for database at {DB_PATH} ...")
    if not wait_for_db():
        print("Timed out waiting for database.")
        raise SystemExit(1)

    # Give HA a moment to finish registering demo entities
    time.sleep(10)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if is_seeded(cur):
        print("Already seeded, skipping.")
        conn.close()
        return
    now = time.time()
    start_ts = now - HOURS_BACK * 3600
    interval_secs = INTERVAL_MINUTES * 60
    num_points = int((HOURS_BACK * 3600) / interval_secs)

    for sensor in SENSORS:
        entity_id = sensor["entity_id"]
        print(f"Seeding {entity_id} ...")

        metadata_id = get_or_create_states_meta(cur, entity_id)
        attributes_id = get_or_create_state_attributes(cur, sensor["attrs"])
        stats_meta_id = get_or_create_statistics_meta(
            cur, entity_id, sensor["unit"], has_mean=True, has_sum=False
        )

        # Clear existing rows for a clean seed
        cur.execute("DELETE FROM states WHERE metadata_id = ?", (metadata_id,))
        cur.execute(
            "DELETE FROM statistics_short_term WHERE metadata_id = ?", (stats_meta_id,)
        )
        cur.execute("DELETE FROM statistics WHERE metadata_id = ?", (stats_meta_id,))

        prev_state_id = None
        prev_state_str = None
        five_min = {}
        one_hour = {}

        for i in range(num_points + 1):
            ts = start_ts + i * interval_secs
            hour_of_day = (ts % 86400) / 3600
            value = sensor["value_fn"](hour_of_day)
            state_str = sensor["fmt"](value)

            last_changed_ts = ts if state_str != prev_state_str else None

            cur.execute(
                "INSERT INTO states "
                "(state, last_changed_ts, last_reported_ts, last_updated_ts, "
                "old_state_id, attributes_id, origin_idx, metadata_id, "
                "context_id_bin, context_user_id_bin, context_parent_id_bin) "
                "VALUES (?, ?, ?, ?, ?, ?, 0, ?, NULL, NULL, NULL)",
                (state_str, last_changed_ts, ts, ts, prev_state_id, attributes_id, metadata_id),
            )
            prev_state_id = cur.lastrowid
            prev_state_str = state_str

            bucket_5 = ts - (ts % 300)
            five_min.setdefault(bucket_5, []).append(value)
            bucket_60 = ts - (ts % 3600)
            one_hour.setdefault(bucket_60, []).append(value)

        for bucket_ts, vals in sorted(five_min.items()):
            cur.execute(
                "INSERT INTO statistics_short_term "
                "(created_ts, metadata_id, start_ts, mean, min, max, "
                "last_reset_ts, state, sum) "
                "VALUES (?, ?, ?, ?, ?, ?, NULL, NULL, NULL)",
                (
                    bucket_ts + 300,
                    stats_meta_id,
                    bucket_ts,
                    round(sum(vals) / len(vals), 2),
                    round(min(vals), 2),
                    round(max(vals), 2),
                ),
            )

        for bucket_ts, vals in sorted(one_hour.items()):
            cur.execute(
                "INSERT INTO statistics "
                "(created_ts, metadata_id, start_ts, mean, min, max, "
                "last_reset_ts, state, sum) "
                "VALUES (?, ?, ?, ?, ?, ?, NULL, NULL, NULL)",
                (
                    bucket_ts + 3600,
                    stats_meta_id,
                    bucket_ts,
                    round(sum(vals) / len(vals), 2),
                    round(min(vals), 2),
                    round(max(vals), 2),
                ),
            )

        print(f"  {num_points + 1} states, {len(five_min)} short-term stats, {len(one_hour)} long-term stats")

    mark_seeded(cur)
    conn.commit()
    conn.close()
    print("Done! Refresh the dashboard to see graph data.")


if __name__ == "__main__":
    seed()
