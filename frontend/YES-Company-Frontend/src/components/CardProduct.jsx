import React from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { addToCart } from "./functions/addToCart";
import { useState, useEffect } from "react";
const CardProduct = ({
  id,
  name,
  unit_price,
  description,
  role,
  setProducts,
  items,
  setItems,
  //   quantity,
  //   setQuantity,
  setIsCheckedOut,
  isCheckedOut,
}) => {
  const token = localStorage.getItem("token");
  const [quantity, setQuantity] = useState(0);
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
  //   useEffect(() => {
  //     if (quantity === 0) {
  //       document.getElementById(`quantity-${id}`).value = 0;
  //     }
  //   }, [quantity]);
  const resetQuantityFields = () => {
    const quantityInputs = document.getElementsByClassName("quantity-input");
    for (let input of quantityInputs) {
      input.value = "";
    }
    setIsCheckedOut(false);
  };
  useEffect(() => {
    if (isCheckedOut) {
      resetQuantityFields();
    }
  }, [isCheckedOut]);

  //   useEffect(() => {
  //     setItems([]);
  //   }, []);
  return (
    <>
      <div className="card" style={{ width: "18rem", height: "100%" }}>
        {/* <img src="..." className="card-img-top" alt="..."/> */}
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
          &nbsp;
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
          {/* {role === "customer" && (
            
            <input
              min="0"
              //   max="20"
              type="number"
              id="typeNumber"
              className="form-control"
              onChange={(e) => {
                setQuantity(e.target.value);
              }}
            />
          )} */}
          {role === "customer" && (
            <div
              className="d-flex align-items-center"
              style={{ marginTop: "5px" }}
            >
              <label htmlFor="typeNumber" className="me-2">
                Quantity:
              </label>
              <input
                min="0"
                type="number"
                id={`quantity-${id}`}
                className="form-control quantity-input"
                onChange={(e) => {
                  setQuantity(e.target.value);
                }}
                style={{
                  width: "10rem",
                }}
              />
            </div>
          )}
          {role === "customer" && (
            <button
              className="text-decoration-none btn btn-sm btn-primary"
              onClick={() => {
                console.log("quantity: ", quantity);
                console.log("typeof quantity", typeof quantity);
                console.log(quantity === "");
                console.log("parseInt quantity:", parseInt(quantity));
                if (quantity === "" || parseInt(quantity) === 0) {
                  alert("Please input quantity");
                  return;
                }
                addToCart(id, parseInt(quantity), items, setItems);
                // setQuantity(0);
                // document.getElementById(`quantity-${id}`).value = 0;
              }}
              style={{ marginTop: "5%" }}
            >
              Add to Cart
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
