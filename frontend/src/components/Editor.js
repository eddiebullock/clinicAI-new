import React from "react";
import ReactQuill from "react-quill";
import "react-quill/dist/quill.snow.css";

const Editor = ({ content, onContentChange }) => {
  const handleChange = (value) => {
    if (onContentChange) {
      onContentChange(value); // Pass content updates to the parent
    }
  };

  return (
    <div
      style={{
        border: "1px solid #ccc",
        borderRadius: "5px",
        minHeight: "300px",
        padding: "10px",
      }}
    >
      <ReactQuill value={content} onChange={handleChange} />
    </div>
  );
};

export default Editor;
