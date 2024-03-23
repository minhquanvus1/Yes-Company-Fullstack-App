import React from "react";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";

const UpdateProduct = () => {
  const token = localStorage.getItem("token");
  const { id } = useParams();
  const navigate = useNavigate();
  const [values, setValues] = useState({
    id: id,
    name: "",
    unit_price: 0,
    description: "",
  });

  useEffect(() => {
    axios
      .get(`http://localhost:8080/products/${id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response) => {
        console.log(response.data.product);
        setValues(response.data.product);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  const handleSubmit = (e) => {
    const { id, ...updatedValues } = values;
    e.preventDefault();
    axios
      .patch(`http://localhost:8080/products/${id}`, updatedValues, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((res) => {
        setValues(res.data.product);
        navigate("/landingPage");
      });
  };
  return (
    <>
      <div className="d-flex w-100 vh-100 justify-content-center align-items-center">
        <div className="w-50 border bg-secondary text-white p-5">
          <form onSubmit={handleSubmit}>
            <div>
              <label htmlFor="name">Name</label>
              <input
                type="text"
                className="form-control"
                id="name"
                placeholder="Enter Product Name"
                value={values.name}
                onChange={(e) => setValues({ ...values, name: e.target.value })}
              />
            </div>
            <div>
              <label htmlFor="unit_price">Unit Price</label>
              <input
                type="number"
                className="form-control"
                id="unit_price"
                placeholder="Enter Unit Price"
                value={values.unit_price}
                onChange={(e) =>
                  setValues({ ...values, unit_price: parseInt(e.target.value) })
                }
              />
            </div>
            <div>
              <label htmlFor="description">Description</label>
              <textarea
                type="text"
                className="form-control"
                id="description"
                placeholder="Enter Description"
                value={values.description}
                onChange={(e) =>
                  setValues({ ...values, description: e.target.value })
                }
              />
            </div>
            <button className="btn btn-info ">Update</button>
          </form>
        </div>
      </div>
    </>
  );
};

export default UpdateProduct;
