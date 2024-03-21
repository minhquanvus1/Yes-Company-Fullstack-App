import React from "react";
import { useState, useEffect } from "react";
import SpinnerLoading from "./utils/SpinnerLoading";
import SearchCustomer from "./SearchCustomer";
import { Link } from "react-router-dom";
const CustomerTable = () => {
  const [customers, setCustomers] = useState([]);
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const getCustomers = async () => {
      try {
        setIsLoading(true);
        const response = await fetch("http://localhost:8080/customers", {
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
    <div>
      {token && (
        <SearchCustomer
          token={token}
          setCustomers={setCustomers}
        ></SearchCustomer>
      )}
      <h1>Customer List</h1>
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
            {isLoading && <SpinnerLoading></SpinnerLoading>}
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
      <Link to="/landingPage">Landing Page</Link>
    </div>
  );
};

export default CustomerTable;
