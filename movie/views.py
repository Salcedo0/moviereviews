import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
from django.shortcuts import render
from django.http import HttpResponse
from openai import OpenAI
import numpy as np
import os
from dotenv import load_dotenv

from .models import Movie

# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name':'Matias Monsalve'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies': movies})

def about(request):
    #return HttpResponse('<h1>Welcome to About Page</h1>')
    return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

def statistics_view(request):
    matplotlib.use('Agg')
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')  # Obtener todos los años de las películas
    movie_counts_by_year = {}  # Crear un diccionario para almacenar la cantidad de películas por año 
    for year in years: # Contar la cantidad de películas por año
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    bar_width = 0.5 # Ancho de las barras
    bar_spacing = 0.5 # Separación entre las barras 
    bar_positions = range(len(movie_counts_by_year)) # Posiciones de las barras
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    movies = Movie.objects.values_list('genre', flat=True)
    genre_counts = {}
    for g in movies:
        if g:  
            first_genre = g.split(",")[0].strip()  # tomar solo el primer género
            genre_counts[first_genre] = genre_counts.get(first_genre, 0) + 1

    plt.bar(range(len(genre_counts)), genre_counts.values(), width=0.5, align='center', color='green')
    plt.title('Movies per genre (first only)')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(range(len(genre_counts)), genre_counts.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic1 = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'statistics.html', {
        'graphic': graphic,
        'graphic1': graphic1
    })

