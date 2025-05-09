import React, { useState, FormEvent, KeyboardEvent } from 'react';

type InputFieldProps = {
  onSubmit: (answer: string) => void;
};

export const InputField = ({ onSubmit }: InputFieldProps) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      onSubmit(input);
      setInput('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="relative">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Type your answer..."
        className="w-full p-3 pr-12 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        aria-label="Type your answer"
        tabIndex={0}
      />
      <button
        type="submit"
        className="absolute right-2 top-1/2 transform -translate-y-1/2 w-8 h-8 flex items-center justify-center bg-blue-500 text-white rounded-full hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        aria-label="Submit answer"
        tabIndex={0}
      >
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          viewBox="0 0 20 20" 
          fill="currentColor" 
          className="w-5 h-5"
        >
          <path 
            fillRule="evenodd" 
            d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" 
            clipRule="evenodd" 
          />
        </svg>
      </button>
    </form>
  );
}; 