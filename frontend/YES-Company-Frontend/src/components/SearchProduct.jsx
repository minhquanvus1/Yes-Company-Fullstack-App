import React from "react";
import { useState } from "react";

const SearchProduct = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const handleChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const searchForProduct = async () => {
    try {
      const response = await fetch(
        `http://localhost:8080/products?search=${searchTerm}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            name: searchTerm,
          }),
        }
      );
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const responseData = await response.json();
      console.log(responseData);
      const productList = responseData.products;
      console.log(productList);
    } catch (error) {
      console.log("error");
      console.log(error.message);
    }
  };

  return (
    <>
      <form className="d-flex">
        <input
          className="form-control me-2"
          type="search"
          placeholder="Search"
          aria-label="Search"
          value={searchTerm}
          onChange={handleChange}
        />
        <button
          className="btn btn-outline-success"
          type="submit"
          onClick={searchForProduct}
        >
          Search
        </button>
      </form>
    </>
  );
};

export default SearchProduct;
