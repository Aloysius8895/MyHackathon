import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { LoginService } from '../login/login-service';

@Injectable({
  providedIn: 'root',
})
export class HomeService {
  apiUrl = environment.backend_url + ':query';
  constructor(private http: HttpClient, private loginService: LoginService) {}

  createSession(userId: string): Observable<any> {
    const body = {
      class_method: 'create_session',
      input: { user_id: userId },
    };
    return this.http.post(this.apiUrl, body);
  }

  async streamQuery(
    userId: string,
    sessionId: string,
    message: string,
    onMessage: (chunk: { owner: string; message: string } | null) => void,
    onComplete: () => void
  ) {
    const url = environment.backend_url + ':streamQuery?alt=sse';
    const body = {
      class_method: 'stream_query',
      input: {
        user_id: userId,
        session_id: sessionId,
        message: message,
      },
    };

    const token = this.loginService.getAccessToken();
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
        Accept: 'text/event-stream',
      },
      body: JSON.stringify(body),
    });

    const reader = response.body?.getReader();
    const decoder = new TextDecoder('utf-8');
    let buffer = '';

    while (true) {
      const { done, value } = await reader!.read();
      if (done) {
        onComplete();
        break;
      }

      buffer += decoder.decode(value, { stream: true });

      while (true) {
        const result = this.extractNextJsonObject(buffer);
        // console.log('INSIDE STREAMQUERY RESULT=>', result);

        if (!result) {
          break;
        }

        const { jsonObject, remainingBuffer } = result;

        try {
          const parsed = JSON.parse(jsonObject);
          const display = this.transformSSEEvent(parsed);
          // console.log('INSIDE STREAMQUERY DISPLAY=>', display);
          if (display) {
            onMessage(display);
          }
        } catch (e) {
          console.warn('Failed to parse JSON from chunk:', jsonObject);
        }

        buffer = remainingBuffer;
      }
    }
  }

  private extractNextJsonObject(
    buffer: string
  ): { jsonObject: string; remainingBuffer: string } | null {
    const startIndex = buffer.indexOf('{');
    if (startIndex === -1) {
      return null;
    }

    let braceCount = 0;
    for (let i = startIndex; i < buffer.length; i++) {
      if (buffer[i] === '{') {
        braceCount++;
      } else if (buffer[i] === '}') {
        braceCount--;
      }

      if (braceCount === 0) {
        const jsonObject = buffer.substring(startIndex, i + 1);
        const remainingBuffer = buffer.substring(i + 1);
        return { jsonObject, remainingBuffer };
      }
    }

    return null;
  }

  transformSSEEvent(event: any): { owner: string; message: string } | null {
    const { content, actions, author } = event;

    if (content?.parts?.[0]?.function_call?.name === 'transfer_to_agent') {
      const agentName = content.parts[0].function_call.args.agent_name;
      return {
        owner: 'system_instruction',
        message: `${author} is transferring to ${agentName}`,
      };
    }

    if (
      content?.parts?.[0]?.function_response?.name === 'transfer_to_agent' &&
      actions?.transfer_to_agent
    ) {
      const agentName = actions.transfer_to_agent;
      return {
        owner: 'system_instruction',
        message: `${author} has transferred to ${agentName}`,
      };
    }

    if (content?.parts?.[0]?.text) {
      return {
        owner: 'bot',
        message: content.parts[0].text,
      };
    }

    return null;
  }
}
