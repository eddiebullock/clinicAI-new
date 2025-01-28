import React, { useState, useEffect } from "react";
import { TextField, Button, CircularProgress, Box, Typography } from "@mui/material";
import Editor from "./Editor"; // Import updated React Quill-based Editor
import DownloadButton from "./DownloadButton";
import { anonymizeText, generateReport } from "../services/api";

const Anonymizer = () => {
  const [text, setText] = useState("");
  const [anonymizedText, setAnonymizedText] = useState("");
  const [report, setReport] = useState("");
  const [editedContent, setEditedContent] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isReportLoading, setIsReportLoading] = useState(false);

  useEffect(() => {
    if (report) {
      setEditedContent(report); // Sync report to editor content
    }
  }, [report]);

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
      const response = await anonymizeText(text);
      setAnonymizedText(response.anonymized_text);
    } catch (err) {
      setError(err.message || "Failed to anonymize text.");
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
      const response = await generateReport(anonymizedText);
      setReport(response.report || ""); // Ensure report is a string
    } catch (err) {
      setError(err.message || "Failed to generate report.");
    } finally {
      setIsReportLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: "600px", margin: "auto", textAlign: "center" }}>
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
            Edit the Assessment Report
          </Typography>
          <Editor content={editedContent} onContentChange={setEditedContent} />
          <DownloadButton content={editedContent} />
        </Box>
      )}
    </Box>
  );
};

export default Anonymizer;
