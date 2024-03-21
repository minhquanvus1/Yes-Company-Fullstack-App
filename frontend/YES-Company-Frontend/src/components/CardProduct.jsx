import React from "react";
import { Link } from "react-router-dom";
import OrderItemQuantity from "./utils/OrderItemQuantity";
const CardProduct = ({ id, name, unit_price, description }) => {
  return (
    <>
      <div className="card" style={{ width: "18rem" }}>
        {/* <img src="..." class="card-img-top" alt="..."/> */}
        <div className="card-body">
          <h5 className="card-title">{name}</h5>
          <p className="card-text">{unit_price}k (VND)</p>
          <p className="card-text">{description}</p>
          {/* <a href="#" className="btn btn-primary">
            Go somewhere
          </a> */}
          <Link
            to={`/products/${id}`}
            className="text-decoration-none btn btn-sm btn-success"
          >
            Update
          </Link>
          {/* <div className="flex justify-content-between align-items-center">
            <button className="btn btn-primary" style={{ marginTop: "7px" }}>
              Quantity
            </button>
            <OrderItemQuantity />
          </div> */}
          {/* <div className="row">
          <button className="btn btn-primary ">Quantity</button>
          <OrderItemQuantity></OrderItemQuantity>
          </div> */}
        </div>
      </div>
    </>
  );
};

export default CardProduct;
