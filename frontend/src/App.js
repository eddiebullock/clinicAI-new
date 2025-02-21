import React, { useState } from "react";
import { Container, Typography } from "@mui/material";
import FileUpload from "./components/FileUpload";
import ReportDisplay from "./components/ReportDisplay";
import DownloadButton from "./components/DownloadButton"; // Import the button

function App() {
  const [report, setReport] = useState([]); // Ensure report is state-managed properly

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Psychological Assessment Report Generator
      </Typography>
      <FileUpload setReport={setReport} />
      <ReportDisplay report={report} />
      
      {/* Show the download button only if a report exists */}
      {report.length > 0 && <DownloadButton report={report} />}
    </Container>
  );
}

export default App;
