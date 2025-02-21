import React, { useState } from "react";
import { Container, Typography, Box } from "@mui/material";
import FileUpload from "./components/FileUpload";
import ReportDisplay from "./components/ReportDisplay";

function App() {
  const [report, setReport] = useState(null);

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 5, textAlign: "center" }}>
        <Typography variant="h4" gutterBottom>
          ADHD Assessment Report Generator
        </Typography>
        <FileUpload setReport={setReport} />
        {report && <ReportDisplay report={report} />}
      </Box>
    </Container>
  );
}

export default App;
