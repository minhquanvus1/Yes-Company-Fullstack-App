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
import { Link } from "react-router-dom";
const LandingPage = () => {
  const { user, isAuthenticated, getAccessTokenSilently } = useAuth0();
  const [token, setAccessToken] = useState("");
  const [role, setRole] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [products, setProducts] = useState([]);
  const [isAlreadyCustomer, setIsAlreadyCustomer] = useState(false);
  const [items, setItems] = useState([]);
  //   const [isAuthenticatedFromLocalStorage, setIsAuthenticatedFromLocalStorage] =
  //     useState("");
  //   const [quantity, setQuantity] = useState(0);
  const [isCheckedOut, setIsCheckedOut] = useState(false);
  const [customer, setCustomer] = useState({});
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
    // const tokenFromLocalStorage = localStorage.getItem("token");
    // if (
    //   tokenFromLocalStorage !== "" &&
    //   isAuthenticatedFromLocalStorage !== ""
    // ) {
    //   setAccessToken(tokenFromLocalStorage);
    //   setIsAuthenticatedFromLocalStorage(isAuthenticatedFromLocalStorage);
    // } else {
    //   getToken();
    // }
    getToken();
    // setAccessToken(localStorage.getItem("token"));
    // setIsAuthenticatedFromLocalStorage(localStorage.getItem("isAuthenticated"));
  }, [isAuthenticated]);

  useEffect(() => {
    if (token) {
      setRole(findRole(token));
      localStorage.setItem("role", findRole(token));
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
    const fetchCustomerData = async () => {
      if (role === "customer") {
        try {
          const customer = await checkCustomer(
            token,
            setIsAlreadyCustomer,
            setIsLoading
          );
          setCustomer(customer);
          localStorage.setItem("customer", JSON.stringify(customer));
          console.log("isAlreadyCustomer: ", isAlreadyCustomer);
        } catch (error) {
          console.log("error");
          console.log(error.message);
          if (error.message === "This Customer not found in backend database") {
            setIsAlreadyCustomer(false);
            setIsLoading(false);
          }
        }
      }
    };
    fetchCustomerData();
  }, [isAuthenticated, token, role]);
  console.log("items: ", items);
  return (
    <div style={{ alignItems: "center", marginLeft: "10%" }}>
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
      {isAuthenticated && token && role === "customer" && customer && (
        <CustomerView
          token={token}
          isAlreadyCustomer={isAlreadyCustomer}
          isLoading={isLoading}
          items={items}
          setItems={setItems}
          customer={customer}
          setIsCheckedOut={setIsCheckedOut}
        ></CustomerView>
      )}
      {isAuthenticated &&
        token &&
        (role === "manager" || (role === "customer" && isAlreadyCustomer)) && (
          <Link
            to="/orders"
            state={{ role: role }}
            className="btn btn-success"
            style={{ marginTop: "0.5%" }}
          >
            {role === "manager" ? "All Orders" : "My Orders"}
          </Link>
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
            items={items}
            setItems={setItems}
            // quantity={quantity}
            // setQuantity={setQuantity}
            setIsCheckedOut={setIsCheckedOut}
            isCheckedOut={isCheckedOut}
          ></ProductList>
        )}
      <div style={{ marginTop: "1%" }}>
        <LogoutButton></LogoutButton>&nbsp;&nbsp;
        {role === "customer" && isAlreadyCustomer && (
          <button
            className="btn btn-warning btn-sm"
            style={{ marginLeft: "2%" }}
            onClick={() => {
              setItems([]);
            }}
          >
            Reset Order
          </button>
        )}
      </div>
    </div>
  );
};

export default LandingPage;
