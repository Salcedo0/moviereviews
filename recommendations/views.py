import os
from pathlib import Path

import numpy as np
from django.shortcuts import render
from dotenv import load_dotenv
from openai import OpenAI

from movie.models import Movie


def recommendations(request):
    """Recommend the most similar movie to a free-text prompt using embeddings."""
    best_movie = None
    similarity = None
    prompt = None
    error_message = None

    if request.method == "POST":
        prompt = request.POST.get("prompt", "").strip()
        if prompt:
            env_path = Path(__file__).resolve().parent.parent / "openAI.env"
            if env_path.exists():
                load_dotenv(env_path)

            api_key = os.environ.get("openai_apikey")
            if not api_key:
                error_message = "OpenAI API key is not configured."
            else:
                try:
                    client = OpenAI(api_key=api_key)
                    response = client.embeddings.create(
                        input=[prompt],
                        model="text-embedding-3-small",
                    )
                    prompt_emb = np.array(response.data[0].embedding, dtype=np.float32)
                    max_similarity = -1.0

                    for movie in Movie.objects.all():
                        if not movie.emb:
                            continue

                        movie_emb = np.frombuffer(movie.emb, dtype=np.float32)
                        denom = np.linalg.norm(prompt_emb) * np.linalg.norm(movie_emb)
                        if denom == 0:
                            continue

                        sim = float(np.dot(prompt_emb, movie_emb) / denom)
                        if sim > max_similarity:
                            max_similarity = sim
                            best_movie = movie
                            similarity = sim
                except Exception as exc:
                    error_message = str(exc)
        else:
            error_message = "Please enter a short description so we can recommend a movie."

    return render(
        request,
        "recommendations.html",
        {
            "best_movie": best_movie,
            "similarity": similarity,
            "prompt": prompt,
            "error_message": error_message,
        },
    )
