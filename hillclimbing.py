import random
from typing import final
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

countries = ['mx','ar','bo','br','cl','co','cr','cu','do','ec','gt','hn','ht','pr','sv','tt','ur','ni','pa','pe','py']
#Lee archivo txt con las coordenadas de los paises
def getInputs(inp):
    data = []
    newdata = []
    with open('paises2.txt') as my_file:      
        for line in my_file:  
            data.append([list(map(float ,x.split(','))) for x in line.split(' ')])
    
        for i in range(len(inp)):
            newdata.append(data[int(inp[i])])
    coords = np.array(newdata)
    return coords

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


def hill_climbing(coords):
    matrix = createAdyacencyMatrix(coords)
    
    currSolution = randomSolution(matrix)
    currentPath = createPathlength(matrix, currSolution)
    neighbor = generateNeighbors(matrix,currSolution)[0]
    bestNeighbor, bestNeighborPath = generateNeighbors(matrix, neighbor)

    while bestNeighborPath < currentPath:
        currentSolution = bestNeighbor
        currentPath = bestNeighborPath
        neighbor = generateNeighbors(matrix, currentSolution)[0]
        bestNeighbor, bestNeighborPath = generateNeighbors(matrix, neighbor)

    return currentPath, currentSolution


def graph(coords, countryCords):
    finalSolution = hill_climbing(coords)
    countryResults=[]
    

    G = nx.DiGraph()
    t = finalSolution[1]
    G.add_nodes_from(finalSolution[1])
    

    for i in range(0, len(finalSolution[1])):
        countryResults.append( countryCords[t[i]] )
        #print("fs",finalSolution[1][i])
    print("Countries: ",countryResults)

    for i in range(1, len(finalSolution[1])):
        G.add_edge(t[i - 1], t[i])
        print("t: ",t[i])
    G.add_edge(t[len(t) - 1], t[0])
    colorMap = []
    for node in G:
        if node == finalSolution[1][0]:
            colorMap.append('lime')
        else: 
            colorMap.append('plum')
    nx.draw(G, with_labels = True, node_color = colorMap, node_size = 1000)
    plt.savefig("path.png")
    print("The solution is \n", finalSolution[1], "\nThe path length is \n", finalSolution[0])
    return finalSolution[1], countryResults
