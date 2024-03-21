import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { useState, useEffect } from "react";

const ManagerView = ({ token }) => {
  const { user, isAuthenticated, isLoading, getAccessTokenSilently } =
    useAuth0();
  return (
    <div>
      <div>
        <h1>Welcome to YES-Company, Manager</h1>
        <p>
          {isAuthenticated ? `Welcome ${user.name}!` : "You are not logged in!"}
        </p>
      </div>
    </div>
  );
};

export default ManagerView;
