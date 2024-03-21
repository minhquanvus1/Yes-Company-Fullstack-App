import React from "react";
import { useState } from "react";

const CreateCustomerForm = ({ token }) => {
  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");
  const [address, setAddress] = useState("");
  const [customer, setCustomer] = useState({});

  const createCustomer = async () => {
    try {
      const response = await fetch("http://localhost:8080/customers", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          first_name: first_name,
          last_name: last_name,
          address: address,
        }),
      });
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const responseData = await response.json();
      if (response.status === 201) {
        setCustomer(responseData);
      }
      console.log(responseData);
      setFirstName("");
      setLastName("");
      setAddress("");
    } catch {
      console.log("error");
      console.log(error.message);
    }
  };
  return (
    <>
      <form onSubmit={createCustomer}>
        <div className="mb-3">
          <label htmlFor="first_name" className="form-label">
            First Name
          </label>
          <input
            type="text"
            className="form-control"
            id="first_name"
            aria-describedby="emailHelp"
            value={first_name}
            onChange={(e) => {
              setFirstName(e.target.value);
            }}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="last_name" className="form-label">
            Last Name
          </label>
          <input
            type="text"
            className="form-control"
            id="last_name"
            value={last_name}
            onChange={(e) => {
              setLastName(e.target.value);
            }}
          />
        </div>
        <div className="mb-3 form-check">
          <label className="form-label" htmlFor="address">
            Address
          </label>
          <input
            type="text"
            className="form-control"
            id="address"
            value={address}
            onChange={(e) => {
              setAddress(e.target.value);
            }}
          />
        </div>
        <button type="submit" className="btn btn-primary">
          Submit
        </button>
      </form>
    </>
  );
};

export default CreateCustomerForm;
