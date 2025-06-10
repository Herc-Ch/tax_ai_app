import React, { useState, useRef } from "react";

const FidgetSpinner = () => (
  <div className="fidget-spinner">
    <span className="fidget-spinner-euro euro1">€</span>
    <span className="fidget-spinner-euro dollar1">€</span>
    <span className="fidget-spinner-euro euro2">€</span>
  </div>
);

const LoadingOverlay = () => (
  <div
    style={{
      position: "fixed",
      inset: 0,
      background: "rgba(0,0,0,0.4)",
      zIndex: 9999,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
    }}
  >
    <FidgetSpinner />
  </div>
);

const TaxForm = ({ onAdvice }) => {
  const [form, setForm] = useState({
    filing_status: "single",
    age: "",
    country: "",
    employment_type: "employee",
    income: "",
    work_expenses: "",
    mortgage_interest: "",
    charity_donations: "",
    education_expenses: "",
    retirement_contributions: "",
    dependents: "",
  });
  const [advice, setAdvice] = useState("");
  const [loading, setLoading] = useState(false);
  const adviceRef = useRef(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const resetForm = () => {
    setAdvice("");
    setForm({
      filing_status: "single",
      age: "",
      country: "",
      employment_type: "employee",
      income: "",
      work_expenses: "",
      mortgage_interest: "",
      charity_donations: "",
      education_expenses: "",
      retirement_contributions: "",
      dependents: "",
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setAdvice("");
    try {
      await fetch("http://localhost:5000/api/submit-tax", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      const response = await fetch("http://localhost:5000/api/ai-tax-advice", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const result = await response.json();
      setAdvice(result.advice || result.error || "No advice available.");
      if (onAdvice && result.advice) {
        onAdvice(form, result.advice);
      }
    } catch (err) {
      setAdvice("Error getting AI advice: " + err.message);
    }
    setLoading(false);
  };

  return (
    <div>
      {loading && <LoadingOverlay />}
      {!advice && (
        <form
          className="tax-form p-6 rounded-xl shadow bg-white space-y-4"
          onSubmit={handleSubmit}
        >
          <label className="block">
            Filing Status:
            <select
              name="filing_status"
              value={form.filing_status}
              onChange={handleChange}
              required
              className="block w-full mt-1 p-2 rounded"
            >
              <option value="single">Single</option>
              <option value="married_joint">Married Filing Jointly</option>
              <option value="married_separate">
                Married Filing Separately
              </option>
              <option value="head_household">Head of Household</option>
            </select>
          </label>
          <label className="block">
            Age:
            <input
              name="age"
              type="number"
              value={form.age}
              onChange={handleChange}
              required
              min="18"
              max="99"
              className="block w-full mt-1 p-2 rounded"
            />
          </label>
          <label className="block">
            Country:
            <input
              name="country"
              value={form.country}
              onChange={handleChange}
              required
              className="block w-full mt-1 p-2 rounded"
            />
          </label>
          <label className="block">
            Employment Type:
            <select
              name="employment_type"
              value={form.employment_type}
              onChange={handleChange}
              required
              className="block w-full mt-1 p-2 rounded"
            >
              <option value="employee">Employee</option>
              <option value="self_employed">Self-Employed</option>
              <option value="both">Both</option>
            </select>
          </label>
          <label className="block">
            Total Income (€):
            <input
              name="income"
              type="number"
              value={form.income}
              onChange={handleChange}
              required
              className="block w-full mt-1 p-2 rounded"
            />
          </label>
          <label className="block">
            Work-related Expenses (€):
            <input
              name="work_expenses"
              type="number"
              value={form.work_expenses}
              onChange={handleChange}
              className="block w-full mt-1 p-2 rounded"
            />
          </label>
          <label className="block">
            Mortgage Interest (€):
            <input
              name="mortgage_interest"
              type="number"
              value={form.mortgage_interest}
              onChange={handleChange}
              className="block w-full mt-1 p-2 rounded"
            />
          </label>
          <label className="block">
            Charitable Donations (€):
            <input
              name="charity_donations"
              type="number"
              value={form.charity_donations}
              onChange={handleChange}
              className="block w-full mt-1 p-2 rounded"
            />
          </label>
          <label className="block">
            Education Expenses (€):
            <input
              name="education_expenses"
              type="number"
              value={form.education_expenses}
              onChange={handleChange}
              className="block w-full mt-1 p-2 rounded"
            />
          </label>
          <label className="block">
            Retirement Contributions (€):
            <input
              name="retirement_contributions"
              type="number"
              value={form.retirement_contributions}
              onChange={handleChange}
              className="block w-full mt-1 p-2 rounded"
            />
          </label>
          <label className="block">
            Number of Dependents:
            <input
              name="dependents"
              type="number"
              value={form.dependents}
              onChange={handleChange}
              className="block w-full mt-1 p-2 rounded"
            />
          </label>
          <button
            type="submit"
            className="mt-4 w-full py-2 rounded bg-blue-600 text-white font-bold hover:bg-blue-700"
          >
            Submit
          </button>
        </form>
      )}
      {advice && (
        <>
          <div
            ref={adviceRef}
            className="advice mt-6 bg-gray-50 p-6 rounded-xl shadow"
          >
            <strong>AI Tax Advice:</strong>
            <div>{advice}</div>
          </div>
          <div className="reset-btn-container mt-4">
            <button
              className="reset-btn py-2 px-4 rounded bg-gray-300 hover:bg-gray-400"
              onClick={resetForm}
            >
              Reset
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default TaxForm;
