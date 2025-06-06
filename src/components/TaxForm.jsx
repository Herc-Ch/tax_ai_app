// src/components/TaxForm.jsx
import { useState } from "react";

const TaxForm = () => {
  const [form, setForm] = useState({
    name: "",
    year: new Date().getFullYear(),
    income: "",
    expenses: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://localhost:5000/api/submit-tax", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      const result = await response.json();
      alert("Server says: " + result.message);
    } catch (err) {
      alert("Error submitting form: " + err);
    }
  };

  return (
    <form className="tax-form" onSubmit={handleSubmit}>
      <label>
        Name:
        <input name="name" value={form.name} onChange={handleChange} required />
      </label>
      <label>
        Year:
        <input
          name="year"
          type="number"
          value={form.year}
          onChange={handleChange}
          required
        />
      </label>
      <label>
        Income (€):
        <input
          name="income"
          type="number"
          value={form.income}
          onChange={handleChange}
          required
        />
      </label>
      <label>
        Expenses (€):
        <input
          name="expenses"
          type="number"
          value={form.expenses}
          onChange={handleChange}
          required
        />
      </label>
      <button type="submit">Submit</button>
    </form>
  );
};

export default TaxForm;
