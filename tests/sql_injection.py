# tests/sql_injection.py

import requests

BASE_URL = "http://localhost:5000"

def test_sql_injection_bypass():
    payload = "' OR '1'='1"

    r = requests.post(f"{BASE_URL}/login", data={
        "username": payload,
        "password": payload
    })

    assert r.status_code == 200
    print(r.json())
    