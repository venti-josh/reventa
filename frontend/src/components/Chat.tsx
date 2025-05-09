"use client";

import { useState, useRef, useEffect } from "react";

// Type definitions
type MessageRole = 'user' | 'assistant';

interface Message {
  role: MessageRole;
  content: string;
}

type Messages = Message[];

// Custom hook for localStorage
function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T | ((val: T) => T)) => void] {
  // Get stored value from localStorage or use initialValue
  const getStoredValue = (): T => {
    if (typeof window === 'undefined') {
      return initialValue;
    }
    
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error('Error reading from localStorage:', error);
      return initialValue;
    }
  };

  const [storedValue, setStoredValue] = useState<T>(getStoredValue);

  // Update localStorage when storedValue changes
  const setValue = (value: T | ((val: T) => T)) => {
    try {
      // Allow value to be a function
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      
      // Save state
      setStoredValue(valueToStore);
      
      // Save to localStorage
      if (typeof window !== 'undefined') {
        window.localStorage.setItem(key, JSON.stringify(valueToStore));
      }
    } catch (error) {
      console.error('Error writing to localStorage:', error);
    }
  };

  // Sync with other tabs/windows
  useEffect(() => {
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === key && e.newValue) {
        setStoredValue(JSON.parse(e.newValue));
      }
    };

    window.addEventListener('storage', handleStorageChange);
    
    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [key]);

  return [storedValue, setValue];
}

const Chat = () => {
  const [userInput, setUserInput] = useState("");
  const [messages, setMessages] = useLocalStorage<Messages>(
    "chat-messages",
    []
  );
  const [isLoading, setIsLoading] = useState(false);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  };

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Parse SSE chunk to extract the actual data content
  const parseSSEChunk = (chunk: string): string => {
    // Split the chunk by lines and look for data: prefix
    const lines = chunk.split("\n");
    let data = "";

    for (const line of lines) {
      if (line.startsWith("data: ")) {
        data += line.substring(6); // Remove "data: " prefix
      }
    }

    return data;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!userInput.trim() || isLoading) return
  
    // 1) build your two new messages up front
    const userMessage: Message = { role: 'user', content: userInput.trim() }
    const assistantMessage: Message = { role: 'assistant', content: '' }
  
    // 2) create a local copy of the new state
    let updatedMessages: Messages = [
      ...messages,
      userMessage,
      assistantMessage,
    ]
    // push that into React (and localStorage)
    setMessages(updatedMessages)
  
    setUserInput('')
    setIsLoading(true)
  
    try {
      const res = await fetch(process.env.NEXT_PUBLIC_CHAT_API as string, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage.content }),
      })
      if (!res.ok || !res.body) throw new Error(`HTTP ${res.status}`)
  
      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let receivedText = ''
  
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
  
        const raw = decoder.decode(value, { stream: true })
        const parsed = parseSSEChunk(raw)
        if (!parsed) continue
  
        // 3) update your local copy's assistant content
        receivedText += parsed
        updatedMessages = [
          ...updatedMessages.slice(0, -1),
          { ...assistantMessage, content: receivedText },
        ]
        // 4) push the new copy into React state
        setMessages(updatedMessages)
        scrollToBottom()
      }
    } catch (err) {
      // on error, replace the assistant placeholder with an error message
      console.error(err)
      updatedMessages = [
        ...updatedMessages.slice(0, -1),
        { ...assistantMessage, content: 'Sorry, there was an error.' },
      ]
      setMessages(updatedMessages)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-screen bg-white border shadow-sm">
      <div 
        className="flex-1 overflow-y-auto p-4 space-y-4"
        ref={chatContainerRef}
      >
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`relative max-w-[80%] px-4 py-2 rounded-2xl shadow-sm
                ${message.role === "user" 
                  ? "bg-blue-500 text-white after:content-[''] after:absolute after:right-0 after:bottom-0 after:border-8 after:border-transparent after:border-r-blue-500 after:rotate-45 after:translate-x-2 after:-translate-y-1" 
                  : "bg-gray-200 text-gray-800 after:content-[''] after:absolute after:left-0 after:bottom-0 after:border-8 after:border-transparent after:border-l-gray-200 after:rotate-[-45deg] after:-translate-x-2 after:-translate-y-1"}`}
            >
              {message.content ||
                (message.role === "assistant" &&
                isLoading &&
                index === messages.length - 1
                  ? "..."
                  : "")}
            </div>
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="border-t p-4 bg-gray-50">
        <div className="flex space-x-2">
          <textarea
            className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            placeholder="Type your message here..."
            rows={1}
            disabled={isLoading}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSubmit(e);
              }
            }}
          />
          <button
            type="submit"
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            disabled={isLoading || !userInput.trim()}
          >
            {isLoading ? "Sending..." : "Send"}
          </button>
        </div>
      </form>
    </div>
  );
};

export default Chat;
