import React, { useState, useEffect, useRef } from 'react';
import { Bubble } from './Bubble';
import { InputField } from './InputField';
import { LoadingIndicator } from './LoadingIndicator';

type Message = {
  id: string;
  type: 'question' | 'answer';
  content: string;
};

export const Survey = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [done, setDone] = useState<boolean>(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Start the survey as soon as the page loads
    sendMessage('start');
    
    // Clean up on unmount
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, []);

  const sendMessage = async (message: string) => {
    setLoading(true);
    
    // Abort any ongoing request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    
    // Create a new AbortController for this request
    const abortController = new AbortController();
    abortControllerRef.current = abortController;
    
    try {
      // First add the user answer to the messages if not the initial 'start' message
      if (message !== 'start') {
        setMessages(prev => [
          ...prev,
          { id: Date.now().toString(), type: 'answer', content: message }
        ]);
      }

      // Make a POST request to the chat endpoint
      const response = await fetch('http://localhost:8000/api/v1/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
        signal: abortController.signal
      });

      if (!response.ok) {
        throw new Error(`Failed to send message: ${response.status}`);
      }

      if (!response.body) {
        throw new Error('Response body is empty');
      }

      // Process the response as a stream
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      processingLoop: while (true) {
        const { done, value } = await reader.read();
        
        if (value) {
          const text = decoder.decode(value, { stream: true });
          console.log('Received chunk:', text);
          buffer += text;
        }
        
        // Split buffer into potential event messages.
        // An event message is terminated by double newlines.
        let processableEventStrings = buffer.split('\n\n');
        
        if (!done) {
          // If the stream is not yet done, the last item in processableEventStrings
          // might be an incomplete event. So, we put it back into the buffer.
          buffer = processableEventStrings.pop() || '';
        } else {
          // If the stream is done, all parts in processableEventStrings are considered complete.
          // We clear the buffer as everything will be processed from processableEventStrings.
          buffer = ''; 
        }
        
        for (const eventString of processableEventStrings) {
          if (!eventString.trim()) continue; 
          
          const lines = eventString.split('\n');
          let eventType = '';
          const eventDataLines: string[] = [];
          
          for (const line of lines) {
            if (line.startsWith('event:')) {
              eventType = line.substring(6).trim();
            } else if (line.startsWith('data:')) {
              eventDataLines.push(line.substring(5).trim());
            }
          }
          const eventData = eventDataLines.join('\n');
          
          console.log('Processed event:', { eventType, eventData });
          
          if (eventType === 'message' && eventData) {
            setMessages(prev => [
              ...prev,
              { id: Date.now().toString(), type: 'question', content: eventData }
            ]);
            setLoading(false);
          } else if (eventType === 'done' || eventData === 'done') {
            console.log('Received application-level "done" event');
            setDone(true);
            setLoading(false); // Ensure loading is also false
            break processingLoop; // Exit the main stream reading loop
          } else if (eventType === 'error') {
            console.error('Error from server event:', eventData);
            setMessages(prev => [
              ...prev,
              { 
                id: Date.now().toString(), 
                type: 'question', 
                content: 'Sorry, something went wrong with the event stream. Please try again.' 
              }
            ]);
            setLoading(false);
          } else if (!eventType && eventData) {
            // Handle case where event type might not be specified (data-only)
            setMessages(prev => [
              ...prev,
              { id: Date.now().toString(), type: 'question', content: eventData }
            ]);
            setLoading(false);
          }
        }
        
        if (done) {
          console.log('End of stream reached (reader.read() returned done:true)');
          // If buffer still has content here, it implies a malformed stream ending.
          // However, the logic above should have processed all valid events.
          if (buffer.trim()) {
             console.warn('Residual buffer content after stream ended:', buffer);
          }
          break; 
        }
      }
      
    } catch (error: any) {
      if (error.name === 'AbortError') {
        console.log('Request was aborted');
      } else {
        console.error('Error communicating with server:', error);
        setMessages(prev => [
          ...prev,
          { 
            id: Date.now().toString(), 
            type: 'question', 
            content: 'Sorry, something went wrong. Please try again.' 
          }
        ]);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (answer: string) => {
    if (answer.trim() === '') return;
    sendMessage(answer);
  };

  const handleSkip = () => {
    sendMessage('skip');
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
        {messages.map((message) => (
          <Bubble 
            key={message.id} 
            type={message.type} 
            content={message.content} 
          />
        ))}
        {loading && <LoadingIndicator />}
        <div ref={messagesEndRef} />
      </div>
      
      {!loading && messages.length > 0 && (
        <div className="sticky bottom-0 bg-white pt-2">
          <InputField onSubmit={handleSubmit} />
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