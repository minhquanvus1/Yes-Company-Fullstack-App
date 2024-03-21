import React from "react";
import { useState, useEffect } from "react";
import SpinnerLoading from "./utils/SpinnerLoading";

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
      {isLoading && <SpinnerLoading></SpinnerLoading>}
      <h1>Customer List</h1>
      <table>
        <thead>
          <tr>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Address</th>
          </tr>
        </thead>
        <tbody>
          {customers.map((customer) => {
            return (
              <tr key={customer.id}>
                <td>{customer.first_name}</td>
                <td>{customer.last_name}</td>
                <td>{customer.address}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default CustomerTable;
