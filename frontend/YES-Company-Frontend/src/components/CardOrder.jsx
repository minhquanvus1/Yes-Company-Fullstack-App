import React from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { getCustomerById } from "./functions/getCustomerById";
import { useState, useEffect } from "react";

const CardOrder = ({
  orderId,
  deliverDate,
  comment,
  totalPrice,
  role,
  customerId,
  orders,
  setOrders,
}) => {
  const [customer, setCustomer] = useState({});
  const token = localStorage.getItem("token");
  useEffect(() => {
    if (role === "manager") {
      getCustomerById(token, customerId)
        .then((response) => {
          setCustomer(response);
        })
        .catch((error) => {
          console.log(error);
        });
    }
  }, []);

  const deleteOrder = async () => {
    try {
      const response = await axios.delete(
        `http://localhost:8080/orders/${orderId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      const deletedOrderId = response.data.deleted;
      const newOrders = orders.filter((order) => order.id !== deletedOrderId);
      setOrders(newOrders);
      console.log("deleted orderId: ", deletedOrderId);
    } catch (error) {
      console.log(error);
    }
  };
  return (
    <>
      <div
        className="card text-center mb-4"
        style={{
          maxWidth: "540px",
          display: "flex",
        }}
      >
        <div className="card-header">
          {role === "manager" && Object.keys(customer).length > 0
            ? `Order ID: ${orderId} - Customer Name: ${customer.first_name} ${customer.last_name} - Customer Address: ${customer.address}`
            : `Order ID: ${orderId}`}
        </div>
        <div className="card-body">
          <h5 className="card-title">{`Deliver Date: ${deliverDate}`}</h5>
          <p className="card-text">{`Comment: ${comment}`}</p>
          <Link to={`/orders/${orderId}`} className="btn btn-primary">
            View Order
          </Link>{" "}
          &nbsp;
          <button className="btn btn-danger" onClick={deleteOrder}>
            Delete Order
          </button>
        </div>
        <div className="card-footer text-body-secondary">{`Total Price: ${totalPrice}K (VND)`}</div>
      </div>
    </>
  );
};

export default CardOrder;
