#este archivo sirve para relacionar el script de Python con las herramientas de desarrollo web.
import json
from flask import Flask, render_template, request, jsonify
from hillclimbing import getInputs, getInputsCountries, graph

app = Flask(__name__)

coords=[]

#se hace routing de la página principal de la interfaz
@app.route("/")
def index():
    return render_template("index.html")

#se obtienen las entradas puestas por el usuario
#se mandan los datos al archivo hillclimbing.py 
#se despliegan los resultados
@app.route("/calcular", methods=['POST'])
def inputUsuario():
    coords = getInputs(request.form.getlist('country'))
    countryCoords = getInputsCountries(request.form.getlist('country'))
    sol = graph(coords, countryCoords)
    solNum = sol[0]
    solCountry = sol[1]
    solLength = sol[2]
    return render_template("index.html",solNum=solNum,solCountry=solCountry,solLength=solLength)

#se actualiza la imagen del grafo obtenida. 
@app.route('/get_img', methods = ['GET'])
def get_img():
    img = '../static/imgs/img1.png'
    return jsonify({'img':img}) 

#se elimina el cache del framework para que se actualice la imagen de forma efectiva.
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
