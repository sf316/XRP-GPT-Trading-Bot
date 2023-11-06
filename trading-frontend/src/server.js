const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors()); 
app.use(express.json());

app.post('/submit-form', (req, res) => {
  const { walletAddress, openaiKey, desiredCurrency, issuerAddress } = req.body;

  const pythonProcess = spawn('python', [
    '../../main.py',
    JSON.stringify(req.body),
  ]);

  pythonProcess.stdout.on('data', (data) => {
    res.json(JSON.parse(data.toString()));
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
    res.status(500).send('An error occurred');
  });
});

app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});