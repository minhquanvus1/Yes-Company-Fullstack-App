const baseURL =
  import.meta.env.MODE === "production"
    ? import.meta.env.VITE_REACT_APP_BASE_URL
    : "http://localhost:8080";
export { baseURL };
