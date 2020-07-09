import React from "react";
import ReactDOM from "react-dom";
import "./static/sass/style.scss";
import App from "./App";
import { createStore, applyMiddleware } from "redux";
import { Provider } from "react-redux";
import * as serviceWorker from "./serviceWorker";
import reducers from "./store/reducers";
import promise from "redux-promise";
import { BrowserRouter } from "react-router-dom";
import env from "dotenv";
env.config();

const createStoreWithMiddleware = applyMiddleware(promise)(createStore);

const app = (
  // <React.StrictMode>
  <Provider store={createStoreWithMiddleware(reducers)}>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </Provider>
  // </React.StrictMode>
);

ReactDOM.render(app, document.getElementById("root"));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
