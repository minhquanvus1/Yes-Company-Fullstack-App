import React from "react";
import axios from "axios";
import { useState, useEffect } from "react";
import CardOrder from "../CardOrder";
import SpinnerLoading from "../utils/SpinnerLoading";
import { useLocation, Link } from "react-router-dom";
const AllOrdersPage = () => {
  const [orders, setOrders] = useState([]);
  const token = localStorage.getItem("token");
  const [isLoading, setIsLoading] = useState(true);
  const location = useLocation();
  const { role } = location.state;
  //   const propsData = location.state;
  //   console.log("role in allorders: ", propsData);
  //   console.log("customer in allorder: ", customer);
  //   console.log("role in allorders: ", role);
  const customer = JSON.parse(localStorage.getItem("customer"));
  console.log("customer in allorder: ", customer);

  const getAllOrders = async () => {
    try {
      let response;
      setIsLoading(true);
      if (role === "manager") {
        response = await axios.get("http://localhost:8080/orders", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
      } else {
        response = await axios.get(
          `http://localhost:8080/customers/${customer["id"]}/orders`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
      }

      const ordersResponse = response.data;
      const allOrders = ordersResponse.orders;
      console.log("orders: ", allOrders);
      setOrders(allOrders);
      setIsLoading(false);
    } catch (error) {
      console.log(error);
    }
  };
  useEffect(() => {
    getAllOrders();
  }, []);
  return (
    <>
      {!isLoading && (
        <Link to="/landingPage" className="btn btn-info">
          Go to Landing Page
        </Link>
      )}
      {!isLoading &&
        orders.length > 0 &&
        orders.map((order) => {
          return (
            // <CardOrder
            //   key={order.id}
            //   orderId={order.id}
            //   deliverDate={order.deliver_date}
            //   comment={order.comment}
            //   totalPrice={order.total_price}
            //   role={role}
            //   customerId={order.customer_id}
            // />
            <div
              key={order.id}
              style={{
                display: "flex",
                // marginLeft: "40%",
                marginTop: "10px",
                justifyContent: "center", // Horizontally center the CardOrder
                alignItems: "center", // Vertically center the CardOrder
                // minHeight: "60vh",
                overflowY: "auto",
              }}
            >
              <CardOrder
                // key={order.id}
                orderId={order.id}
                deliverDate={order.deliver_date}
                comment={order.comment}
                totalPrice={order.total_price}
                role={role}
                customerId={order.customer_id}
                orders={orders}
                setOrders={setOrders}
              />
              {/* {!isLoading && orders.length <= 0 && <p>No orders</p>}
              {isLoading && <SpinnerLoading />} */}
            </div>
          );
        })}
      {!isLoading && orders.length <= 0 && (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            minHeight: "100vh",
          }}
        >
          <p>No orders</p>
        </div>
      )}
      {isLoading && (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            minHeight: "100vh",
          }}
        >
          <SpinnerLoading />
        </div>
      )}
    </>
  );
};

export default AllOrdersPage;
