import random
from typing import final
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

#Conla finalidad que los países seleccionados se muestren en orden,
#se ponen sus siglas en su orden de aparición en el .txt
countries = ['mx','ar','bo','br','cl','co','cr','cu','do','ec','gt','hn','ht','pr','sv','tt','ur','ni','pa','pe','py']


#Lee archivo txt con las coordenadas de los paises
def getInputs(inp):
    data = []
    newdata = []
    with open('paises2.txt') as my_file:      
        for line in my_file:  
            data.append([list(map(float ,x.split(','))) for x in line.split(' ')])

        #se toman los inputs del usuario y se arma una lista con sus coordenadas correspondientes
        for i in range(len(inp)):
            newdata.append(data[int(inp[i])])

    #los datos obtenidos se toman en cuenta para la lista de coordenadas oficiales. 
    coords = np.array(newdata)
    return coords

#Se agregan las siglas de los países correspondientes a los escogidos por el usuario.
def getInputsCountries(inp):
    countryIndex = []
    for i in range(len(inp)):
        countryIndex.append(countries[int(inp[i])])
    
    return countryIndex

#Este metodo genera la matriz de adyacencia de los pesos del grapho obteniendo la distancia Euclideana de las coordenadas
def createAdyacencyMatrix(coords):
    matrix = []
    for i in range(len(coords)):
        for j in range(len(coords)) :       
            p = np.linalg.norm(coords[i] - coords[j])
            matrix.append(p)
    matrix = np.reshape(matrix, (len(coords),len(coords)))
    #print("The matrix: ",matrix)
    return matrix

#Este metodo genera una solucion random para evitar generar todas las posibles combinaciones de una, escogemos una random    
def randomSolution(matrix):
    countriesPoints= list(range(0, len(matrix)))
    solutionArray = []
    for i in range(0, len(matrix)):
        randomPoint = countriesPoints[random.randint(0, len( countriesPoints) - 1)]
        solutionArray .append(randomPoint)
        countriesPoints.remove(randomPoint)
    return solutionArray 

#Este metodo obtiene la longitud del camino de la solucion random escogida
def createPathlength(matrix, randSolution):
    pathLength = 0
    for i in range(0, len(randSolution)):
        pathLength  += matrix[randSolution[i]][randSolution[i - 1]]
    return pathLength 

#Este metodo genera los puntos vecinos de la solucion random intercambiando las coordenadas y regresa el mejor punto vecino
def generateNeighbors(matrix, randSolution):
    neighbors = []
    for i in range(len(randSolution)):
        for j in range(i + 1, len(randSolution)):
            neighbor = randSolution.copy()
            neighbor[i] = randSolution[j]
            neighbor[j] = randSolution[i]
            neighbors.append(neighbor)
            
    #Se asume que el primer punto vecino en la lista es el mejor     
    bestNeighbor = neighbors[0]
    bestPath = createPathlength(matrix, bestNeighbor)
    
    #Se verifica que el punto vecino si sea el mejor
    for neighbor in neighbors:
        currentPath = createPathlength(matrix, neighbor)
        if currentPath < bestPath:
            bestPath = currentPath
            bestNeighbor = neighbor
    return bestNeighbor, bestPath

#se ejecuta el algoritmo de Hill Climbing, tomando en cuenta las coordenadas.
def hill_climbing(coords):
    #se crea la matriz de adyacencia. 
    matrix = createAdyacencyMatrix(coords)
    
    #se crea una solucion aleatoria y una longitud de ruta basada en esta solucion.
    currSolution = randomSolution(matrix)
    currentPath = createPathlength(matrix, currSolution)

    #se generan los vecinos tomando como base la solucion y matriz generadas.
    neighbor = generateNeighbors(matrix,currSolution)[0]
    bestNeighbor, bestNeighborPath = generateNeighbors(matrix, neighbor)

    #se itera para determinar si la ruta obtenida es la más optima
    #si se obtiene una mejor ruta, las variables declaradas anteriormente se actualizan.
    while bestNeighborPath < currentPath:
        currentSolution = bestNeighbor
        currentPath = bestNeighborPath
        neighbor = generateNeighbors(matrix, currentSolution)[0]
        bestNeighbor, bestNeighborPath = generateNeighbors(matrix, neighbor)
    #se regresa la mejor ruta y la mejor solucion
    return currentPath, currentSolution

#se genera el grafo y se obtienen los resultados
def graph(coords, countryCords):
    #se ejecuta el algoritmo y se guarda en una variable: finalSolution
    finalSolution = hill_climbing(coords)
    
    countryResults=[]

    #se establecen las variables para la creacion del grafo
    G = nx.DiGraph()
    t = finalSolution[1]
    G.add_nodes_from(finalSolution[1])
    
    for i in range(0, len(finalSolution[1])):
        countryResults.append( countryCords[t[i]] )

    for i in range(1, len(finalSolution[1])):
        G.add_edge(t[i - 1], t[i])
    G.add_edge(t[len(t) - 1], t[0])
    
    #se crea el grafo, generando una imagen png. 
    colorMap = []
    for node in G:
        print("node: ",node)
        if node == finalSolution[1][0]:
            colorMap.append('lime')
        else: 
            colorMap.append('plum')
    nx.draw(G, with_labels = True, node_color = colorMap, node_size = 1000)
    print("G: ",G)
    #print(imageName)
    plt.savefig("static/imgs/img1.png")
    plt.close()
    print("The solution is \n", finalSolution[1], "\nThe path length is \n", finalSolution[0])
    return finalSolution[1], countryResults, finalSolution[0]
