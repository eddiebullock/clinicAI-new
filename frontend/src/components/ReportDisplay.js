import React from "react";
import { Box, Typography, Paper } from "@mui/material";

function ReportDisplay({ report }) {
  console.log("📝 Rendering Report:", report); // Debugging

  // Ensure report is an array and not empty
  if (!Array.isArray(report) || report.length === 0) {
    console.warn("⚠️ Report data is empty or not an array:", report);
    return (
      <Typography variant="h6" sx={{ mt: 4, textAlign: "center", color: "gray" }}>
        No report generated yet. Please upload a file and generate a report.
      </Typography>
    );
  }

  return (
    <Box sx={{ mt: 4, display: "flex", flexDirection: "column", gap: 2 }}>
      {report.map((section, index) => {
        // Ensure section has correct structure
        if (!section || typeof section !== "object" || !section.title || !section.content) {
          console.warn(`⚠️ Invalid section format at index ${index}:`, section);
          return null; // Skip invalid sections
        }

        return (
          <Paper key={index} sx={{ p: 3, mb: 2, borderRadius: 2, backgroundColor: "#f9f9f9" }}>
            <Typography variant="h5" sx={{ fontWeight: "bold", mb: 1 }}>
              {section.title}
            </Typography>
            <Typography variant="body1" sx={{ color: "#333" }}>
              {section.content}
            </Typography>
          </Paper>
        );
      })}
    </Box>
  );
}

export default ReportDisplay;
