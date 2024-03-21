import { useAuth0 } from "@auth0/auth0-react";

import React from "react";

const LogoutButton = () => {
  const { logout, isAuthenticated } = useAuth0();
  const handleLogOut = () => {
    logout({ returnTo: window.location.origin });
    localStorage.clear();
  };
  return isAuthenticated && <button onClick={handleLogOut}>Log Out</button>;
};

export default LogoutButton;
