import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import CustomerView from "./views/CustomerView";
import { useState, useEffect } from "react";
import { findRole } from "../functions/findRole";
import ManagerView from "./views/ManagerView";
import LogoutButton from "../LogoutButton";
import ProductList from "../ProductList";
import SpinnerLoading from "../utils/SpinnerLoading";
import SearchProduct from "../SearchProduct";

const LandingPage = () => {
  const { user, isAuthenticated, getAccessTokenSilently } = useAuth0();
  const [token, setAccessToken] = useState("");
  const [role, setRole] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  const getToken = async () => {
    try {
      setIsLoading(true);
      const response = await getAccessTokenSilently();
      setIsLoading(false);
      setAccessToken(response);
      localStorage.setItem("user", JSON.stringify(user));
      localStorage.setItem("isAuthenticated", isAuthenticated);
      localStorage.setItem("token", response);
      console.log(response);
    } catch (error) {
      console.log("error");
      console.log(error.message);
      setIsLoading(false);
    }
  };
  useEffect(() => {
    if (isAuthenticated) {
      getToken();
    }
  }, [isAuthenticated]);

  useEffect(() => {
    if (token) {
      setRole(findRole(token));
    }
  }, [token]);
  return (
    <div>
      <SearchProduct></SearchProduct>
      {isAuthenticated && (!token || !role) && (
        <SpinnerLoading></SpinnerLoading>
      )}
      {isAuthenticated && token && role === "manager" && (
        <ManagerView token={token}></ManagerView>
      )}
      {isAuthenticated && token && role === "customer" && (
        <CustomerView token={token}></CustomerView>
      )}
      {/* <CustomerView></CustomerView> */}
      {isAuthenticated && token && role && <ProductList></ProductList>}
      <LogoutButton></LogoutButton>
    </div>
  );
};

export default LandingPage;
