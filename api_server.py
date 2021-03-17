# TODO: allow flask to handle async function
import flask
import requests_cache
from flask import request
import traceback
from flask import Response
import json
import scraper

requests_cache.install_cache('requests_cache')

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=["GET"])
def getSites():
    sites = ["1337x", "tpb", "Ettvdl", "Rarbg", 'nyaa']
    return Response(json.dumps({"sites": sites}), mimetype='application/json')


@app.route('/getTorrents', methods=["GET"])
def getTorrents():
    query = request.args.get("query")
    if(query is None or query == ""):
        return Response(json.dumps("Invalid Request"))
    site = request.args.get("site")
    try:
        if(site == "1337x"):
            return Response(json.dumps({"torrents": scraper.search1337x(query)}), mimetype="application/json")
        elif(site == "nyaa"):
            return Response(json.dumps({'torrents': scraper.searchNyaa(query)}), mimetype="application/json")
        elif(site == "tpb"):
            return Response(json.dumps({"torrents": scraper.searchTPB(query)}), mimetype="application/json")
        elif(site == "Rarbg"):
            return Response(json.dumps({"torrents": scraper.searchRarbg(query)}), mimetype="application/json")
        elif(site == "Ettvdl"):
            return Response(json.dumps({"torrents": scraper.searchEttv(query)}), mimetype="application/json")
        else:
            return Response(json.dumps({"torrents": scraper.search1337x(query)}), mimetype="application/json")
    except Exception as e:
        print(traceback.format_exc())
        return Response(json.dumps("Invalid Request"))
