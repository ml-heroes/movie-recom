import { combineReducers } from 'redux';
import TrendingReducer from './reducerTrending';
import LikeableReducer from './reducerLikeable';
import TopRatedReducer from './reducerTopRated';
import ActionMoviesReducer from './reducerActionMovies';
import ComedyMoviesReducer from './reducerComedyMovies';
import HorrorMoviesReducer from './reducerHorrorMovies';
import RomanceMoviesReducer from './reducerRomanceMovies';
import DocumentaryReducer from './reducerDocumentary';
import PopularReducer from './reducerPopular';

const rootReducer = combineReducers({
  trending: TrendingReducer,
  likeable: LikeableReducer,
  topRated: TopRatedReducer,
  action: ActionMoviesReducer,
  comedy: ComedyMoviesReducer,
  horror: HorrorMoviesReducer,
  romance: RomanceMoviesReducer,
  documentary: DocumentaryReducer,
  popular: PopularReducer
});

export default rootReducer;
