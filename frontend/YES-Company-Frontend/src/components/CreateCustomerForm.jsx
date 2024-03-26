import React from "react";
import { useState, useEffect } from "react";
import { useNavigate, Link, useLocation } from "react-router-dom";
import { baseURL } from "../baseURL";

const CreateCustomerForm = () => {
  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");
  const [address, setAddress] = useState("");
  const [customer, setCustomer] = useState({});
  const navigate = useNavigate();
  // const location = useLocation();
  // const stateData = location.state;
  // console.log("location data", location.state);

  const token = localStorage.getItem("token");

  const createCustomer = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${baseURL}/customers`, {
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
      navigate("/landingPage");
      console.log("navigate", navigate("/landingPage"));
    } catch (error) {
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
        <button
          type="submit"
          className="btn btn-primary"
          disabled={first_name === "" || last_name === "" || address === ""}
        >
          Submit
        </button>
        <Link to="/landingPage">Go to LandingPage</Link>
      </form>
    </>
  );
};

export default CreateCustomerForm;
