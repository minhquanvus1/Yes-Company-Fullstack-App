import React from "react";
import axios from "axios";
import { useAuth0 } from "@auth0/auth0-react";
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import SpinnerLoading from "../../utils/SpinnerLoading";
import { formatDeliverDate } from "../../functions/formatDeliverDate";

const CustomerView = ({
  token,
  isAlreadyCustomer,
  isLoading,
  items,
  setItems,
  customer,
  setIsCheckedOut,
}) => {
  const { user, isAuthenticated } = useAuth0();
  const [deliverDate, setDeliverDate] = useState("");
  const [comment, setComment] = useState("");

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
  const handleDeliverDate = (e) => {
    const formattedDeliverDate = formatDeliverDate(e.target.value);
    setDeliverDate(formattedDeliverDate);
    console.log("non formatted deliver date: ", e.target.value);
    console.log("formatted deliver date: ", formattedDeliverDate);
  };
  const handleComment = (e) => {
    setComment(e.target.value);
    console.log("comment: ", e.target.value);
  };
  const handleCheckOut = async () => {
    setIsCheckedOut(false);
    const headers = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    };
    console.log("customer inside customerview:", customer);
    const checkOutObject = {
      customer_id: customer.id,
      order_items: items,
      deliver_date: deliverDate,
      comment: comment,
    };
    console.log("checkoutobject: ", checkOutObject);
    try {
      const response = await axios.post(
        "http://localhost:8080/orders",
        checkOutObject,
        { headers: headers }
      );
      console.log(response);
      console.log("Order created successfully!: ", response.data.order);
      setItems([]);
      setComment("");
      setDeliverDate("");
      //   setQuantity(0);
      setIsCheckedOut(true);
      return response.data.order;
    } catch (error) {
      console.log(error);
      setIsCheckedOut(false);
    }
  };
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
      {items.length > 0 && (
        <div>
          <label htmlFor="datetime">Delivery Date and Time:</label>
          <input
            type="datetime-local"
            id="datetime"
            name="datetime"
            value={deliverDate}
            onChange={handleDeliverDate}
          />
        </div>
      )}
      {items.length > 0 && (
        <div>
          <label htmlFor="comment">Comments:</label>
          <textarea
            id="comment"
            name="comment"
            placeholder="Enter your comments..."
            value={comment}
            onChange={handleComment}
          ></textarea>
        </div>
      )}
      {items.length > 0 && (
        <button
          className="btn btn-primary"
          disabled={deliverDate === ""}
          onClick={handleCheckOut}
        >
          Checkout
        </button>
      )}
    </div>
  );
};

export default CustomerView;
