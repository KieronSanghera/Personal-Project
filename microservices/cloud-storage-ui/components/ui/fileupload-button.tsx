'use client'

import React, { useRef } from 'react';

const FileUploadButton: React.FC = () => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleButtonClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files && files.length > 0) {
      const file = files[0];
      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await fetch('http://localhost:8080/upload', {
          method: 'POST',
          body: formData,
          headers: {
          },
        });

        if (response.ok) {
          const result = await response.json();
          console.log('File upload successful:', result);
        } else {
          console.error('File upload failed:', response.statusText);
        }
      } catch (error) {
        console.error('Error uploading file:', error);
      }
    }
  };

  return (
    <div>
      <button
        onClick={handleButtonClick}
        className="fixed right-4 bottom-4 flex h-[48px] w-[100px] justify-center items-center gap-2 rounded-md bg-gray-50 text-sm font-medium text-black hover:bg-sky-100 hover:text-blue-600"
      >
        Upload
      </button>
      
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        className="hidden"
      />
    </div>
  );
};

export default FileUploadButton;