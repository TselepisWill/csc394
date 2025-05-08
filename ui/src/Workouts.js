import React, { useEffect, useState } from "react";

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/workouts")
      .then((res) => res.json())
      .then((data) => {
        setWorkouts(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching workouts:", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading workouts...</p>;

  return (
    <div style={{ padding: "1rem", fontFamily: "sans-serif" }}>
      <h2>My Workouts</h2>
      <ul>
        {workouts.map((workout) => (
          <li key={workout.id}>
            {workout.workout_name} — {workout.muscle_group}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Workouts;


