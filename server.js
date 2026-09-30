const express = require("express");
const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");
const csv = require("csv-parser");
require("dotenv").config();

const app = express();

app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

const dataDir = path.join(__dirname, "data");
const auditFilePath = path.join(dataDir, "audit_log.csv");

if (!fs.existsSync(dataDir)) {
  fs.mkdirSync(dataDir);
}

// POST: Triage Ticket
app.post("/api/triage", (req, res) => {
  const ticketText = req.body.ticket_text || "";

  if (!ticketText.trim()) {
    return res.status(400).json({ error: "Ticket text cannot be empty." });
  }

  // Execute Python Watsonx Engine
  const pythonProcess = spawn("python", ["watsonx_engine.py", ticketText]);

  let pythonData = "";
  pythonProcess.stdout.on("data", (data) => {
    pythonData += data.toString();
  });

  pythonProcess.stderr.on("data", (data) => {
    console.error(`Python error: ${data}`);
  });

  pythonProcess.on("close", (code) => {
    try {
      const result = JSON.parse(pythonData);

      // Save to CSV Audit Log
      const timestamp = new Date()
        .toISOString()
        .replace("T", " ")
        .substring(0, 19);
      const csvLine = `"${timestamp}","${ticketText.replace(/"/g, '""')}","${result.category}",${result.urgency_score},"${result.sentiment}","${result.recommended_action}"\n`;

      if (!fs.existsSync(auditFilePath)) {
        fs.writeFileSync(
          auditFilePath,
          "timestamp,ticket_text,category,urgency,sentiment,action\n",
        );
      }
      fs.appendFileSync(auditFilePath, csvLine);

      res.json(result);
    } catch (err) {
      res.status(500).json({ error: "Failed to process ticket output." });
    }
  });
});

// GET: Operational Audit Logs
app.get("/api/logs", (req, res) => {
  if (!fs.existsSync(auditFilePath)) {
    return res.json([]);
  }

  const logs = [];
  fs.createReadStream(auditFilePath)
    .pipe(csv())
    .on("data", (row) => logs.push(row))
    .on("end", () => {
      res.json(logs.slice(-10));
    })
    .on("error", () => {
      res.status(500).json({ error: "Failed to read audit logs." });
    });
});

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`Server running at PORT ${PORT}`);
});
