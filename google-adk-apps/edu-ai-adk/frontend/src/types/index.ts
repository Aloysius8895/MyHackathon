// Session Types
export interface SessionState {
  userId: string;
  sessionId: string | null;
  isSessionActive: boolean;
}

export interface SessionContextType {
  sessionState: SessionState;
  createSession: (appName?: AppType) => Promise<string>;
  clearSession: () => void;
  updateSession: (data: Partial<SessionState>) => void;
}

// API Types
export interface MessagePart {
  text: string;
}

export interface Message {
  role: "user" | "assistant";
  parts: MessagePart[];
}

export interface RunPayload {
  app_name: string;
  user_id: string | null;
  session_id: string | null;
  new_message: Message;
  session_state?: Record<string, any>;
}

// Component Types
export interface EssayFormData {
  text: string;
  file: File | null;
}

export interface ApiResponse {
  success: boolean;
  data?: any;
  error?: string;
}

// App Types
export type AppType =
  | "essay_evaluator_agent"
  | "image_to_essay_agent"
  | "content_generator_agent"
  | "personal_tutor_agent"
  | "progress_tracker_agent"
  | "interdisciplinary_agent"
  | "simulated_exam_agent"
  | "rephraser_agent"
  | "prompt_builder_agent";

export interface AppConfig {
  name: AppType;
  displayName: string;
  description: string;
  supportsFileUpload: boolean;
}
