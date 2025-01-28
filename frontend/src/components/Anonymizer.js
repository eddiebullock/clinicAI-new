import React, { useState, useEffect } from "react";
import { TextField, Button, Checkbox, CircularProgress, Box, Typography, FormControlLabel } from "@mui/material";
import DraftEditor from "./Editor";
import DownloadButton from "./DownloadButton";
import { anonymizeText, generateReport } from "../services/api";

const Anonymizer = () => {
  const [text, setText] = useState("");
  const [transcript, setTranscript] = useState(""); // For the assessment transcript
  const [includeTranscript, setIncludeTranscript] = useState(false); // Checkbox state
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
    if (!text.trim() && (!includeTranscript || !transcript.trim())) {
      setError("Please enter clinician notes or upload a transcript.");
      return;
    }

    const combinedText = `${text}\n${includeTranscript && transcript ? transcript : ""}`.trim();

    setIsLoading(true);
    setError("");
    setAnonymizedText("");
    setReport("");

    try {
      const response = await anonymizeText(combinedText);
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
        label="Enter clinician notes"
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

      <Typography variant="h6" gutterBottom>
        Add assessment transcript
      </Typography>
      <FormControlLabel
        control={
          <Checkbox
            checked={includeTranscript}
            onChange={(e) => setIncludeTranscript(e.target.checked)}
          />
        }
        label="Include transcript"
        sx={{ display: "block", marginBottom: "20px", textAlign: "left" }}
      />
      {includeTranscript && (
        <TextField
          label="Paste assessment transcript here"
          multiline
          rows={6}
          variant="outlined"
          fullWidth
          value={transcript}
          onChange={(e) => setTranscript(e.target.value)}
          sx={{ marginBottom: "20px" }}
        />
      )}

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
          <DraftEditor content={editedContent} onContentChange={setEditedContent} />
          <DownloadButton content={editedContent} />
        </Box>
      )}
    </Box>
  );
};

export default Anonymizer;
