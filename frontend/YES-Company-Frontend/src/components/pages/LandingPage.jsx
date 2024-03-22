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
import { checkCustomer } from "../functions/checkCustomer";
const LandingPage = () => {
  const { user, isAuthenticated, getAccessTokenSilently } = useAuth0();
  const [token, setAccessToken] = useState("");
  const [role, setRole] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [products, setProducts] = useState([]);
  const [isAlreadyCustomer, setIsAlreadyCustomer] = useState(false);
  //   useEffect(() => {
  //     // setAccessToken(localStorage.getItem("token"));
  //     console.log("haha inside");
  //     console.log(localStorage.getItem("isAuthenticated"));
  //   }, []);

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

  console.log("outside return: ", products);
  console.log("outside return: ", products.length);
  const getProducts = async () => {
    try {
      setIsLoading(true);
      const response = await fetch("http://localhost:8080/products", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const responseData = await response.json();
      setIsLoading(false);
      setProducts(responseData.products);
      console.log(responseData);
      console.log(responseData.products);
      console.log("inside getProduct: ", products.length);
    } catch (error) {
      console.log("error");
      console.log(error.error);
      setIsLoading(false);
    }
  };
  useEffect(() => {
    if (isAuthenticated && token) {
      getProducts();
    }
  }, [isAuthenticated, token]);

  useEffect(() => {
    role === "customer" &&
      checkCustomer(token, setIsAlreadyCustomer, setIsLoading);
    console.log("isAlreadyCustomer: ", isAlreadyCustomer);
  }, [isAuthenticated, token, role]);

  return (
    <div>
      {/* <p>hello world</p>
      <CustomerView token={token}></CustomerView>
      <ProductList products={products}></ProductList>
      <LogoutButton></LogoutButton> */}
      {/* {isLoading && <SpinnerLoading></SpinnerLoading>} */}

      {isAuthenticated &&
        token &&
        (role === "manager" || (role === "customer" && isAlreadyCustomer)) && (
          <SearchProduct
            token={token}
            setProducts={setProducts}
          ></SearchProduct>
        )}

      {isAuthenticated && (!token || !role) && (
        <SpinnerLoading></SpinnerLoading>
      )}
      {isAuthenticated && token && role === "manager" && (
        <ManagerView token={token}></ManagerView>
      )}
      {isAuthenticated && token && role === "customer" && (
        <CustomerView
          token={token}
          isAlreadyCustomer={isAlreadyCustomer}
          isLoading={isLoading}
        ></CustomerView>
      )}
      {/* <CustomerView></CustomerView> */}
      {isAuthenticated &&
        token &&
        (role === "manager" || (role === "customer" && isAlreadyCustomer)) && (
          <ProductList
            products={products}
            isLoading={isLoading}
            role={role}
            setProducts={setProducts}
          ></ProductList>
        )}
      <LogoutButton></LogoutButton>
    </div>
  );
};

export default LandingPage;
