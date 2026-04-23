import React, { useState } from "react";

function Form({ setResult }) {
    const [formData, setFormData] = useState({
        age: "",
        weight: "",
        goal: "fat_loss"
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const response = await fetch("http://127.0.0.1:8000/api/recommend/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        setResult(data);
    };

    return (
        <form onSubmit={handleSubmit}>
            <input name="age" placeholder="Age" onChange={handleChange} />
            <input name="weight" placeholder="Weight" onChange={handleChange} />

            <select name="goal" onChange={handleChange}>
                <option value="fat_loss">Fat Loss</option>
                <option value="muscle_gain">Muscle Gain</option>
            </select>

            <button type="submit">Get Plan</button>
        </form>
    );
}

export default Form;