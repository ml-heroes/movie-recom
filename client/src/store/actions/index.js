import axios from '../../axios-movies';

export const FETCH_TRENDING = 'FETCH_TRENDING';
export const FETCH_NETFLIX_ORIGINALS = 'FETCH_NETFLIX_ORIGINALS';
export const FETCH_TOP_RATED = 'FETCH_TOP_RATED';
export const FETCH_ACTION_MOVIES = 'FETCH_ACTION_MOVIES';
export const FETCH_COMEDY_MOVIES = 'FETCH_COMEDY_MOVIES';
export const FETCH_HORROR_MOVIES = 'FETCH_HORROR_MOVIES';
export const FETCH_ROMANCE_MOVIES = 'FETCH_ROMANCE_MOVIES';
export const FETCH_DOCUMENTARIES = 'FETCH_DOCUMENTARIES';
export const FETCH_LIKEABLE = "FETCH_LIKEABLE";

export function fetchTrending() {
  const request = axios.get(
    `/api/trending`
  );

  return {
    type: FETCH_TRENDING,
    payload: request,
  };
}

export function fetchPopular() {
  const request = axios.get(`/api/popular`);

  return {
    type: "FETCH_POPULAR",
    payload: request,
  };
}

export function fetchLikeable() {
  const request = axios.get(`/api/likeable`);

  return {
    type: FETCH_LIKEABLE,
    payload: request,
  };
}

export async function fetchContentBased(title) {
  const request = await axios.get(`/api/content/${title}`)


  return {
    type: "FETCH_CONTENT",
    payload: request,
  };
}



export function fetchTopRated() {
  const userId = localStorage.getItem('userId') || 1;
  const request = axios.get(`/api/collabs/${userId}`);

  return {
    type: FETCH_TOP_RATED,
    payload: request,
  };
}

export function fetchActionMovies() {
  const request = axios.get(`/api/genres/Action`);

  return {
    type: FETCH_ACTION_MOVIES,
    payload: request,
  };
}

export function fetchComedyMovies() {
  const request = axios.get(`/api/genres/Comedy`);

  return {
    type: FETCH_COMEDY_MOVIES,
    payload: request,
  };
}

export function fetchHorrorMovies() {
  const request = axios.get(`/api/genres/Horror`);

  return {
    type: FETCH_HORROR_MOVIES,
    payload: request,
  };
}

export function fetchRomanceMovies() {
  const request = axios.get(`/api/genres/Romance`);

  return {
    type: FETCH_ROMANCE_MOVIES,
    payload: request,
  };
}

export function fetchDocumentaries() {
  const request = axios.get(`/api/genres/Documentary`);

  return {
    type: FETCH_DOCUMENTARIES,
    payload: request,
  };
}
