import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import "bootstrap/dist/css/bootstrap.css";
import { Auth0Provider } from "@auth0/auth0-react";
import { BrowserRouter } from "react-router-dom";
// import { useState } from "react";
const domain = import.meta.env.VITE_REACT_APP_AUTH0_DOMAIN;
const clientId = import.meta.env.VITE_REACT_APP_AUTH0_CLIENT_ID;
console.log(domain);
console.log(clientId);
// const [accessToken, setAccessToken] = useState("");
// const accessToken = useAccessToken();
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <Auth0Provider
        domain={domain}
        clientId={clientId}
        authorizationParams={{
          // redirect_uri: window.location.origin + "/landingPage",
          redirect_uri:
            "https://yes-company-frontend-react.onrender.com/landingPage",
          audience: "https://yesCompany/api",
        }}
        // useRefreshTokens={true}
        // cacheLocation="localstorage"
        // token={
        //   "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRjNE5WN1pyeUppemVKdW5wblI0MyJ9.eyJpc3MiOiJodHRwczovL2Rldi10aW9pNGJuZmlzYzZiY2xpLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExNTYxOTgzMTY3OTE3MzcxMTA4NyIsImF1ZCI6Imh0dHBzOi8veWVzQ29tcGFueS9hcGkiLCJpYXQiOjE3MTA3NDg5MzksImV4cCI6MTcxMDc1NjEzOSwic2NvcGUiOiIiLCJhenAiOiJYREJEOGN5VDl1WVlnUVpqaEJHSVEzekF3UWF5Q29PSCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpvcmRlcnMiLCJkZWxldGU6cHJvZHVjdHMiLCJnZXQ6Y3VzdG9tZXJzIiwiZ2V0Om9yZGVycyIsImdldDpvcmRlcnNCeUN1c3RvbWVySWQiLCJnZXQ6b3JkZXJzLWJ5LWRhdGUiLCJnZXQ6cHJvZHVjdHMiLCJwYXRjaDpvcmRlcnMiLCJwYXRjaDpwcm9kdWN0cyIsInBvc3Q6b3JkZXJzIiwicG9zdDpwcm9kdWN0cyIsInNlYXJjaDpjdXN0b21lcnMiLCJzZWFyY2g6cHJvZHVjdHMiXX0.KescLJH9vcUI8ch4wJT_O49bN-ZFUPBfFMTOdXCxexDbnV-u6sVYj9BGyu9fjF29Ih41WbUkXiyeiyBAwcYAJdMcQmEt51v3NqDNs5sLMGHXolN_JObvmYEs2rvIyeop1h9JkahWBknBAQBoZoWyQULAq4_RTP9uM5a3mZlHMIBsfkukpqSxdz83RLWTgBKYcJrkNCeAjzN-Xsd5bs5B2G9dCykHIh2GZs6s8711VOnCEbrMxYg5rVJkJDTAlRkRPgxJhyBgxgjiwXVN3YJAl8Bgh5eCnyRYwbewqY4ke-n3msuKH2L4rnrwCMEyANWUhnlfLuOOar0MvfTaXJyMYQ"
        // }
      >
        <App />
      </Auth0Provider>
    </BrowserRouter>
  </React.StrictMode>
);
