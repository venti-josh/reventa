# Typeform-Style Survey App

A minimal, Typeform-style survey web app that communicates with an existing chat-based backend using Server-Sent Events (SSE).

## Features

- Single-question view showing one question at a time
- Clean, minimalist interface with chat-like bubbles
- History of previous questions and answers
- Smooth scrolling to highlight new questions
- Loading indicator during API requests
- Skip option for any question
- Real-time response streaming via SSE

## Getting Started

1. Install dependencies:
```bash
npm install
# or
yarn install
```

2. Set up environment variables:
   - Create a `.env` file in the frontend directory
   - Add the following variables (adjust as needed):
   ```
   BACKEND_API_URL=http://localhost:3001/api/v1/chat
   API_URL=http://localhost:3001/api
   ```

3. Run the development server:
```bash
npm run dev
# or
yarn dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser to see the survey.

## API Integration

The app connects to an existing chat-based backend using Server-Sent Events (SSE):

- Initial requests are sent with `?message=start` to initialize the survey
- Each answer or "skip" action is sent as a query parameter
- The server keeps the connection open and streams responses in real-time
- When the server sends `{ "message": "done" }`, the survey concludes

### Server-Sent Events

This application uses the EventSource API to establish persistent connections with the server, allowing for real-time streaming of responses. This provides several benefits:

- Real-time updates without polling
- Automatic reconnection if the connection is lost
- Efficient one-way communication from server to client

## Technologies Used

- React with TypeScript
- Next.js for server-side rendering and API routing
- Tailwind CSS for styling 