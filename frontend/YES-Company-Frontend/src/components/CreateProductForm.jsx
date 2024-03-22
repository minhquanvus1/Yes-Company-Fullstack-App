import React from "react";
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

const CreateProductForm = () => {
  const [name, setName] = useState("");
  const [unit_price, setUnitPrice] = useState("");
  const [description, setDescription] = useState("");
  const navigate = useNavigate();

  const token = localStorage.getItem("token");
  const createProduct = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:8080/products", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          name: name,
          unit_price: unit_price,
          description: description,
        }),
      });
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const responseData = await response.json();
      console.log(responseData);
      setName("");
      setUnitPrice("");
      setDescription("");
      navigate("/landingPage");
    } catch (error) {
      console.log("error");
      console.log(error.error);
    }
  };
  return (
    <>
      <form onSubmit={createProduct}>
        <div className="mb-3">
          <label for="name" className="form-label">
            Product Name
          </label>
          <input
            type="text"
            className="form-control"
            id="name"
            value={name}
            onChange={(e) => {
              setName(e.target.value);
            }}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="unit_price" className="form-label">
            Unit Price
          </label>
          <input
            type="text"
            className="form-control"
            id="unit_price"
            value={unit_price}
            onChange={(e) => {
              setUnitPrice(e.target.value);
            }}
          />
        </div>
        <div className="mb-3 form-check">
          <label className="form-label" htmlFor="description">
            Description
          </label>
          <input
            type="text"
            className="form-control"
            id="description"
            value={description}
            onChange={(e) => {
              setDescription(e.target.value);
            }}
          />
        </div>
        <button type="submit" className="btn btn-primary">
          Submit
        </button>
      </form>
      <Link to="/landingPage">Go to LandingPage</Link>
    </>
  );
};

export default CreateProductForm;
