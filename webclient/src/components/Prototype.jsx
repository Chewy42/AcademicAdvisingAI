import React, { useState } from "react";
import UploadPDFWidget from "./UploadPDFWidget";
import Dashboard from "./Dashboard";
import axios from "axios";

function Prototype() {
  const [isFileUploaded, setIsFileUploaded] = useState(false);

  const handleFileUpload = (file) => {
    const formData = new FormData();
    formData.append("file", file);

    axios
      .post("http://localhost:5000/upload-pdf", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        withCredentials: true,
      })
      .then((response) => {
        console.log(response.data);
        setIsFileUploaded(true);
      })
      .catch((error) => {
        console.error(
          "Error uploading file:",
          error.response ? error.response.data : error.message
        );
        // Handle the error appropriately, e.g., show an error message to the user
        alert("Failed to upload file. Please try again.");
      });
  };

  return (
    <div className="*:w-[100%] h-[100%] bg-gray-50 flex justify-center align-middle">
      {isFileUploaded ? (
        <Dashboard />
      ) : (
        <UploadPDFWidget onFileUpload={handleFileUpload} />
      )}
    </div>
  );
}

export default Prototype;
