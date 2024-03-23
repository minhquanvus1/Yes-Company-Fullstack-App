import React from "react";
import { useParams, useLocation, Link } from "react-router-dom";
import CardOrderDetail from "../CardOrderDetail";
const OrderDetailsPage = () => {
  const { orderIid } = useParams();
  const location = useLocation();
  const { order } = location.state;
  const orderItems = order.order_items;
  console.log("orderItems in orderdetailspage: ", orderItems);
  return (
    <>
      <div style={{ marginTop: "1vh" }}>
        <Link to="/orders" className="btn btn-info">
          Go to All Orders Page
        </Link>
        &nbsp;
        <Link to="/landingPage" className="btn btn-success">
          Go to Landing Page
        </Link>
      </div>
      <div className="row" style={{ marginTop: "2%" }}>
        {orderItems.length > 0 &&
          orderItems.map((item) => (
            <div key={item.name} className="col-sm-6 mb-3 mb-sm-0">
              <CardOrderDetail
                // key={item.name}
                productName={item.name}
                unitPrice={item.unit_price}
                quantity={item.quantity}
              />
            </div>
          ))}
        {/* {orderItems.map((item) => (
          <CardOrderDetail
            key={item.name}
            productName={item.name}
            unitPrice={item.unit_price}
            quantity={item.quantity}
          />
        ))} */}
      </div>
    </>
  );
};

export default OrderDetailsPage;
