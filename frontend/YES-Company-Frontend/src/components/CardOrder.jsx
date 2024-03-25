import React from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { getCustomerById } from "./functions/getCustomerById";
import { useState, useEffect } from "react";
import { baseURL } from "../baseURL";

const CardOrder = ({
  //   orderId,
  //   deliverDate,
  //   comment,
  //   totalPrice,
  order,
  role,
  //   customerId,
  orders,
  setOrders,
}) => {
  const [customer, setCustomer] = useState({});
  const token = localStorage.getItem("token");
  console.log("order haha:", order);
  console.log("role ahah:", role);
  useEffect(() => {
    if (role === "manager") {
      getCustomerById(token, order.customer_id)
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
      const response = await axios.delete(`${baseURL}/orders/${order.id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
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
          width: "50%",
          display: "flex",
        }}
      >
        <div className="card-header">
          {role === "manager" && Object.keys(customer).length > 0
            ? `Order ID: ${order.id} - Customer Name: ${customer.first_name} ${customer.last_name} - Customer Address: ${customer.address}`
            : `Order ID: ${order.id}`}
        </div>
        <div className="card-body">
          <h5 className="card-title">{`Deliver Date: ${order.deliver_date}`}</h5>
          <p className="card-text">{`Comment: ${order.comment}`}</p>
          <Link
            to={`/orders/${order.id}`}
            state={{ order: order }}
            className="btn btn-primary"
          >
            View Order
          </Link>
          &nbsp;
          <button className="btn btn-danger" onClick={deleteOrder}>
            Delete Order
          </button>
        </div>
        <div className="card-footer text-body-secondary">{`Total Price: ${order.total_price}K (VND)`}</div>
      </div>
    </>
  );
};

export default CardOrder;
