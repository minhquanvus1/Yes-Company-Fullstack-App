import React from "react";
import { useState, useEffect } from "react";
import SpinnerLoading from "./utils/SpinnerLoading";
import SearchCustomer from "./SearchCustomer";
import { Link } from "react-router-dom";
import { baseURL } from "../baseURL";

const CustomerTable = () => {
  const [customers, setCustomers] = useState([]);
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const getCustomers = async () => {
      try {
        setIsLoading(true);
        const response = await fetch(`${baseURL}/customers`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const customersResponse = await response.json();
        setIsLoading(false);
        const customers = customersResponse.customers;
        setCustomers(customers);
        console.log("customers list: ", customers);
      } catch (error) {
        console.log("error");
        console.log(error.error);
        setIsLoading(false);
      }
    };
    if (token) {
      getCustomers();
    }
  }, [token]);
  return (
    <div style={{ width: "80%", marginLeft: "10%", marginTop: "2%" }}>
      {token && (
        <SearchCustomer
          token={token}
          setCustomers={setCustomers}
        ></SearchCustomer>
      )}
      <h1>Customer List</h1>
      {!isLoading && (
        <>
          {token && customers.length > 0 ? (
            <table className="table table-hover">
              <thead>
                <tr>
                  <th scope="col">First Name</th>
                  <th scope="col">Last Name</th>
                  <th scope="col">Address</th>
                </tr>
              </thead>
              <tbody>
                {customers.map((customer) => {
                  return (
                    <tr scope="row" key={customer.id}>
                      <td>{customer.first_name}</td>
                      <td>{customer.last_name}</td>
                      <td>{customer.address}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          ) : (
            <p>No customers found</p>
          )}
        </>
      )}
      {isLoading && <SpinnerLoading></SpinnerLoading>}
      <Link to="/landingPage" className="btn btn-success">
        Landing Page
      </Link>
    </div>
  );
};

export default CustomerTable;
