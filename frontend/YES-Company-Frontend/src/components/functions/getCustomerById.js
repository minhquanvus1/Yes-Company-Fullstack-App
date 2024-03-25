import axios from "axios";
import { baseURL } from "../../baseURL";

export const getCustomerById = async (token, id) => {
  try {
    const response = await axios.get(`${baseURL}/customers/${id}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data.customer;
  } catch (error) {
    console.log(error);
  }
};
