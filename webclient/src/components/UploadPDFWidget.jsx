import React, { useState, useRef } from "react";
import {
  FaCircleArrowRight,
  FaCircleArrowLeft,
  FaUpload,
} from "react-icons/fa6";

function UploadPDFWidget({ onFileUpload }) {
  const [document, setDocument] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    const files = e.dataTransfer.files;
    handleFiles(files);
  };

  const handleFileInput = (e) => {
    const files = e.target.files;
    handleFiles(files);
  };

  const handleFiles = (files) => {
    if (files.length > 0) {
      const file = files[0];
      if (file.type === "application/pdf") {
        setDocument(file);
        onFileUpload(file);
      } else {
        alert("Please upload a PDF file.");
      }
    }
  };

  return (
    <form className="md:w-[704px] md:h-[396px] sm:w-[100%] sm:h-[360px] m-auto -translate-y-20 rounded-[16px] shadow-lg md:hover:shadow-2xl linear-anim-transitions border-[2px] relative">
      <div className="flex flex-col justify-center align-top w-full h-full">
        <div className="text-center mb-2 hover:cursor-pointer">
          <h1 className="text-[24px] select-none">Step 42</h1>
          <h2 className="text-[16px] text-gray-500 select-none">
            Upload your{" "}
            <span className="text-black font-semibold">
              Academic Advising PDF
            </span>{" "}
            document.
          </h2>
        </div>
        <div
          className={`flex flex-col items-center justify-center mx-auto w-[50%] h-[200px] border-2 border-dashed rounded-[12px] cursor-pointer transition-all duration-300 ${
            isDragging
              ? "border-blue-500 bg-blue-50"
              : "border-gray-300 hover:border-gray-400 hover:bg-gray-50"
          }`}
          onDragEnter={handleDragEnter}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current.click()}
        >
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileInput}
            accept=".pdf"
            className="hidden"
          />
          {document ? (
            <div className="text-center">
              <p className="text-green-600 font-semibold">Upload Successful!</p>
              <p className="text-gray-600">Please Proceed</p>
            </div>
          ) : (
            <>
              <FaUpload className="text-4xl text-gray-400" />
              <p className="text-gray-600 ">Drag and drop your PDF here</p>
              <p className="text-gray-400">or</p>
              <p className="text-blue-500 font-semibold">Click to upload</p>
            </>
          )}
        </div>
      </div>
    </form>
  );
}

export default UploadPDFWidget;
