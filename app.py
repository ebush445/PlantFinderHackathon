from flask import Flask, request
from dotenv import load_dotenv
from helpers import get_environmental_impact, search_by_species

load_dotenv()

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/species/<speciesid>/zip/<zipcode>")
def environ_impact(speciesid, zipcode):
    response = get_environmental_impact(zipcode)
    return response.json()

@app.route("/search")
def get_by_species():
    species = request.args.get("species")
    response = search_by_species(species)
    return response.json()

if __name__ == "__main__":
    app.run(debug=True)
