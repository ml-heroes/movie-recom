import { FETCH_NETFLIX_ORIGINALS } from '../actions/index';

export default function (state = {}, action) {
  switch (action.type) {
    case "FETCH_CONTENT":
      const data = action.payload;
      return { ...state, data };
    default:
      return state;
  }
}
