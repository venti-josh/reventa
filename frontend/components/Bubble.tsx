import React from 'react';

type BubbleProps = {
  type: 'question' | 'answer';
  content: string;
};

export const Bubble = ({ type, content }: BubbleProps) => {
  if (type === 'question') {
    return (
      <div className="flex mb-4">
        <div className="max-w-3/4 bg-gray-100 rounded-2xl px-4 py-3 text-gray-800">
          {content}
        </div>
      </div>
    );
  }

  return (
    <div className="flex mb-4 justify-end">
      <div className="max-w-3/4 bg-blue-500 rounded-2xl px-4 py-3 text-white">
        {content}
      </div>
    </div>
  );
}; 