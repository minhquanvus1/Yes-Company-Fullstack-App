import axios from "axios";
export const getCustomerById = async (token, id) => {
  try {
    const response = await axios.get(`http://localhost:8080/customers/${id}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data.customer;
  } catch (error) {
    console.log(error);
  }
};
