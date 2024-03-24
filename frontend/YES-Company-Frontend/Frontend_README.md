# YES-Company (Frontend)

- For the Backend functionality comes to live, and the Customer, and Manager can explore the full functionality that the Backend offers, we develop the Frontend with React JS v18, and Bootstrap v5.2.3. The Frontend is a Single Page Application (SPA) that allows the user to navigate through the different sections of the application without the need to reload the page. The Frontend is connected to the Backend through the API that the Backend offers.

- The Frontend React has different Views, depending on which Role you are when you log in. That is, the Customer will see the different View to use the functionality that provides exclusively for Customer role, and Manager will see different View to use the functionality that provides exclusively for Manager role.

- The Frontend React also integrates with Auth0 for the authentication and authorization of the users. Auth0 is a flexible, drop-in solution to add authentication and authorization services to the application. Auth0 provides a universal authentication & authorization platform for web, mobile, and legacy applications.

- The Frontend techstack also includes: Axios, Vite, React Router, React Bootstrap, and Auth0Provider.

## Getting Started

### Pre-requisite and Local Development

- Developers should have Node.js installed in their local machine. If you don't have Node.js installed, you can download it from [Node.js](https://nodejs.org/en/), and npm will be installed with Node.js.

- The Frontend React are installed by using Vite. Vite is a build tool that aims to provide a faster and leaner development experience for modern web projects. It consists of two major parts: a dev server that provides rich feature enhancements over native ES modules, and a build command that bundles your code with Rollup.

- To install Vite, run the following command in the terminal:

```bash
cd frontend
cd YES-Company-Frontend
npm install vite@latest
```

- All the dependencies, libraries used for this Frontend React project are listed in the `package.json` file. To install all the dependencies, run the following command in the terminal:

```bash
cd frontend
cd YES-Company-Frontend
npm install
```

- Then, to start the Frontend React, run the following command in the terminal:

```bash
cd frontend
cd YES-Company-Frontend
npm run dev
```

- The Frontend React will start running on `http://localhost:3000/`. Open the browser and navigate to `http://localhost:3000/` to see the Frontend React.

## Frontend Structure

- The Frontend React has the following structure:

  - `src/` folder: Contains all the source code of the Frontend React.
    - `components/` folder: Contains all the components that are used in the Frontend React.
      - `pages/` folder: Contains all the pages that are used in the Frontend React.
      - `functions/` folder: Contains all the functions that are used in the Frontend React.
      - `utils/` folder: Contains all the utility components that are used in the Frontend React.
    - `App.jsx` file: Contains the Router of the Frontend React.
    - `main.jsx` file: Contains the Auth0Provider of the Frontend React
  - `public` folder: Contains the `index.html` file that is the main HTML file of the Frontend React.
  - `vite.config.js` file: Contains the configuration of the Vite build tool (including define the PORT of the Frontend React to 3000, in lieu of the default 5173 of Vite).
  - `.env` file: Contains the Auth0 DOMAIN, and Auth0 ClientID as environment variables, in this format so that Vite can recognize them as environment variables:

  ```bash
  VITE_REACT_APP_AUTH0_DOMAIN=dev-tioi4bnfisc6bcli.us.auth0.com
  VITE_REACT_APP_AUTH0_CLIENT_ID=XDBD8cyT9uYYgQZjhBGIQ3zAwQayCoOH
  ```

## Frontend Functionality with Auth0

- After the User logs in successfully to the Frontend app, they will automatically be directed to the `http://localhost:3000/landingPage`, which has different View, depending on which Role the Authenticated User is.

## Deployment

## Author:

Quan Tran

## Acknowledgements

Thanks to the fantastic team at Udacity for their excellent Full Stack Web Development Nanodegree Program that provides me the necessary knowledge to implement this app Full Stack.
