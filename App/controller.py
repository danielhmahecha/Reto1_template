"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model 
import csv
from ADT import list as lt
from DataStructures import listiterator as it
from Sorting import mergesort as sort
from time import process_time 


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


# Funcionaes utilitarias

def printList (lst):
    iterator = it.newIterator(lst)
    while  it.hasNext(iterator):
        element = it.next(iterator)
        result = "".join(str(key) + ": " + str(value) + ",  " for key, value in element.items())
        print (result)



def compareratings (movie1, movie2):
    return ( float(movie1['vote_average']) > float(movie2['vote_average']))

def compareVoteCount  (movie1, movie2):
    return ( float(movie1['vote_count']) > float(movie2['vote_count']))

# Funciones para la carga de datos 

def loadMovies (catalog):
    """
    Carga las peliculas del archivo.  Por cada libro se cargan sus directores
    
    """
    t1_start = process_time() #tiempo inicial
    moviesfile = cf.data_dir + 'themoviesdb/SmallMoviesDetailsCleaned.csv'
    
    dialect = csv.excel()
    dialect.delimiter=";"
    with open(moviesfile, encoding="utf-8") as csvfile:
        spamreader = csv.DictReader(csvfile, dialect=dialect)
        for row in spamreader: 
            lt.addLast (catalog['movies'], row)
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución carga peliculas",t1_stop-t1_start," segundos")



def loadDirectors(catalog):
    """
    Carga todos los directores
    """
    t1_start = process_time() #tiempo inicial
    castingfile = cf.data_dir + 'themoviesdb/MoviesCastingRaw-small.csv'
    
    dialect = csv.excel()
    dialect.delimiter=";"
    with open(castingfile, encoding="utf-8") as csvfile:
        spamreader = csv.DictReader(csvfile, dialect=dialect)
        for row in spamreader: 
            model.addDirector (catalog, row)
    t1_stop = process_time() #tiempo inicial
    print("Tiempo de ejecución carga directores",t1_stop-t1_start," segundos")


def loadActors(catalog):
    """
    Carga todos los actores
    """
    t1_start = process_time() #tiempo inicial
    castingfile = cf.data_dir + 'themoviesdb/MoviesCastingRaw-small.csv'
    
    dialect = csv.excel()
    dialect.delimiter=";"
    with open(castingfile, encoding="utf-8") as csvfile:
        spamreader = csv.DictReader(csvfile, dialect=dialect)
        for row in spamreader: 
            model.addActors (catalog, row)
    t1_stop = process_time() #tiempo inicial
    print("Tiempo de ejecución carga actores",t1_stop-t1_start," segundos")



def initCatalog ():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = None
    catalog = model.newCatalog()
    return catalog



def loadData (catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    loadMovies(catalog)
    sort.sort(catalog['movies'],compareratings)
    loadDirectors(catalog)
    loadActors(catalog)
    

# Funciones llamadas desde la vista y enviadas al modelo

def getMoviesByDirector (catalog, dir_name, min_avg):
    return model.getMoviesByDirector(catalog, dir_name, min_avg)

def countMoviesDirector (catalog, dir_name, min_avg):
    movies = getMoviesByDirector (catalog, dir_name, min_avg)
    size = lt.size(movies)
    count = 0
    sum = 0
    if size:
        iterator = it.newIterator(movies)
        while  it.hasNext(iterator):
            movie = it.next(iterator)
            count+=1
            sum += float(movie['vote_average'])
        
        avg = round(( sum / count ),2 )
            
    else:
        avg=0
    
    data = (avg,count)

    return data

def getDirector_mas_comun (catalog,dir_name,min_avg):

    movies = getMoviesByActor (catalog, dir_name,min_avg)
    directors = catalog['directors']
    size = lt.size(movies)
    listDirectors = lt.newList()
    dicc = {}
    if size:
        iterator = it.newIterator(movies)
        while  it.hasNext(iterator):
            movie = it.next(iterator)
            ID = int(movie['id'])
            size1 = lt.size(directors)
            if size1:
                iterator_1 = it.newIterator(directors)
                while  it.hasNext(iterator_1):
                    peli = it.next(iterator_1)
                    i = int(peli['movie_id'])
                    if ID == i :
                        if peli['name'] in dicc:
                            nVeces = dicc[peli['name']]
                            dicc[peli['name']] = nVeces +1
                        else :
                            dicc[peli['name']] = 1
                        lt.addLast(listDirectors, peli['name'])

    maximo = 0
    nombre_maximo = " "

    for director in dicc :
        veces = dicc[director]
        if veces > maximo :
            maximo = veces
            nombre_maximo = director

    return nombre_maximo

def getMoviesByActor (catalog, act_name, min_avg):
    return model.getMoviesByActor(catalog, act_name,min_avg)

def countMoviesActor (catalog, act_name, min_avg):
    movies = getMoviesByActor (catalog, act_name, min_avg)
    size = lt.size(movies)
    count = 0
    sum = 0
    if size:
        iterator = it.newIterator(movies)
        while  it.hasNext(iterator):
            movie = it.next(iterator)
            count+=1
            sum += float(movie['vote_average'])
        
        avg = round(( sum / count ),2 )
            
    else:
        avg=0

    data = [avg,count]
    return data

def getBestMovies (catalog, number):
    sort.sort(catalog['movies'],compareratings)
    movies = catalog['movies']
    bestmovies = lt.newList()
    for cont in range (1, int(number)+1):
        movie = lt.getElement (movies, cont)
        lt.addLast (bestmovies, movie)
    return bestmovies

def getWorstMovies (catalog, number):

    sort.sort(catalog['movies'],compareratings)
    movies = catalog['movies']
    worstmovies = lt.newList()
    size = lt.size(movies)
    for cont in range (size-int(number), size+1):
        movie = lt.getElement (movies, cont)
        lt.addFirst (worstmovies, movie)
    return worstmovies

def getMostVoted (catalog, number):
    
    sort.sort(catalog['movies'],compareVoteCount)
    movies=catalog['movies']
    mostvoted = lt.newList()
    
    for cont in range (1, int(number)+1):
        movie = lt.getElement (movies, cont)
        lt.addLast (mostvoted, movie)
    return mostvoted
    
def getLessVoted (catalog, number):
    
    sort.sort(catalog['movies'],compareVoteCount)
    movies=catalog['movies']

    size=lt.size(movies)
    lessvoted = lt.newList()

    print(size)

    for cont in range (1+size-int(number), size+1):
        movie = lt.getElement (movies, cont)
        lt.addFirst (lessvoted, movie)
    return lessvoted

def getMoviesByGenre (catalog, genre):
    movies = catalog['movies']
    count=0
    sumvote=0
    avg=0
    data=[]

    iterator = it.newIterator(movies)
    while  it.hasNext(iterator):
        movie = it.next(iterator)
        if genre.lower() in movie['genres'].lower():
            count+=1
            sumvote+=float(movie['vote_average'])
            avg=sumvote/count
    
    data = (count,round(avg,2) )
    return data


