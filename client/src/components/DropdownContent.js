import React, { Component } from "react";

export default class Dropdown extends Component {
  handleUserClicked = (id) => {
    localStorage.setItem("userId", id);
    window.location.reload();
  };

  render() {
    const users = [
      {
        text: "Clinton Yeboah",
        id: 1,
      },
      {
        text: "Hatem Hatem",
        id: 2,
      },
      {
        text: "Guethie Guethie",
        id: 2,
      },
    ];

    const items = [];

    for (const [index, user] of users.entries()) {
      items.push(
        <div key={index} onClick={() => this.handleUserClicked(user.id)}>
          <div className="dropdownContent--user"></div>
          <p className="dropdownContent--user-text" style={{ margin: 0 }}>
            {user.text}
          </p>
        </div>
      );
    }
    return (
      <div className="dropdownContainer">
        <div className="navigation__container--userLogo">
          <div className="dropdownContent">
            {items}
          </div>
          <div className="dropdownContent dropdownContent--2">
            <p className="dropdownContent-textOutside">Account</p>
            <p className="dropdownContent-textOutside">Help Center</p>
            <p className="dropdownContent-textOutside">Sign out of Netflix</p>
          </div>
        </div>
      </div>
    );
  }
}
