import React from "react";

const CardProduct = ({ name, unit_price, description }) => {
  return (
    <>
      <div className="card" style={{ width: "18rem" }}>
        {/* <img src="..." class="card-img-top" alt="..."/> */}
        <div className="card-body">
          <h5 className="card-title">{name}</h5>
          <p className="card-text">{unit_price}</p>
          <p className="card-text">{description}</p>
          <a href="#" className="btn btn-primary">
            Go somewhere
          </a>
        </div>
      </div>
    </>
  );
};

export default CardProduct;
