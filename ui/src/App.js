import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Workouts from "./Workouts";

function App() {
  return (
    <Router>
      <nav style={{ padding: "1rem" }}>
        <Link to="/">Home</Link> | <Link to="/workouts">Workouts</Link>
      </nav>
      <Routes>
        <Route path="/" element={<h1>Welcome to the Fitness App</h1>} />
        <Route path="/workouts" element={<Workouts />} />
      </Routes>
    </Router>
  );
}

export default App;
