import { Component, OnInit, NgZone } from '@angular/core';
import { environment } from '../../environments/environment';
import { Router } from '@angular/router';
import { LoginService } from './login-service';

declare var google: any;
interface CredentialResponse {
  credential?: string;
}

interface TokenResponse {
  access_token: string;
  expires_in: number;
  scope: string;
  token_type: string;
}

@Component({
  selector: 'app-login',
  imports: [],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login implements OnInit {
  clientId = environment.googleClientId;
  private tokenClient: any;
  private credentialResponse: any;

  constructor(
    private loginService: LoginService,
    private router: Router,
    private zone: NgZone
  ) {}

  ngOnInit(): void {
    if (this.loginService.isLoginValid()) {
      this.router.navigate(['home']);
    } else {
      this.loginService.loginNotification.emit(false);
    }
  }

  ngAfterViewInit(): void {
    this.initGoogleAuth();
  }

  initGoogleAuth() {
    console.log('inside googleAuth', google);
    google.accounts.id.initialize({
      client_id: environment.googleClientId,
      callback: this.handleCredResponse.bind(this),
      auto_select: false,
      cancel_on_tap_outside: true,
    });

    google.accounts.id.renderButton(document.getElementById('google-button'), {
      theme: 'filled_blue',
      size: 'large',
      shape: 'pill',
      text: 'signin_with',
      logo_alignment: 'left',
    });
    this.tokenClient = google.accounts.oauth2.initTokenClient({
      client_id: environment.googleClientId,
      scope: 'https://www.googleapis.com/auth/cloud-platform',
      callback: (tokenResponse: TokenResponse) => {
        if (tokenResponse && tokenResponse.access_token) {
          this.proceedLogin(
            this.credentialResponse,
            tokenResponse.access_token
          );
        }
      },
    });
  }

  async handleCredResponse(response: CredentialResponse) {
    console.log('inside googleAuth', response);
    this.credentialResponse = response;
    const resPayload = this.loginService.decodeJwtResponse(
      response.credential!
    );
    console.log('inside handleCredResponse => ', resPayload);
    this.tokenClient.requestAccessToken();
  }

  proceedLogin(idTokenResponse: any, acessToken: string) {
    const resPayload = this.loginService.decodeJwtResponse(
      idTokenResponse.credential
    );
    console.log('loginResPayload', resPayload);
    console.log('accessToken', acessToken);

    this.loginService.setLoginData(
      resPayload.name,
      resPayload.email,
      resPayload.picture,
      idTokenResponse.credential,
      acessToken
    );

    this.zone.run(() => {
      this.router.navigate(['home'], {
        state: {
          userName: resPayload.name,
        },
      });
    });
  }
}
