import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { useState, useEffect } from "react";

const CustomerView = ({ token }) => {
  const { user, isAuthenticated } = useAuth0();
  return (
    <div>
      <div>
        <h1>Welcome to YES-Company</h1>
        <p>
          {isAuthenticated ? `Welcome ${user.name}!` : "You are not logged in!"}
        </p>
      </div>
    </div>
  );
};

export default CustomerView;
