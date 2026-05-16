import { Component, OnInit, NgZone } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsComponent } from '../shared/forms/forms';
import { Router } from '@angular/router';
import { HomeService } from './home-service';
import { FormsModule } from '@angular/forms';
import markdownit from 'markdown-it';

interface ChatData {
  owner: string;
  message: string;
}

export interface StreamEvent {
  type: 'chat' | 'form' | 'system_instruction';
  data: any;
}

@Component({
  selector: 'app-home',
  imports: [CommonModule, FormsComponent, FormsModule],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home implements OnInit {
  chatMessages: Array<ChatData> = [];
  showForm = false;
  parsed: any;
  formSchema: any;
  userName = '';
  sessionId = '';
  sessionLoaded = false;
  userMessage = '';
  showChat = false;
  isStreaming = false;

  constructor(
    private router: Router,
    private homeService: HomeService,
    private zone: NgZone
  ) {
    const nav = this.router.getCurrentNavigation();
    this.userName = nav?.extras?.state?.['userName'] || 'testUser';
  }

  ngOnInit(): void {
    this.createSessionId();
  }

  createSessionId() {
    this.isStreaming = true;
    this.homeService.createSession(this.userName).subscribe({
      next: (res) => {
        this.isStreaming = false;
        this.sessionId = res.output?.id;
        this.sessionLoaded = true;
        this.showChat = true;
        this.chatMessages.push({
          owner: 'bot',
          message:
            "**Welcome!** I'm your personal guide to navigating the world of health insurance and finding the right plan for you.",
        });
      },
      error: (err) => {
        console.error('Session creation failed:', err);
      },
    });
  }

  sendMessage(messageToSend: string, displayMessage?: string): void {
    const trimmedMessage = messageToSend.trim();
    if (!trimmedMessage || !this.sessionId) return;

    const userMessageForChat = displayMessage || trimmedMessage;
    this.chatMessages.push({ owner: 'user', message: userMessageForChat });

    this.userMessage = '';
    this.isStreaming = true;
    this.showForm = false;

    this.homeService.streamQuery(
      this.userName,
      this.sessionId,
      trimmedMessage,
      (chunk) => {
        if (chunk) {
          this.zone.run(() => {
            try {
              const parsed = JSON.parse(chunk.message);
              if (parsed && parsed.type === 'form') {
                this.formSchema = parsed.form;
                this.showForm = true;
                this.isStreaming = false;
              } else {
                this.chatMessages.push(chunk);
              }
            } catch (error) {
              this.chatMessages.push(chunk);
            }
          });
        }
      },
      () => {
        this.zone.run(() => {
          this.isStreaming = false;
        });
      }
    );
  }

  sendUserTypedMessage(): void {
    this.sendMessage(this.userMessage);
  }

  onFormSubmit(formData: any): void {
    const formDataString = JSON.stringify(formData);

    this.sendMessage(formDataString, 'Form submitted.');
  }

  formatResponse(text: string) {
    const md = markdownit();
    const result = md.render(text);
    return result;
  }
}
