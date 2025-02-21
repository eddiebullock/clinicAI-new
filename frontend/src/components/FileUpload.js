import React, { useState } from "react";
import { Button, Box, Typography, MenuItem, Select, FormControl, InputLabel } from "@mui/material";
import { uploadTranscript } from "../api";

function FileUpload({ setReport }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [assessmentType, setAssessmentType] = useState("adhd"); // Default to ADHD
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select a file first.");
      return;
    }

    setLoading(true);

    try {
      // 1. We get the entire response object (which might be { report: [...] } or just [...])
      const response = await uploadTranscript(selectedFile, assessmentType);

      console.log("🔄 API Response (raw):", response);

      // 2. We'll figure out if it's an array or object
      let finalReport = [];

      // If the entire response IS the array
      if (Array.isArray(response)) {
        finalReport = response;
      }
      // If the response has `report` as an array
      else if (response && Array.isArray(response.report)) {
        finalReport = response.report;
      }
      // Otherwise, we got something else
      else {
        console.error("🚨 Unexpected API response format:", response);
        alert("Unexpected response format. Please try again.");
        setLoading(false);
        return;
      }

      // 3. At this point, finalReport should be the array of sections
      console.log("✅ finalReport is:", finalReport);
      setReport(finalReport);

    } catch (error) {
      console.error("🚨 Error uploading file:", error);
      alert("Failed to generate report. Please try again.");
    }

    setLoading(false);
  };

  return (
    <Box sx={{ mt: 3, textAlign: "center" }}>
      {/* Dropdown for selecting ADHD or ASD */}
      <FormControl sx={{ minWidth: 200, mb: 2 }}>
        <InputLabel>Select Assessment Type</InputLabel>
        <Select
          value={assessmentType}
          onChange={(event) => setAssessmentType(event.target.value)}
        >
          <MenuItem value="adhd">ADHD Assessment</MenuItem>
          <MenuItem value="asd">ASD Assessment</MenuItem>
        </Select>
      </FormControl>

      {/* File Upload Button */}
      <input
        type="file"
        accept=".txt"
        onChange={handleFileChange}
        style={{ display: "none" }}
        id="file-upload"
      />
      <label htmlFor="file-upload">
        <Button variant="contained" component="span">
          Select Transcript File
        </Button>
      </label>

      {selectedFile && (
        <Typography sx={{ mt: 2 }}>{selectedFile.name}</Typography>
      )}

      {/* Upload and Process Button */}
      <Button
        variant="contained"
        color="primary"
        sx={{ mt: 2 }}
        onClick={handleUpload}
        disabled={loading}
      >
        {loading ? "Processing..." : "Generate Report"}
      </Button>
    </Box>
  );
}

export default FileUpload;
