import axios from "axios";

/** base url to make requests to the the movie database */

const instance = axios.create({
  baseURL: process.env.REACT_APP_SERVER_URL,
});

export default instance;
