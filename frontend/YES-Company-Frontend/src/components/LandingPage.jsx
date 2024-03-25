import { useAuth0 } from "@auth0/auth0-react";
import React, { useEffect, useState } from "react";
import CreateCustomerForm from "./CreateCustomerForm";
import ProductList from "./ProductList";
import CreateProductForm from "./CreateProductForm";
import { useNavigate } from "react-router-dom";
import { baseURL } from "../baseURL";

const LandingPage = () => {
  const { user, isAuthenticated, isLoading, getAccessTokenSilently } =
    useAuth0();
  const [token, setAccessToken] = useState("");
  const [isAlreadyCustomer, setIsAlreadyCustomer] = useState(false);
  const navigate = useNavigate;

  const getToken = async () => {
    try {
      const response = await getAccessTokenSilently();
      setAccessToken(response);
      localStorage.setItem("user", JSON.stringify(user));
      localStorage.setItem("isAuthenticated", isAuthenticated);
      localStorage.setItem("token", response);
      console.log(response);
    } catch {
      console.log("error");
      console.log(error.message);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      getToken();
    }
  }, [isAuthenticated]);

  const checkCustomer = async () => {
    try {
      const response = await fetch(`${baseURL}/check-customer`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      if (response.status === 200) {
        setIsAlreadyCustomer(true);
      } else {
        setIsAlreadyCustomer(false);
      }
      const responseData = await response.json();
      console.log(responseData);
    } catch (error) {
      console.log("error");
      console.log(error.error);
    }
  };

  const handleCustomerFormClick = () => {
    navigate;
  };

  return (
    <div>
      {isAuthenticated && (
        <>
          <h1>Welcome {user.name}</h1>
          <button onClick={getToken}>Get Access Token</button>
          <span>
            <p>Access Token is {token}</p>
          </span>
          <button onClick={handleCustomerFormClick}>
            Register to become our Customer
          </button>
          <button onClick={checkCustomer}>Are you already a Customer?</button>
          <CreateProductForm></CreateProductForm>
          {!isAlreadyCustomer && <ProductList></ProductList>}
          {isAlreadyCustomer && (
            <>
              <p>You are already a customer</p>
              <br />
              <p>Here are the products</p>
              <ProductList></ProductList>
            </>
          )}
          {/* {!isAlreadyCustomer && <CreateCustomerForm token={token}/>} */}
        </>
      )}
    </div>
  );
};

export default LandingPage;
