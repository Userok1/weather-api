#!/usr/bin/env python

from flask import Flask, make_response, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app.src.dependencies import send_request

app_flask = Flask(__name__)
limiter = Limiter(
    get_remote_address, # client ip adress as key
    app=app_flask,
    default_limits=["200 per day", "50 per hour"], # Global limits
    storage_uri="memory://",
)


@app_flask.route("/custom-error")
def custom_error():
    response = make_response("<h1>Page not found</h1>", 404)
    response.headers['X-Custom-Header'] = 'Error'
    return response


@app_flask.get("/")
def root():
    return "<h>API is working!/h" 


@app_flask.get("/favicon.ico")
def favicon():
    return "", 204  # No Content


@app_flask.get("/<city>")
@limiter.limit("10 per minute")
def get_weather_by_city(city: str, exp: int = 300):
    data = send_request(city, exp=exp)
    if not data:
        return jsonify({"error": "Data not found"}), 404
    return data
    

if __name__ == "__main__":
    app_flask.run()