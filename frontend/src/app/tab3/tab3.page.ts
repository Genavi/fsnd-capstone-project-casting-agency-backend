import { Component } from '@angular/core';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-tab3',
  templateUrl: 'tab3.page.html',
  styleUrls: ['tab3.page.scss']
})
export class Tab3Page {
  loginURL: string;

  constructor(public auth: AuthService) {
    this.loginURL = auth.build_login_link('/tabs/user');
  }
  
}
