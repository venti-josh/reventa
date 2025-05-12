import React from 'react';
import { useRouter } from 'next/router';
import { Survey } from '../components/Survey';

const SurveyPage = () => {
  const router = useRouter();
  const { surveyId } = router.query;

  // Wait for router to be ready
  if (!router.isReady) {
    return <div className="container mx-auto max-w-md h-screen flex items-center justify-center">Loading...</div>;
  }

  // Make sure surveyId is a string
  if (typeof surveyId !== 'string') {
    return (
      <div className="container mx-auto max-w-md h-screen flex items-center justify-center text-center">
        <div>
          <h1 className="text-xl font-bold mb-4">Invalid Survey ID</h1>
          <p>Please check your URL and try again.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto max-w-md h-screen">
      <Survey surveyInstanceId={surveyId} />
    </div>
  );
};

export default SurveyPage; 