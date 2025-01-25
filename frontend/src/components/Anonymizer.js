import React, { useState } from "react";
import { TextField, Button, CircularProgress, Box, Typography } from "@mui/material";

const Anonymizer = () => {
  const [text, setText] = useState("");
  const [anonymizedText, setAnonymizedText] = useState("");
  const [report, setReport] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isReportLoading, setIsReportLoading] = useState(false);

  const handleAnonymize = async () => {
    if (!text.trim()) {
      setError("Please enter some text.");
      return;
    }
  
    setIsLoading(true);
    setError("");
    setAnonymizedText("");
    setReport("");
  
    try {
      const response = await fetch("http://localhost:5000/api/anonymize", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });
  
      const data = await response.json();
      if (response.ok) {
        setAnonymizedText(data.anonymized_text);
      } else {
        setError(data.error || "Failed to anonymize text.");
      }
    } catch (err) {
      setError("An error occurred. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };  

  const handleGenerateReport = async () => {
    if (!anonymizedText.trim()) {
      setError("Anonymized text is required to generate a report.");
      return;
    }
  
    setIsReportLoading(true);
    setError("");
    setReport("");
  
    try {
      const response = await fetch("http://localhost:5000/api/generate_report", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ anonymized_text: anonymizedText }),
      });
  
      const data = await response.json();
      if (response.ok) {
        setReport(data.report);
      } else {
        setError(data.error || "Failed to generate report.");
      }
    } catch (err) {
      setError("An error occurred. Please try again.");
    } finally {
      setIsReportLoading(false);
    }
  };  

  return (
    <Box
      sx={{
        maxWidth: "600px",
        margin: "auto",
        textAlign: "center",
      }}
    >
      <TextField
        label="Enter text to anonymize"
        multiline
        rows={6}
        variant="outlined"
        fullWidth
        value={text}
        onChange={(e) => setText(e.target.value)}
        error={!!error}
        helperText={error}
        sx={{ marginBottom: "20px" }}
      />
      <Button
        variant="contained"
        color="primary"
        onClick={handleAnonymize}
        disabled={isLoading}
        sx={{ marginBottom: "20px" }}
      >
        {isLoading ? <CircularProgress size={24} color="inherit" /> : "Anonymize"}
      </Button>
      {anonymizedText && (
        <Box sx={{ marginTop: "20px", textAlign: "left" }}>
          <Typography variant="h6" gutterBottom>
            Anonymized Text
          </Typography>
          <TextField
            value={anonymizedText}
            multiline
            rows={6}
            variant="outlined"
            fullWidth
            InputProps={{
              readOnly: true,
            }}
          />
          <Button
            variant="contained"
            color="secondary"
            onClick={handleGenerateReport}
            disabled={isReportLoading}
            sx={{ marginTop: "20px" }}
          >
            {isReportLoading ? <CircularProgress size={24} color="inherit" /> : "Generate Assessment Report"}
          </Button>
        </Box>
      )}
      {report && (
        <Box sx={{ marginTop: "20px", textAlign: "left" }}>
          <Typography variant="h6" gutterBottom>
            Assessment Report
          </Typography>
          <Typography variant="body1" sx={{ whiteSpace: "pre-wrap" }}>
            {report}
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default Anonymizer;
