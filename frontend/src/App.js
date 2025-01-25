import React from "react";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";

const theme = createTheme({
  palette: {
    primary: {
      main: "#1976d2", // Custom primary color
    },
    secondary: {
      main: "#dc004e", // Custom secondary color
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <div style={{ textAlign: "center", marginTop: "20px" }}>
        <Typography variant="h3" gutterBottom>
          Custom Themed Material-UI!
        </Typography>
        <Button variant="contained" color="primary">
          Primary Button
        </Button>
        <Button variant="outlined" color="secondary" style={{ marginLeft: "10px" }}>
          Secondary Button
        </Button>
      </div>
    </ThemeProvider>
  );
}

export default App;
