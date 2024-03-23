import { useState } from "react";
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
function App() {
  const { isLoading, error } = useAuth0();

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
        <Route
          path="/orders"
          element={<AllOrdersPage></AllOrdersPage>}
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
