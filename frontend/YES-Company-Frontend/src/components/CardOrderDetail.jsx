import React from "react";

const CardOrderDetail = ({ productName, unitPrice, quantity }) => {
  return (
    <div
      className="card"
      style={{
        maxWidth: "50%",
        marginLeft: "20%",
        marginRight: "20%",
      }}
    >
      <div className="card-body">
        <h5 className="card-title">{`Product Name: ${productName}`}</h5>
        <p className="card-text">{`Unit Price: ${unitPrice}k (VND)`}</p>
        <p className="card-text">{`Order Quantity: ${quantity}`}</p>
        {/* <a href="#" className="btn btn-primary">
          Go somewhere
        </a> */}
      </div>
    </div>
  );
};

export default CardOrderDetail;
