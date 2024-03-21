import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { useState, useEffect } from "react";
import CardProduct from "./CardProduct";

const ProductList = () => {
  const [products, setProducts] = useState([]);
  const { isAuthenticated } = useAuth0();
  const [token, setToken] = useState(localStorage.getItem("token"));

  useEffect(() => {
    if (isAuthenticated && token) {
      getProducts();
    }
  }, [isAuthenticated, token]);
  console.log("outside return: ", products);
  console.log("outside return: ", products.length);
  const getProducts = async () => {
    try {
      const response = await fetch("http://localhost:8080/products", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const responseData = await response.json();
      setProducts(responseData.products);
      console.log(responseData);
      console.log(responseData.products);
      console.log("inside getProduct: ", products.length);
    } catch (error) {
      console.log("error");
      console.log(error.error);
    }
  };

  return (
    <div>
      <h1>Product List</h1>
      {console.log(products)}
      {console.log(products.length)}
      {products.length > 0 ? (
        <ul>
          {products.map((product) => {
            return (
              <CardProduct
                key={product.id}
                name={product.name}
                unit_price={product.unit_price}
                description={product.description}
              />
            );
            // return <React.Fragment key={product.id}>
            // <li>{product.name}</li>
            // <li>{product.unit_price}</li>
            // <li>{product.description}</li>
            // </React.Fragment>
          })}
        </ul>
      ) : (
        <p>No products available</p>
      )}
    </div>
  );
};

export default ProductList;