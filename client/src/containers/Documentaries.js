import React, { Component } from "react";
import { bindActionCreators } from "redux";
import { connect } from "react-redux";

import { getMovieRows } from "../getMovie";
import { fetchDocumentaries } from "../store/actions/index";

class Documentaries extends Component {
  constructor(props) {
    super(props);
    props.fetchDocumentaries();
  }

  render() {
    let movies;
    // Call getMoviesRows function only when we get the data back
    // from the API through redux
    if (this.props.doc.data) {
      console.log("Docmmmmt ",this.props.doc.data)
      const url = `/api/genres/Documentary`;
      movies = getMovieRows(this.props.doc.data, url);
    }
    return (
      <>
        <h1 className="movieShowcase__heading">Documentaries</h1>
        <div className="movieShowcase__container">{movies}</div>
      </>
    );
  }
}

const mapStateToProps = (state) => {
  return { doc: state.documentary };
};

const mapDispatchToProps = (dispatch) => {
  return bindActionCreators({ fetchDocumentaries }, dispatch);
};

export default connect(mapStateToProps, mapDispatchToProps)(Documentaries);
