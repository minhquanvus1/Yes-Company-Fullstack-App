import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { useState } from "react";
import { Link } from "react-router-dom";

const ManagerView = ({ token }) => {
  const { user, isAuthenticated } = useAuth0();
  //   const isAuthenticated = localStorage.getItem("isAuthenticated");
  return (
    <div>
      <div>
        <h1>Welcome to YES-Company, Manager</h1>
        <p>
          {isAuthenticated ? `Welcome ${user.name}!` : "You are not logged in!"}
        </p>
        <Link to="/customers">
          <button className="btn btn-success">View Customers</button>
        </Link>
        &nbsp;&nbsp;
        <Link to="/products/create">
          <button className="btn btn-success">Create Product</button>
        </Link>
      </div>
    </div>
  );
};

export default ManagerView;
