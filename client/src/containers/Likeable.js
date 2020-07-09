import React, { Component } from "react";
import { bindActionCreators } from "redux";
import { connect } from "react-redux";

import { getMovieRows } from "../getMovie";
import { fetchLikeable, fetchContentBased } from "../store/actions/index";

class Likeable extends Component {
  constructor(props) {
    super(props);
    props.fetchLikeable();
  }

  render() {
    let movies;
    // Call getMoviesRows function only when we get the data back
    // from the API through redux
    if (this.props.likeable.data) {
      const url = `/api/likeable`;
      movies = getMovieRows(this.props.likeable.data, url);
    }
    return (
      <>
        <h1 className="movieShowcase__heading">Movies you May Like</h1>
        <div className="movieShowcase__container">{movies}</div>
      </>
    );
  }
}

const mapStateToProps = (state) => {
  return { likeable: state.likeable };
};

const mapDispatchToProps = (dispatch) => {
  return bindActionCreators({ fetchLikeable }, dispatch);
};

export default connect(mapStateToProps, mapDispatchToProps)(Likeable);
