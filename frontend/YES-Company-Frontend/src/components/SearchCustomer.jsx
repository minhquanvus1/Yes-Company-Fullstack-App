import React from "react";
import { useState } from "react";

const SearchCustomer = ({ token, setCustomers }) => {
  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");

  const handleFirstNameChange = (e) => {
    setFirstName(e.target.value);
  };
  const handleLastNameChange = (e) => {
    setLastName(e.target.value);
  };

  const searchForCustomer = async () => {
    try {
      const response = await fetch(`http://localhost:8080/search-customers`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          first_name: first_name,
          last_name: last_name,
        }),
      });
      if (response.status === 200 || response.status === 404) {
        const responseData = await response.json();
        console.log(responseData);
        const customerList = responseData.customers;
        setCustomers(customerList);
        console.log(customerList);
      } else {
        throw new Error("Network response was not ok");
        console.log(response.status);
      }
    } catch (error) {
      console.log("error");
      console.log(error.message);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    searchForCustomer();
    console.log("first name: ", first_name);
    console.log("last name: ", last_name);
  };
  return (
    <>
      <form
        className="d-flex"
        style={{ width: "100%" }}
        onSubmit={handleSubmit}
      >
        <div style={{ width: "50%" }}>
          <input
            className="form-control me-2"
            type="search"
            placeholder="First Name"
            aria-label="Search"
            value={first_name}
            onChange={handleFirstNameChange}
          />
        </div>
        <div style={{ width: "50%" }}>
          <input
            className="form-control me-2"
            type="search"
            placeholder="Last Name"
            aria-label="Search"
            value={last_name}
            onChange={handleLastNameChange}
          />
        </div>
        <button className="btn btn-outline-success" type="submit">
          Search Customer
        </button>
      </form>
    </>
  );
};

export default SearchCustomer;
