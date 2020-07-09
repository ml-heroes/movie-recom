import React, { Component } from "react";
import axios from "axios";
import Header from "../components/Header";
import Footer from "../components/Footer";

import TrendingMovies from "./TrendingMovies";
import Popular from "./Popular";
import Likeable from "./Likeable";
import Recommend from "./Recommend";
import ActionMovies from "./ActionMovies";
import ComedyMovies from "./ComedyMovies";
import Documentaries from "./Documentaries";

class MainContent extends Component {
  state = {
    /** Will hold our chosen movie to display on the header */
    selectedMovie: {},
  };

  componentDidMount = () => {
    this.getMovie();
  };

  getMovie = () => {
    /** Movie Id for the Narcos series  */
    const movieId = 63351;
    /** Make Api call to retrieve the details for a single movie  */
    const url = `https://api.themoviedb.org/3/tv/${movieId}?api_key=2085f970b90ca4a5b5047991206ede55`;
    axios
      .get(url)
      .then((res) => {
        const movieData = res.data;
        this.setState({ selectedMovie: movieData });
      })
      .catch((error) => {
        console.log(error);
      });
  };

  render() {
    return (
      <div className="container">
        <Header movie={this.state.selectedMovie} />
        <div className="movieShowcase">
          <TrendingMovies />
          <Recommend />
          <ActionMovies />
          <ComedyMovies />
          <Documentaries />
          <Popular />
          <Likeable />
        </div>
        <Footer />
      </div>
    );
  }
}

export default MainContent;
