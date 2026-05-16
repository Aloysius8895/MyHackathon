# EduAI Frontend

A modern Next.js application for AI-powered education tools with session management.

## Features

### Session Management System

- **Persistent Sessions**: Sessions are automatically saved to localStorage
- **User Context**: Centralized user and session state management
- **Clean API Integration**: Modular API service layer

### Architecture

```
frontend/
├── src/
│   ├── contexts/
│   │   └── useSession.tsx          # Session context and provider
│   ├── services/
│   │   └── api.ts                  # API service layer
│   ├── components/
│   │   └── Essays/
│   │       └── SendEssay.tsx       # Essay submission component
│   └── app/
│       ├── layout.tsx              # Root layout with SessionProvider
│       └── page.tsx                # Home page
```

## Session System Usage

### 1. Setup (Already configured)

The `SessionProvider` is already configured in `layout.tsx` to wrap the entire application:

```tsx
<SessionProvider>{children}</SessionProvider>
```

### 2. Using Sessions in Components

```tsx
import { useSession } from "@/contexts/useSession";

export default function MyComponent() {
  const { sessionState, createSession, clearSession, updateSession } =
    useSession();

  // Access session data
  const { userId, sessionId, isSessionActive } = sessionState;

  // Create a new session
  const handleCreateSession = async () => {
    const newSessionId = await createSession("essay_evaluator_agent");
    console.log("New session created:", newSessionId);
  };

  // Clear current session
  const handleClearSession = () => {
    clearSession();
  };

  // Update session data
  const handleUpdateSession = () => {
    updateSession({ userId: "new-user-id" });
  };

  return (
    <div>
      <p>Current User: {userId}</p>
      <p>Session ID: {sessionId || "No session"}</p>
      <p>Active: {isSessionActive ? "Yes" : "No"}</p>
    </div>
  );
}
```

### 3. API Service Usage

```tsx
import { ApiService } from "@/services/api";

// Create and send an essay for evaluation
const payload = ApiService.createEssayPayload(userId, sessionId, essayText);
const result = await ApiService.runAgent(payload);

// Create and send an image for processing
const imagePayload = ApiService.createImagePayload(userId, sessionId, imageUrl);
const imageResult = await ApiService.runAgent(imagePayload);
```

## Key Features

### Automatic Session Persistence

- Sessions are automatically saved to localStorage
- Sessions persist across browser refreshes
- Invalid sessions are automatically cleaned up

### Error Handling

- Comprehensive error handling for API calls
- User-friendly error messages
- Automatic session recovery

### Type Safety

- Full TypeScript support
- Type-safe API payloads
- Strongly typed session state

### Clean Architecture

- Separation of concerns
- Modular service layer
- Reusable components

## Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## Environment Variables

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Session Configuration

The session system can be configured in `src/contexts/useSession.tsx`:

```tsx
const defaultSessionState: SessionState = {
  userId: "your-default-user-id", // Configure default user
  sessionId: null,
  isSessionActive: false,
};

const SESSION_STORAGE_KEY = "your-app-session"; // Configure storage key
const BASE_API_URL = "your-api-url"; // Configure API URL
```

## Components

### SendEssay Component

- Handles essay submission
- Automatic session creation
- File upload support
- Loading states and error handling
- Session status display

## Best Practices

1. **Always use the useSession hook** for session-related operations
2. **Handle errors gracefully** with try-catch blocks
3. **Show loading states** for better UX
4. **Validate inputs** before API calls
5. **Use the ApiService** for all API interactions

## Contributing

1. Follow the established patterns
2. Add proper TypeScript types
3. Include error handling
4. Update documentation for new features
