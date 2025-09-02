import React, { useState, useEffect, useRef } from 'react';
import { Bubble } from './Bubble';
import { InputField } from './InputField';
import { LoadingIndicator } from './LoadingIndicator';

// API configuration
const API_BASE_URL = process.env.API_URL || 'https://reventa-s82p.onrender.com';

// Add JSX namespace declaration to fix "JSX element implicitly has type 'any'" errors
declare namespace JSX {
  interface IntrinsicElements {
    div: React.DetailedHTMLProps<React.HTMLAttributes<HTMLDivElement>, HTMLDivElement>;
    h2: React.DetailedHTMLProps<React.HTMLAttributes<HTMLHeadingElement>, HTMLHeadingElement>;
    p: React.DetailedHTMLProps<React.HTMLAttributes<HTMLParagraphElement>, HTMLParagraphElement>;
    button: React.DetailedHTMLProps<React.ButtonHTMLAttributes<HTMLButtonElement>, HTMLButtonElement>;
    label: React.DetailedHTMLProps<React.LabelHTMLAttributes<HTMLLabelElement>, HTMLLabelElement>;
    input: React.DetailedHTMLProps<React.InputHTMLAttributes<HTMLInputElement>, HTMLInputElement>;
    span: React.DetailedHTMLProps<React.HTMLAttributes<HTMLSpanElement>, HTMLSpanElement>;
  }
}

interface BubbleProps {
  type: 'question' | 'answer';
  content: string;
}

type Question = {
  id: string;
  text: string;
  type: 'text' | 'multiple_choice' | 'checkbox' | 'rating';
  choices?: string[];
  min?: number;
  max?: number;
};

type SurveyResponse = {
  question: Question;
  response_id: string;
  done: boolean;
};

type HistoryItem = {
  question: Question;
  answer: any;
};

export const Survey = ({ surveyInstanceId }: { surveyInstanceId: string }) => {
  const [responseId, setResponseId] = useState<string | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [done, setDone] = useState<boolean>(false);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [history, currentQuestion]);

  useEffect(() => {
    // Start the survey as soon as the page loads
    startSurvey();
  }, [surveyInstanceId]);

  const startSurvey = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/survey-flow/instance/${surveyInstanceId}/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to start survey: ${response.status}`);
      }

      const data: SurveyResponse = await response.json();
      setResponseId(data.response_id);
      setCurrentQuestion(data.question);
    } catch (error) {
      console.error('Error starting survey:', error);
    } finally {
      setLoading(false);
    }
  };

  const submitAnswer = async (answer: any, skipped = false) => {
    if (!responseId || !currentQuestion) return;
    
    setLoading(true);
    
    try {
      // Add the question and answer to history
      setHistory((prev: HistoryItem[]) => [
        ...prev,
        { question: currentQuestion, answer: skipped ? "Skipped" : answer }
      ]);

      const response = await fetch(`${API_BASE_URL}/api/v1/survey-flow/responses/${responseId}/answer`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question_id: currentQuestion.id,
          answer: skipped ? null : { value: answer },
          skipped: skipped
        })
      });

      if (!response.ok) {
        throw new Error(`Failed to submit answer: ${response.status}`);
      }

      const data: SurveyResponse = await response.json();
      
      if (data.done) {
        setDone(true);
      } else {
        setCurrentQuestion(data.question);
      }
    } catch (error) {
      console.error('Error submitting answer:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSkip = () => {
    submitAnswer(null, true);
  };

  const renderQuestion = () => {
    if (!currentQuestion) return null;

    switch (currentQuestion.type) {
      case 'text':
        return <InputField onSubmit={(answer) => submitAnswer(answer)} />;
      
      case 'multiple_choice':
        return (
          <div className="flex flex-col space-y-2 mt-2">
            {currentQuestion.choices?.map((choice: string) => (
              <button 
                key={choice}
                className="p-2 border border-gray-300 rounded hover:bg-gray-100"
                onClick={() => submitAnswer(choice)}
              >
                {choice}
              </button>
            ))}
          </div>
        );
      
      case 'checkbox':
        return (
          <CheckboxGroup 
            choices={currentQuestion.choices || []} 
            onSubmit={(selectedItems) => submitAnswer(selectedItems)}
          />
        );
      
      case 'rating':
        return (
          <RatingInput 
            min={currentQuestion.min || 1} 
            max={currentQuestion.max || 5} 
            onSubmit={(rating) => submitAnswer(rating)}
          />
        );
      
      default:
        return <InputField onSubmit={(answer) => submitAnswer(answer)} />;
    }
  };

  if (done) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen p-4 bg-white">
        <div className="text-center p-8 rounded-lg">
          <h2 className="text-2xl font-semibold mb-2">Thanks!</h2>
          <p className="text-gray-600">Your responses have been recorded.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-screen p-4 bg-white">
      <div className="flex-1 overflow-y-auto mb-4">
        {/* Display history */}
        {history.map((item, index) => (
          <React.Fragment key={index}>
            <Bubble 
              type="question"
              content={item.question.text}
            />
            <Bubble 
              type="answer"
              content={typeof item.answer === 'object' ? JSON.stringify(item.answer) : item.answer.toString()}
            />
          </React.Fragment>
        ))}

        {/* Display current question */}
        {currentQuestion && !loading && (
          <Bubble 
            type="question"
            content={currentQuestion.text}
          />
        )}

        {loading && <LoadingIndicator />}
        <div ref={messagesEndRef} />
      </div>
      
      {!loading && currentQuestion && (
        <div className="sticky bottom-0 bg-white pt-2">
          {renderQuestion()}
          <button 
            onClick={handleSkip}
            className="text-gray-500 text-sm mt-2 mx-auto block hover:underline focus:outline-none"
            aria-label="Skip this question"
            tabIndex={0}
          >
            Skip
          </button>
        </div>
      )}
    </div>
  );
};

// Helper components for different question types

type CheckboxGroupProps = {
  choices: string[];
  onSubmit: (selected: string[]) => void;
};

const CheckboxGroup = ({ choices, onSubmit }: CheckboxGroupProps) => {
  const [selected, setSelected] = useState<string[]>([]);
  
  const toggleItem = (item: string) => {
    setSelected(prev => 
      prev.includes(item)
        ? prev.filter(i => i !== item)
        : [...prev, item]
    );
  };
  
  return (
    <div className="flex flex-col space-y-2">
      {choices.map(choice => (
        <label key={choice} className="flex items-center space-x-2 cursor-pointer">
          <input 
            type="checkbox" 
            checked={selected.includes(choice)}
            onChange={() => toggleItem(choice)}
            className="h-5 w-5"
          />
          <span>{choice}</span>
        </label>
      ))}
      <button 
        onClick={() => onSubmit(selected)}
        className="mt-4 bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded"
        disabled={selected.length === 0}
      >
        Submit
      </button>
    </div>
  );
};

type RatingInputProps = {
  min: number;
  max: number;
  onSubmit: (rating: number) => void;
};

const RatingInput = ({ min, max, onSubmit }: RatingInputProps) => {
  const [rating, setRating] = useState<number | null>(null);
  
  return (
    <div className="flex flex-col space-y-4">
      <div className="flex justify-between">
        {Array.from({ length: max - min + 1 }, (_, i) => min + i).map(num => (
          <button 
            key={num}
            className={`h-10 w-10 rounded-full border ${rating === num ? 'bg-blue-500 text-white' : 'border-gray-300'}`}
            onClick={() => setRating(num)}
          >
            {num}
          </button>
        ))}
      </div>
      <button 
        onClick={() => rating !== null && onSubmit(rating)}
        className="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded"
        disabled={rating === null}
      >
        Submit
      </button>
    </div>
  );
}; 