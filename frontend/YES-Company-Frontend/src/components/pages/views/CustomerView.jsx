import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import SpinnerLoading from "../../utils/SpinnerLoading";

const CustomerView = ({ token, isAlreadyCustomer, isLoading }) => {
  const { user, isAuthenticated } = useAuth0();
  //   const [isAlreadyCustomer, setIsAlreadyCustomer] = useState(false);
  //   const checkCustomer = async () => {
  //     try {
  //       const response = await fetch("http://localhost:8080/check-customer", {
  //         headers: {
  //           Authorization: `Bearer ${token}`,
  //         },
  //       });
  //       if (!response.ok) {
  //         throw new Error("Network response was not ok");
  //       }
  //       if (response.status === 200) {
  //         setIsAlreadyCustomer(true);
  //       } else {
  //         setIsAlreadyCustomer(false);
  //       }
  //       const responseData = await response.json();
  //       console.log(responseData);
  //     } catch (error) {
  //       console.log("error");
  //       console.log(error.error);
  //     }
  //   };
  //   useEffect(() => {
  //     checkCustomer();
  //   }, []);
  return (
    <div>
      <div>
        <h1>Welcome to YES-Company</h1>
        <p>
          {isAuthenticated ? `Welcome ${user.name}!` : "You are not logged in!"}
        </p>
      </div>
      {!isLoading && isAuthenticated && !isAlreadyCustomer && (
        <Link to="/customers/create">Register to be our Customer</Link>
      )}
      {isLoading && <SpinnerLoading />}
    </div>
  );
};

export default CustomerView;
