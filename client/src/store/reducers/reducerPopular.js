import { FETCH_LIKEABLE } from '../actions/index';

export default function (state = {}, action) {
  switch (action.type) {
    case "FETCH_POPULAR":
      const data = action.payload.data;
      return { ...state, data };
    default:
      return state;
  }
}
