import React from 'react';

const LandingPage = () => {
  return (
    <div className="container mx-auto max-w-md h-screen flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-2xl font-bold mb-4">Survey Platform</h1>
        <p className="mb-4">Please access your survey using the URL provided to you.</p>
        <p className="text-sm text-gray-500">Format: /{'{survey_id}'}</p>
      </div>
    </div>
  );
};

export default LandingPage; 