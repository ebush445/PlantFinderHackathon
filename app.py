from flask import Flask, request, render_template
from dotenv import load_dotenv
from helpers import get_environmental_impact, search_by_species, get_reccommended_plants

load_dotenv()

app = Flask(__name__)


@app.route("/species/<speciesid>/zip/<zipcode>")
def environ_impact(zipcode):
    response = get_environmental_impact(zipcode)
    return response.json()

@app.route("/", methods=["GET", "POST"])
def get_by_species():
    if request.method == "POST":
        species_name = request.form.get('species')
        state_code = request.form.get('state_code')
        hardiness_index = request.form.get('hardiness_index')
        species = search_by_species(species_name)
        result = get_reccommended_plants(state_code, hardiness_index)
        return render_template("index.html", species=species, result=result)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
