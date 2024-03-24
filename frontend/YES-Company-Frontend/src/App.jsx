// import { useState, useEffect } from "react";
import { Routes, Route } from "react-router-dom";
import "./App.css";
import LoginButton from "./components/LoginButton";
import LogoutButton from "./components/LogoutButton";
import { useAuth0 } from "@auth0/auth0-react";
// import LandingPage from "./components/LandingPage";
import CreateCustomerForm from "./components/CreateCustomerForm";
import CreateProductForm from "./components/CreateProductForm";
import IntroPage from "./components/pages/IntroPage";
import LandingPage from "./components/pages/LandingPage";
import CustomerTable from "./components/CustomerTable";
import UpdateProduct from "./components/UpdateProduct";
import AllOrdersPage from "./components/pages/AllOrdersPage";
import OrderDetailsPage from "./components/pages/OrderDetailsPage";
// import { useState, useEffect } from "react";
// import axios from "axios";
function App() {
  const { isLoading, error } = useAuth0();

  // function useAccessToken() {
  //   useEffect(() => {
  //     async function fetchAccessToken() {
  //       const data = {
  //         client_id: "XDBD8cyT9uYYgQZjhBGIQ3zAwQayCoOH",
  //         client_secret:
  //           "dsnK8431RJRlVoMs7XiRfyVUyNKsHn1fpBgFpgtsPefeIOMooPi_siAnOkv1a5Sw",
  //         audience: "https://dev-tioi4bnfisc6bcli.us.auth0.com/api/v2/",
  //         grant_type: "client_credentials",
  //       };

  //       const config = {
  //         method: "post",
  //         url: "https://dev-tioi4bnfisc6bcli.us.auth0.com/oauth/token",
  //         headers: { "Content-Type": "application/json" },
  //         data: data,
  //       };

  //       try {
  //         const response = await axios(config);
  //         setAccessToken(response.data.access_token);
  //       } catch (error) {
  //         console.error(error);
  //       }
  //     }

  //     fetchAccessToken();
  //   }, []);

  //   return accessToken;
  // }
  return (
    <>
      <Routes>
        <Route path="/" element={<IntroPage></IntroPage>}></Route>
        <Route
          path="/landingPage"
          element={<LandingPage></LandingPage>}
        ></Route>
        <Route path="/customers" element={<CustomerTable />}></Route>
        <Route
          path="/products/:id"
          element={<UpdateProduct></UpdateProduct>}
        ></Route>
        <Route
          path="/products/create"
          element={<CreateProductForm></CreateProductForm>}
        ></Route>
        <Route
          path="/customers/create"
          element={<CreateCustomerForm></CreateCustomerForm>}
        ></Route>
        <Route path="/orders" element={<AllOrdersPage></AllOrdersPage>}></Route>
        <Route
          path="/orders/:id"
          element={<OrderDetailsPage></OrderDetailsPage>}
        ></Route>
      </Routes>
      {/* {error && <p>Authentication Error</p>}
      {!error && isLoading && <p>Loading...</p>}
      {!error && !isLoading && (
        <>
          <LoginButton />
          <LandingPage />
          <LogoutButton />
        </>
      )} */}
      {/* <Router>
        <Routes>
          <Route exact path="/" component={LandingPage} />
          <Route exact path="/createCustomer" component={CreateCustomerForm} />
          <Route exact path="/createProduct" component={CreateProductForm} />
        </Routes>
      </Router> */}
    </>
  );
}

export default App;

// import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
// import { useAuth0 } from '@auth0/auth0-react';
// import LoginButton from './components/LoginButton';
// import LogoutButton from './components/LogoutButton';
// import LandingPage from './components/LandingPage';
// // import ProtectedRoute from './components/ProtectedRoute';

// function App() {
//   const { isLoading, error } = useAuth0();

//   if (error) {
//     return <p>Authentication Error</p>;
//   }

//   if (isLoading) {
//     return <p>Loading...</p>;
//   }

//   return (
//     <Router>
//       <Switch>
//         <Route path="/login" component={LoginButton} />
//         {/* <ProtectedRoute path="/landingPage" component={LandingPage} /> */}
//         <Route path="/logout" component={LogoutButton} />
//       </Switch>
//     </Router>
//   );
// }

// export default App;
