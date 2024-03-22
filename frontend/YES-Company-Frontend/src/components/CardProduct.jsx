import React from "react";
import axios from "axios";
import { Link } from "react-router-dom";

const CardProduct = ({
  id,
  name,
  unit_price,
  description,
  role,
  setProducts,
}) => {
  const token = localStorage.getItem("token");
  const deleteProduct = async (e) => {
    e.preventDefault();
    axios
      .delete(`http://localhost:8080/products/${id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((res) => {
        console.log("deleted product id: ", res.data.deleted);
        setProducts((prevProducts) =>
          prevProducts.filter((product) => product.id !== id)
        );
      })
      .catch((error) => {
        console.log(error);
      });
  };
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
          {role === "manager" && (
            <Link
              to={`/products/${id}`}
              className="text-decoration-none btn btn-sm btn-success"
            >
              Update
            </Link>
          )}
          {/* <Link
            to={`/products/${id}`}
            className="text-decoration-none btn btn-sm btn-success"
          >
            Update
          </Link> */}
          {role === "manager" && (
            <button
              className="text-decoration-none btn btn-sm btn-primary"
              onClick={deleteProduct}
            >
              Delete
            </button>
          )}
          {/* <button
            className="text-decoration-none btn btn-sm btn-primary"
            onClick={deleteProduct}
          >
            Delete
          </button> */}

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
