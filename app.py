from flask import Flask, render_template, request
from hillclimbing import getInputs, getInputsCountries, graph

app = Flask(__name__)

coords=[]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calcular", methods=['POST'])
def inputUsuario():
    coords = getInputs(request.form.getlist('country'))
    countryCoords = getInputsCountries(request.form.getlist('country'))
    #print("The coords you selected:",coords)
    sol = graph(coords, countryCoords)
    solNum = sol[0]
    solCountry = sol[1]
    return render_template("index.html",solNum=solNum,solCountry=solCountry)

if __name__ == "__main__":
    app.run(debug=True)
