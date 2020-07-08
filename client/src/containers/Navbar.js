import React, { useState } from "react";
import axios from 'axios';
import NavigationItem from "../components/NavigationItem";
import { ReactComponent as SearchLogo } from "../static/images/search-icon.svg";
import NetflixLogo from "../static/images/Netflix_Logo_RGB.png";
import { ReactComponent as BellLogo } from "../static/images/bell-logo.svg";
import { ReactComponent as DropdownArrow } from "../static/images/drop-down-arrow.svg";
import DropdownContent from "../components/DropdownContent";

function Navigation(props){
  const [scrolling, setScrolling] = useState(false);

  const handleScroll = (event) => {
    if (window.scrollY === 0) {
      setScrolling(false);
    } else if (window.scrollY > 50) {
      setScrolling(true);
    }
  }

return(
      <nav className={"navigation " + (scrolling ? "black" : "")}>
        <ul className="navigation__container">
          <NavigationItem link="/" exact>
            <img
              className="navigation__container--logo"
              src={NetflixLogo}
              alt=""
            />
          </NavigationItem>
          <DropdownArrow className="navigation__container--downArrow-2"></DropdownArrow>
          <div className="navigation__container-link pseudo-link">Home</div>
          <div className="navigation__container-link pseudo-link">TV Shows</div>
          <div className="navigation__container-link pseudo-link">Movies</div>
          <div className="navigation__container-link pseudo-link">
            Recently Added
          </div>
          <div className="navigation__container-link pseudo-link">My List</div>

          <div className="navigation__container--left">

            <input
              onChange={props.inputChange}
              className="navigation__container--left__input"
              type="text"
              placeholder="Title" />

              <button>
                <SearchLogo onClick={props.showMovies} className="logo" />
              </button>

          </div>

          <div className="navigation__container-link pseudo-link">KIDS</div>
          <div className="navigation__container-link pseudo-link">DVD</div>
          <BellLogo className="navigation__container--bellLogo" />

          <DropdownContent />
          <DropdownArrow className="navigation__container--downArrow" />
        </ul>
      </nav>
)}






/*class navigation extends Component {

  state = {
    scrolling: false,
    title:""
  };

  componentDidMount() {
    window.addEventListener("scroll", this.handleScroll);
  }

  componentWillUnmount() {
    window.removeEventListener("scroll", this.handleScroll);
  }

  /** changes the scrolling state depending on the Y-position */
  /*handleScroll = (event) => {
    if (window.scrollY === 0) {
      this.setState({ scrolling: false });
    } else if (window.scrollY > 50) {
      this.setState({ scrolling: true });
    }
  };



  onTitleChange = (e) => {
    const titleV = e.target.value
    this.setState({title : titleV});
  };

  contentBased = (e)=>{
      console.log("searched clicked")
  };


  render() {
    const { scrolling } = this.state;
    const { showMovies } = this.props;

    return (

    );
  }
}*/

export default Navigation;
