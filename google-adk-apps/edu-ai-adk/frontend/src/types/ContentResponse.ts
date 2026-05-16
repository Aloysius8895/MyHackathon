export interface ContentResponse {
  text_explanation: string;
  topics_summary: string[];
  flashcards: Flashcard[];
  video_suggestions: VideoSuggestion[];
}

interface Flashcard {
  question: string;
  answer: string;
}

interface VideoSuggestion {
  title: string;
  link: string;
  description: string;
}
