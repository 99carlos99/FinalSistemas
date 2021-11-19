import json
from flask import Flask, render_template, request, jsonify
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
    sol = graph(coords, countryCoords)
    solNum = sol[0]
    solCountry = sol[1]
    solLength = sol[2]
    return render_template("index.html",solNum=solNum,solCountry=solCountry,solLength=solLength)

@app.route('/get_img', methods = ['GET'])
def get_img():
    img = '../static/imgs/img1.png'
    return jsonify({'img':img}) 

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == "__main__":
    app.run(debug=True)
