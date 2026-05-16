import { RunPayload } from "@/types";

const BASE_API_URL = "https://edu-ai-adk-659561392335.europe-west1.run.app";
const APP_NAME = "orchestrator_agent";

export class ApiService {
  static async initializeSession(userId: string): Promise<{
    userId: string;
    sessionId: string;
  }> {
    try {
      const res = await fetch(`${BASE_API_URL}/initiate-session/${userId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: userId,
        }),
      });

      if (!res.ok) {
        throw new Error(`API request failed: ${res.statusText}`);
      }

      const data = await res.json();
      return {
        userId: data.user_id,
        sessionId: data.id,
      };
    } catch (error) {
      console.error("Error initializing session:", error);
      throw error;
    }
  }

  static async runAgent(payload: RunPayload): Promise<any> {
    console.log("🔄 Sending payload to API:", payload);
    try {
      const response = await fetch(`${BASE_API_URL}/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.statusText}`);
      }

      const data = await response.json();
      console.log("🔄 Response from API:", data);
      return data;
    } catch (error) {
      console.error("Error running agent:", error);
      throw error;
    }
  }

  static createPayload(
    user_id: string | null,
    session_id: string | null,
    text: string
  ): RunPayload {
    return {
      app_name: APP_NAME,
      user_id: user_id,
      session_id: session_id,
      new_message: {
        role: "user",
        parts: [{ text: text }],
      },
    };
  }

  static async createImagePayload(
    user_id: string | null,
    session_id: string | null,
    file: File
  ): Promise<RunPayload> {
    console.log("file received", file);

    // Use FileReader for safe base64 conversion
    const base64String = await new Promise<string>((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const result = reader.result as string;
        // Remove the data URL prefix (data:image/jpeg;base64,)
        const base64 = result.split(",")[1];
        resolve(base64);
      };
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });

    console.log("base64String created, length:", base64String.length);

    const payload: RunPayload = {
      app_name: APP_NAME,
      user_id: user_id,
      session_id: session_id,
      new_message: {
        role: "user",
        parts: [
          {
            text: "O usuário enviou uma imagem para ser avaliada como redação.",
          },
          {
            inline_data: {
              data: base64String,
              mime_type: file.type,
            },
          } as any,
        ],
      },
    };

    return payload;
  }
}
