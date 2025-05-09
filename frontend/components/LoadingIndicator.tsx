import React from 'react';

export const LoadingIndicator = () => {
  return (
    <div className="flex mb-4">
      <div className="flex space-x-2 bg-gray-100 rounded-2xl px-4 py-3">
        <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: '0ms' }}></div>
        <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: '150ms' }}></div>
        <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: '300ms' }}></div>
      </div>
    </div>
  );
}; 