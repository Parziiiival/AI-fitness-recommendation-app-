import React from "react";

function Result({ result }) {
    if (!result) return null;

    return (
        <div>
            <h2>Result</h2>
            <p>Workout: {result.workout}</p>
            <p>Diet: {result.diet}</p>
            <p>Calories: {result.calories}</p>
        </div>
    );
}

export default Result;