import React, { useState } from "react";
import "./Navbar.css";
import { MenuList } from "./MenuList";
import { NavLink } from "react-router-dom";

const Navbar = () => {
    const [clicked, setClicked] = useState(false);

    const menulist = MenuList.map(({ title, url }, index) => {

        return (
            <li key={index}>
                {/* <a href={url}>{title}</a> */}
                <NavLink to={url} activeClassName="active">{title}</NavLink>
            </li>
        )
    })

    return (
        <nav>
            <div className="logo">
                VPN<font>Lab</font>
            </div>
            <div className="menu-icon" onClick={() => setClicked(!clicked)}>
                <i className={clicked ? "fa fa-times" : "fa fa-bars"} />
            </div>
            <ul className={clicked ? "menu-list" : "menu-list close"}>
                {menulist}
            </ul>
        </nav>
    )
}

export default Navbar;