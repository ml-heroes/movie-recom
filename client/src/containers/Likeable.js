import React, { Component } from "react";
import { bindActionCreators } from "redux";
import { connect } from "react-redux";

import { getMovieRows } from "../getMovie";
import { fetchLikeable, fetchContentBased } from "../store/actions/index";

class NetflixOriginals extends Component {
  constructor(props) {
    super(props);
    props.fetchLikeable();
  }

  render() {
    let movies;
    // Call getMoviesRows function only when we get the data back
    // from the API through redux
    if (this.props.movies.data) {
      const url = `/likeable`;
      movies = getMovieRows(this.props.movies.data, url);
    }
    return (
      <>
        <h1 className="movieShowcase__heading">CONTENT BASED RECOMMENDATION</h1>
        <div className="movieShowcase__container">{movies}</div>
      </>
    );
  }
}

const mapStateToProps = (state) => {
  return { movies: state.netflixOriginals };
};

const mapDispatchToProps = (dispatch) => {
  return bindActionCreators({ fetchLikeable }, dispatch);
};

export default connect(mapStateToProps, mapDispatchToProps)(NetflixOriginals);
