import MovieGenre from './components/MovieGenre';
import React from 'react';
import axios from "axios";

export function getMovieRows(movies, url) {
  console.log(movies)
  const movieRow = movies.map((movie) => {
    const url = `https://api.themoviedb.org/3/movie/${movie.id}?api_key=2085f970b90ca4a5b5047991206ede55`
    //const movieD = await axios.get(url)
    //console.log(movieD.data)

    //const postPath = await axios.get(`https://api.themoviedb.org/3/movie/${movie.id}?api_key=2085f970b90ca4a5b5047991206ede55`)


    let movieImageUrl ='https://image.tmdb.org/t/p/w500' + movie.poster_path;

      const movieComponent =
      (<MovieGenre
          key={movie.id}
          url={url}
          posterUrl={movieImageUrl}
          movie={movie}
        />)

    return  movieComponent;
  });

  return movieRow;
}
