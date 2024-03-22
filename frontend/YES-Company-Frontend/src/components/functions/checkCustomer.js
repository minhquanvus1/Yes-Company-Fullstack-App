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
      throw new Error("Network response was not ok");
    }
    const responseData = await response.json();
    console.log(responseData);
    if (response.status === 200) {
      const customer = responseData.customer;
      console.log("customer: ", customer);
      setIsAlreadyCustomer(true);
      return customer;
    } else {
      setIsAlreadyCustomer(false);
      console.log("message: ", responseData.message);
    }
    setIsLoading(false);
  } catch (error) {
    console.log("error");
    console.log(error.error);
  }
};
