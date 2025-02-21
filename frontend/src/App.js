import React, { useState } from "react";
import { Container, Typography } from "@mui/material";
import FileUpload from "./components/FileUpload";
import ReportDisplay from "./components/ReportDisplay";

function App() {
  const [report, setReport] = useState([]); // Ensure report is state-managed properly

  console.log("📢 Current Report State:", report);

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Psychological Assessment Report Generator
      </Typography>
      <FileUpload setReport={setReport} />
      <ReportDisplay report={report} />
    </Container>
  );
}

export default App;
