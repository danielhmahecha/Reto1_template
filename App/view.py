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
import sys
import controller 
import csv
from ADT import list as lt
from DataStructures import listiterator as it

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones  y  por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def printMenu():
    print("Bienvenido al Reto 1")
    print("1- Cargar información del reto")
    print("2- Peliculas con mejores votaciones")
    print("3- Peliculas por Director")
    print("4- Requerimiento 1: Buenas películas por director")
    print("5- Requerimiento 2: Filtrar películas por votos")
    print("6- Requerimiento 3: Peliculas por Director con promedio de votos")
    print("7- Requerimiento 4: Películas por actores")
    print("8- Requerimiento 5: Peliculas por género")
    print("0- Salir")


def initCatalog ():
    """
    Inicializa el catalogo de peliculas
    """
    return controller.initCatalog()


def loadData (catalog):
    """
    Carga las peliculas en la estructura de datos
    """
    controller.loadData(catalog)



def printBestMovies (movies, number, criteria):
    size = lt.size(movies)
    if size:
        print ('\nEstas son las '+str(number)+' películas con '+criteria+": ")
        iterator = it.newIterator(movies)
        while  it.hasNext(iterator):
            movie = it.next(iterator)
            print ('Titulo: ' + movie['original_title'] + '  Fecha: ' + movie['release_date'] + ' Rating: ' + movie['vote_average'] + ' (' + movie['vote_count'] + ' votos)')
    else:
        print ('No se encontraron peliculas')

def printByDirector (movies):
    size = lt.size(movies)
    if size:
        iterator = it.newIterator(movies)
        while  it.hasNext(iterator):
            movie = it.next(iterator)
            print ('Titulo: ' + movie['original_title'] + '  Fecha: ' + movie['release_date'] + ' Rating: ' + movie['vote_average'])
    else:
        print ('No se encontraron peliculas')


"""
Menu principal
"""
while True:
    printMenu()
    inputs =input('Seleccione una opción para continuar\n')
    if int(inputs[0])==1:
        print("Cargando información de los archivos ....")
        catalog = initCatalog ()
        loadData (catalog)
        print ('Peliculas cargadas: ' + str(lt.size(catalog['movies'])))
        print ('Directores cargados: ' + str(lt.size(catalog['directors'])))


    elif int(inputs[0])==2:
        number = input ("Buscando las TOP ?: ")
        movies = controller.getBestMovies (catalog, int(number))
        printBestMovies (movies, number, 'mejor promedio de votos')
        print ("\n")

    elif int(inputs[0])==3:
        dir_name = input("Nombre del director a buscar: ")
        movies = controller.getMoviesByDirector (catalog, dir_name, 0)
        print('Director buscado: '+dir_name)
        printByDirector (movies)
        print ("\n")

    elif int(inputs[0])==4:
        dir_name = input("Nombre del director a buscar: ")
        movies = controller.getMoviesByDirector (catalog, dir_name, 6)
        print("El director "+dir_name+" tiene las siguientes películas con puntaje igual o mayor a 6:\n")
        printByDirector (movies)
        print ("\n")

    elif int(inputs[0])==5:
        print("1- Mostrar las 10 películas con mayor cantidad de votos")
        print("2- Mostrar las películas con menor cantidad de votos")
        print("3- Mostrar las 10 películas con el mayor voto promedio")
        print("4- Mostrar las películas con el menor voto promedio")
        inputs=input('Seleccione una opción para continuar\n')
        if int(inputs[0])==1:
            movies = controller.getMostVoted(catalog, 10)
            printBestMovies(movies, 10, 'mayor cantidad de votos')
            print ("\n")
        elif int(inputs[0])==2:
            number = input("Buscando las TOP?: ")
            movies = controller.getLessVoted(catalog, number)
            printBestMovies(movies,number, 'menor cantidad de votos')
            print('\n')
        elif int(inputs[0])==3:
            movies = controller.getBestMovies(catalog,10)
            printBestMovies(movies, 10, 'mejor voto promedio')
            print('\n')
        elif int(inputs[0])==4:
            number = input("Buscando las TOP?: ")
            movies = controller.getWorstMovies(catalog, number)
            printBestMovies(movies, number, 'peor voto promedio')
            print('\n')

    elif int(inputs[0])==6:
        dir_name = input("Nombre del director a buscar: ")
        print("El director "+dir_name+" tiene las siguientes películas: ")
        movies = controller.getMoviesByDirector (catalog, dir_name, 0)
        printByDirector (movies)
        data = controller.countMoviesDirector (catalog, dir_name, 0)
        print('\nEl total de peliculas es '+str(data[1])+' y el voto promedio es '+str(data[0]))
        print ("\n")


    elif int(inputs[0])==7:
        act_name = input("Nombre del actor a buscar: ")
        print("El actor "+act_name+" ha participado en las siguientes películas: ")
        movies = controller.getMoviesByActor(catalog, act_name, 0)
        printByDirector (movies)
        data = controller.countMoviesActor(catalog, act_name, 0)
        director = controller.getDirector_mas_comun(catalog,act_name,0)
        print('\nEl total de peliculas es: '+str(data[1])+' y el voto promedio es: '+str(data[0]))
<<<<<<< HEAD
        print("\n El director que más ha dirigido a este actor es: " + director)
=======
        print("\n El director que mas veces lo ha dirigido es  " + director)
>>>>>>> 4effad2efb213679d4a779e9859d998c26e37459
        print ("\n")

    elif int(inputs[0])==8:
        genre = input ("Nombre del género a buscar: ")
        #print(catalog['directors'])
        data = controller.getMoviesByGenre(catalog,genre)
        print('\nEl total de películas del género '+genre+' es: '+str(data[0])+' y tienen un promedio de votos de: '+str(data[1])+'\n')

        pass
    else:
        sys.exit(0)
sys.exit(0)
