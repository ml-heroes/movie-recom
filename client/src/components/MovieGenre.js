import React, { Component } from 'react'
import axios from 'axios'
import Modal from '../components/UI/Modal';
import MovieDetails from '../components/Movie/MovieDetails';

export default class MovieGenre extends Component {
   state = {
      toggleModal: false,
      img:null
   }

   handleToggleModal = () => {
      this.setState({ toggleModal: true });
   }

   closeModal = () => {
      this.setState({ toggleModal: false })
   }


    getPoster = async () => {
        // const imgs=[]
        const dataM = await axios.get(`https://api.themoviedb.org/3/movie/${this.props.movie.id}?api_key=2085f970b90ca4a5b5047991206ede55`)
          const res = dataM.data.poster_path
          return res;
          // .then((data)=>{
          //   const theImgP = data.poster_path
          //   //this.setState({img:theImgP})
          //    imgs.push(data.poster_path)
          //    return theImgP
          // })
          // return dataM
      }

   componentDidMount = async ()=>{
    const img = await this.getPoster()
    this.setState({ img: 'https://image.tmdb.org/t/p/w500' + img })
   }



   render() {
      let netflixUrl = false;
      if (this.props.url === `/discover/tv?api_key=2085f970b90ca4a5b5047991206ede55&with_networks=213`) {
         netflixUrl = true;
      }

      return (
         <>
            <div onClick={() => this.handleToggleModal()}
               className={"movieShowcase__container--movie" + (netflixUrl ? "__netflix" : "")}>
               <img src={this.state.img} className="movieShowcase__container--movie-image" alt="movie showcase" />
            </div>
            <Modal show={this.state.toggleModal} movie={this.props.movie} modalClosed={this.closeModal}>
               <MovieDetails movie={this.props.movie} />
            </Modal>
         </>
      )
   }
}
