import axios from "axios";
const API_BASE_URL = "http://127.0.0.1:5000"; // Change this if your backend is hosted elsewhere

export const uploadTranscript = async (file, assessmentType) => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("assessment_type", assessmentType);
  
    try {
      const response = await fetch(`${API_BASE_URL}/generate_report`, {
        method: "POST",
        body: formData,
      });
  
      const data = await response.json();
      console.log("🔄 API Response:", data); // Log the entire response
  
      if (!response.ok) {
        throw new Error(data.error || "Unknown error occurred.");
      }
  
      return data.report;
    } catch (error) {
      console.error("🚨 Error in API Call:", error);
      throw error;
    }
  };
  
