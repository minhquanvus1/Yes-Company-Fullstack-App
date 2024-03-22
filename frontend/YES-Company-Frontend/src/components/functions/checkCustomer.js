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
    if (response.status === 200) {
      setIsAlreadyCustomer(true);
    } else {
      setIsAlreadyCustomer(false);
    }
    setIsLoading(false);
    const responseData = await response.json();
    console.log(responseData);
  } catch (error) {
    console.log("error");
    console.log(error.error);
  }
};
