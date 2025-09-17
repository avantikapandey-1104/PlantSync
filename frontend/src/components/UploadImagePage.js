import React, { useState } from 'react';

const UploadImagePage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [predictionResult, setPredictionResult] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadStatus('Please select a file first.');
      return;
    }

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const response = await fetch('/upload-image/', {
        method: 'POST',
        body: formData,
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const data = await response.json();
      setPredictionResult(data);
      setUploadStatus('Upload successful!');
    } catch (error) {
      setUploadStatus('Upload failed. Please try again.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="max-w-lg min-h-96 bg-white rounded-xl shadow-lg p-8 flex flex-col items-center justify-center">
        <h2 className="text-2xl font-bold mb-4">Upload Plant Image</h2>
        <div className="flex justify-center mb-4 w-full">
          <input
            type="file"
            onChange={handleFileChange}
            className="border border-gray-300 rounded px-3 py-2 cursor-pointer block mx-auto"
          />
        </div>
        <button
          onClick={handleUpload}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          Upload
        </button>
        {uploadStatus && <p className="mt-4">{uploadStatus}</p>}
        {predictionResult && (
          <div className="w-full max-w-lg space-y-4">
            <div className="bg-green-50 border border-green-300 rounded p-4">
              <h3 className="text-lg font-semibold text-green-800 mb-2">Analysis Result</h3>
              <p><span className="font-semibold text-green-700">Disease:</span> {predictionResult.prediction}</p>
              <p><span className="font-semibold text-green-700">Confidence:</span> {predictionResult.confidence}</p>
            </div>
            <div className="bg-blue-50 border border-blue-300 rounded p-4">
              <h3 className="text-lg font-semibold text-blue-800 mb-2">Disease Description</h3>
              <p className="text-blue-700">{predictionResult.description}</p>
            </div>
            <div className="bg-yellow-50 border border-yellow-300 rounded p-4">
              <h3 className="text-lg font-semibold text-yellow-800 mb-2">Personalized Care Tips</h3>
              <ul className="list-disc list-inside text-yellow-700">
                {predictionResult.care_tips.map((tip, index) => (
                  <li key={index}>{tip}</li>
                ))}
              </ul>
            </div>
            <div className="bg-purple-50 border border-purple-300 rounded p-4">
              <h3 className="text-lg font-semibold text-purple-800 mb-2">Smart Reminders for Plant Maintenance</h3>
              <ul className="list-disc list-inside text-purple-700">
                {predictionResult.reminders.map((reminder, index) => (
                  <li key={index}>{reminder}</li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
export default UploadImagePage;
