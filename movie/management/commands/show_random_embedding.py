import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie
import random

class Command(BaseCommand):
    help = "Show the embedding of a random movie from the database."

    def handle(self, *args, **kwargs):
        movies = Movie.objects.all()
        if not movies.exists():
            self.stdout.write(self.style.ERROR("No movies found in the database."))
            return
        movie = random.choice(list(movies))
        self.stdout.write(self.style.WARNING(f"Random movie selected: {movie.title}"))
        if movie.emb:
            emb = np.frombuffer(movie.emb, dtype=np.float32)
            self.stdout.write(f"Embedding: {emb}")
        else:
            self.stdout.write(self.style.ERROR("No embedding found for this movie. Run the embedding generation command first."))
