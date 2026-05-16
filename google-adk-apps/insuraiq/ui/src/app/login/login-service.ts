import { Injectable, EventEmitter } from '@angular/core';
import { jwtDecode } from 'jwt-decode';
import * as CryptoJS from 'crypto-js';

@Injectable({
  providedIn: 'root',
})
export class LoginService {
  constructor() {}
  loginNotification = new EventEmitter<boolean>();

  setLoginData(
    userName: string,
    userEmail: string,
    userImage: string,
    credential: string,
    authToken: string
  ) {
    let jsonString = JSON.stringify({
      UserN_ID: this.encryptAES256(userName),
      UserE_ID: this.encryptAES256(userEmail),
      UserI_ID: this.encryptAES256(userImage),
      SECURE_TOKEN: this.encryptAES256(credential),
      SECURE_ACCESS_TOKEN: this.encryptAES256(authToken),
      L_TIME: this.encryptAES256(new Date().getTime().toString()),
    });
    sessionStorage.setItem('__UADID__', this.encryptAES256(jsonString));
    this.loginNotification.emit(true);
  }

  isLoginValid() {
    let loginData = sessionStorage.getItem('__UADID__');
    if (loginData != null) {
      loginData = this.decryptAES256(loginData!.toString());
      let jsonLoginData = JSON.parse(loginData);
      let loginTime: string = this.decryptAES256(jsonLoginData.L_TIME);
      let timeDifference = new Date().getTime() - Number(loginTime);
      timeDifference = timeDifference / (60 * 60 * 1000);
      if (timeDifference < 1) {
        this.loginNotification.emit(true);
        return true;
      }
    }
    this.loginNotification.emit(false);
    return false;
  }

  getLoginData() {
    let loginData = sessionStorage.getItem('__UADID__');
    loginData = this.decryptAES256(loginData!.toString());
    return JSON.parse(loginData);
  }

  getLoginImage() {
    return this.decryptAES256(this.getLoginData().UserI_ID);
  }

  getLoginEmail() {
    return this.decryptAES256(this.getLoginData().UserE_ID);
  }

  getLoginName() {
    return this.decryptAES256(this.getLoginData().UserN_ID);
  }

  getCredentialToken() {
    return this.decryptAES256(this.getLoginData().SECURE_TOKEN);
  }

  getAccessToken() {
    return this.decryptAES256(this.getLoginData().SECURE_ACCESS_TOKEN);
  }

  encryptAES256(data: string): string {
    const secretKey = '1234567890abcdef1234567890abcdef';
    const encrypted = CryptoJS.AES.encrypt(data, secretKey);
    return encrypted.toString();
  }

  decryptAES256(cipherText: string): string {
    const secretKey = '1234567890abcdef1234567890abcdef';
    const bytes = CryptoJS.AES.decrypt(cipherText, secretKey);
    return bytes.toString(CryptoJS.enc.Utf8);
  }

  decodeJwtResponse(token: string): any {
    try {
      return jwtDecode(token);
    } catch (Error) {
      return null;
    }
  }

  signOut() {
    sessionStorage.removeItem('__UADID__');
    window.location.reload();
  }
}
