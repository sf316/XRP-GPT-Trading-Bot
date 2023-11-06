import React, { useState } from 'react';

function App() {
  const [walletAddress, setWalletAddress] = useState('');
  const [openaiKey, setOpenaiKey] = useState('');
  const [desiredCurrency, setDesiredCurrency] = useState('');
  const [issuerAddress, setIssuerAddress] = useState('');
  const [result, setResult] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch('http://localhost:5000/submit-form', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ walletAddress, openaiKey, desiredCurrency, issuerAddress }),
      });

      const data = await response.json();
      setResult(data);

      // Use the result data to show in the alert
      alert(`Action: ${data.action}\nAmount: ${data.amount}`);
    } catch (error) {
      console.error('Error submitting form:', error);
      alert('An error occurred while processing your request.');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>XRP GPT Trading Bot</h1>
      </header>
      <main>

        <div className="form-container">
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="walletAddress">Wallet Address</label>
              <input
                type="text"
                id="walletAddress"
                value={walletAddress}
                onChange={(e) => setWalletAddress(e.target.value)}
              />
            </div>
            <div className="form-group">
              <label htmlFor="openaiKey">OpenAI API Key</label>
              <input
                type="password"
                id="openaiKey"
                value={openaiKey}
                onChange={(e) => setOpenaiKey(e.target.value)}
              />
            </div>
            <div className="form-group">
              <label htmlFor="desiredCurrency">Desired Currency</label>
              <input
                type="text"
                id="desiredCurrency"
                value={desiredCurrency}
                onChange={(e) => setDesiredCurrency(e.target.value)}
                placeholder='TST'
              />
            </div>
            <div className="form-group">
              <label htmlFor="issuerAddress">Issuer Address</label>
              <input
                type="text"
                id="issuerAddress"
                value={issuerAddress}
                onChange={(e) => setIssuerAddress(e.target.value)}
                placeholder="rP9jPyP5kyvFRb6ZiRghAGw5u8SGAmU4bd"
              />
            </div>
            <button type="submit">Submit</button>
          </form>
        </div>
      </main>
    </div>
  );
}

export default App;