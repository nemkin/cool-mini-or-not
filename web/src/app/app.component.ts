import { Component } from '@angular/core';
import { HttpService } from './http.service';
import { Observable, of } from 'rxjs';
import { Submission, Submissions } from './interfaces/submission';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  title = 'Cool Mini Or Not Voter';
  submissions$: Observable<Submissions>;
  current$: Observable<Submission> = new Observable<Submission>();

  constructor(private readonly httpService: HttpService) {
    this.submissions$ = this.httpService.getSubmissions();
    this.selectRandomSubmission();
  }

  selectRandomSubmission(): void {
    this.submissions$.subscribe((data) => {
      this.current$ = of(data['363638']);
    });
  }
}
