export const checkCustomer = async (
  token,
  setIsAlreadyCustomer,
  setIsLoading
) => {
  try {
    setIsLoading(true);
    const response = await fetch("http://localhost:8080/check-customer", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error("This Customer not found in backend database");
      } else {
        throw new Error("Network response was not ok");
      }
    }
    const responseData = await response.json();
    console.log("response data of checkCustomer():", responseData);
    if (response.status === 200) {
      const customer = responseData.customer;
      console.log("customer: ", customer);
      setIsAlreadyCustomer(true);
      setIsLoading(false);
      return customer;
    }
    // setIsLoading(false);
  } catch (error) {
    setIsAlreadyCustomer(false);
    setIsLoading(false);
    console.log("error");
    console.log(error.message);
    throw error;
  }
};
