import React, { Component } from "react";
import { bindActionCreators } from "redux";
import { connect } from "react-redux";

import { fetchTopRated,fetchPopular } from "../store/actions/index";
import { getMovieRows } from "../getMovie";

class Popular extends Component {
  constructor(props) {
    super(props)
    props.fetchPopular();
  }

  render() {
    let movies;
    // Call getMoviesRows function only when we get the data back
    // from the API through redux
    if (this.props.popular.data) {
      const url = `/api/popular`;
      movies = getMovieRows(this.props.popular.data, url);
    }
    return (
      <>
        <h1 className="movieShowcase__heading">Popular</h1>
        <div className="movieShowcase__container">{movies}</div>
      </>
    );
  }
}

const mapStateToProps = (state) => {
  return { popular: state.popular };
};

const mapDispatchToProps = (dispatch) => {
  return bindActionCreators({ fetchPopular }, dispatch);
};

export default connect(mapStateToProps, mapDispatchToProps)(Popular);
