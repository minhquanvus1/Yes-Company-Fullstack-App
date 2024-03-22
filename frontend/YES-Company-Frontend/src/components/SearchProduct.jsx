import React from "react";
import { useState, useEffect } from "react";

const SearchProduct = ({ token, setProducts }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const handleChange = (e) => {
    setSearchTerm(e.target.value);
    console.log(searchTerm);
  };

  const searchForProduct = async () => {
    try {
      const response = await fetch(`http://localhost:8080/search-products`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          name: searchTerm,
        }),
      });
      if (response.status === 404) {
        console.log("Product not found");
        setProducts([]);
      } else if (response.status === 200) {
        const responseData = await response.json();
        console.log(responseData);
        const productList = responseData.products;
        setProducts(productList);
        console.log(productList);
      } else {
        throw new Error("Network response was not ok");
      }
    } catch (error) {
      console.log("error");
      console.log(error.message);
    }
  };

  useEffect(() => {
    searchForProduct();
  }, [searchTerm]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    searchForProduct();
  };
  return (
    <>
      <form className="d-flex" onSubmit={handleSubmit}>
        <input
          className="form-control me-2"
          type="search"
          placeholder="Search Product"
          aria-label="Search"
          value={searchTerm}
          onChange={handleChange}
        />
        <button className="btn btn-outline-success" type="submit">
          Search
        </button>
      </form>
    </>
  );
};

export default SearchProduct;
