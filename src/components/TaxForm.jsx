import { useState, useRef, useEffect } from 'react'

const TaxForm = () => {
  const [form, setForm] = useState({
    filing_status: 'single',
    age: '',
    country: '',
    employment_type: 'employee',
    income: '',
    work_expenses: '',
    mortgage_interest: '',
    charity_donations: '',
    education_expenses: '',
    retirement_contributions: '',
    dependents: ''
  })
  const [advice, setAdvice] = useState('')
  const adviceRef = useRef(null)

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    await fetch('http://localhost:5000/api/submit-tax', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    })

    // Now get AI advice
    try {
      const response = await fetch('http://localhost:5000/api/ai-tax-advice', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      })
      const result = await response.json()
      setAdvice(result.advice || result.error || 'No advice available.')
    } catch (err) {
      setAdvice('Error getting AI advice: ' + err.message)
    }
  }

  // Scroll to advice when it appears
  useEffect(() => {
    if (advice && adviceRef.current) {
      setTimeout(() => {
        adviceRef.current.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        })
      }, 100) // Small delay to ensure advice is rendered
    }
  }, [advice])

  return (
    <div>
      <form className='tax-form' onSubmit={handleSubmit}>
        <label>
          Filing Status:
          <select
            name='filing_status'
            value={form.filing_status}
            onChange={handleChange}
            required
          >
            <option value='single'>Single</option>
            <option value='married_joint'>Married Filing Jointly</option>
            <option value='married_separate'>Married Filing Separately</option>
            <option value='head_household'>Head of Household</option>
          </select>
        </label>
        <label>
          Age:
          <input
            name='age'
            type='number'
            value={form.age}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          Country:
          <input
            name='country'
            value={form.country}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          Employment Type:
          <select
            name='employment_type'
            value={form.employment_type}
            onChange={handleChange}
            required
          >
            <option value='employee'>Employee</option>
            <option value='self_employed'>Self-Employed</option>
            <option value='both'>Both</option>
          </select>
        </label>
        <label>
          Total Income (€):
          <input
            name='income'
            type='number'
            value={form.income}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          Work-related Expenses (€):
          <input
            name='work_expenses'
            type='number'
            value={form.work_expenses}
            onChange={handleChange}
          />
        </label>
        <label>
          Mortgage Interest (€):
          <input
            name='mortgage_interest'
            type='number'
            value={form.mortgage_interest}
            onChange={handleChange}
          />
        </label>
        <label>
          Charitable Donations (€):
          <input
            name='charity_donations'
            type='number'
            value={form.charity_donations}
            onChange={handleChange}
          />
        </label>
        <label>
          Education Expenses (€):
          <input
            name='education_expenses'
            type='number'
            value={form.education_expenses}
            onChange={handleChange}
          />
        </label>
        <label>
          Retirement Contributions (€):
          <input
            name='retirement_contributions'
            type='number'
            value={form.retirement_contributions}
            onChange={handleChange}
          />
        </label>
        <label>
          Number of Dependents:
          <input
            name='dependents'
            type='number'
            value={form.dependents}
            onChange={handleChange}
          />
        </label>
        <button type='submit'>Submit</button>
      </form>

      {advice && (
        <div
          ref={adviceRef}
          className='advice'
          style={{
            marginTop: '1em',
            background: '#f5f5f5',
            padding: '1em',
            borderRadius: '8px'
          }}
        >
          <strong>AI Tax Advice:</strong>
          <div>{advice}</div>
        </div>
      )}
    </div>
  )
}

export default TaxForm
