import React, { Component } from "react";
import axios from "axios";
import Header from "../components/Header";
import Footer from "../components/Footer";

import { bindActionCreators } from "redux";
import { connect } from "react-redux";

import { getMovieRows } from "../getMovie";
import { fetchTopRated } from "../store/actions/index";

import TrendingMovies from "./TrendingMovies";
import Popular from "./Popular";
import Likeable from "./Likeable";
import Recommend from "./Recommend";
import ActionMovies from "./ActionMovies";
import ComedyMovies from "./ComedyMovies";
import Documentaries from "./Documentaries";
import HorrorMovies from "./HorrorMovies";
import RomanceMovies from "./RomanceMovies"

class MainContent extends Component {


  state = {
    /** Will hold our chosen movie to display on the header */
    selectedMovie: {},
  };

  componentDidMount = async () => {
    await this.getMovie();
    //this.props.fetchTopRated();
  };

componentDidUpdate = () => {

}


  getMovie = async () => {
    // Make Api call to retrieve the details for a single movie
    const userId = localStorage.getItem('userId') || 1;
    const res = await axios.get(`http://localhost/api/collabs/${userId}`)
    console.log("pros mainContyen",res.data[0].id)
    const postPath = await axios.get(`https://api.themoviedb.org/3/movie/${res.data[0].id}?api_key=2085f970b90ca4a5b5047991206ede55`)

this.setState({selectedMovie: postPath.data})

  };

  render() {

    return (
      <div className="container">
        <Header movie={this.state.selectedMovie} />
        <div className="movieShowcase">
          <Recommend />
          <TrendingMovies />
          <Popular />
          <Likeable />
          <ActionMovies />
          <ComedyMovies />
          <HorrorMovies />
          <RomanceMovies />
          <Documentaries />
        </div>
        <Footer />
      </div>
    );
  }


}


export default MainContent;
