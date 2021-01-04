import { Component } from '@angular/core';
import { HttpService } from './http.service';
import { Observable } from 'rxjs';
import { Submissions } from './interfaces/submission';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  title = 'Cool Mini Or Not Voter';
  submissions$: Observable<Submissions>;

  constructor(private readonly httpService: HttpService) {
    this.submissions$ = this.httpService.getSubmissions();
  }
}
