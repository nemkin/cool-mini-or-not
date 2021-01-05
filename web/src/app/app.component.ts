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
  isLoading = true;
  title = 'Cool Mini Or Not Homework';
  votes = new Array(10);
  currentVote = 0;
  submissions$: Observable<Submissions>;
  current$: Observable<Submission> = new Observable<Submission>();

  constructor(private readonly httpService: HttpService) {
    this.submissions$ = this.httpService.getSubmissions();
    this.selectRandomSubmission();
  }

  voteOnCurrent(vote: number) {
    this.currentVote = vote;
    console.log(`Voted: ${vote}`);
  }
  selectRandomSubmission(): void {
    this.isLoading = true;
    this.submissions$.subscribe((data) => {
      var keys = Object.keys(data);
      var random = keys[(keys.length * Math.random()) << 0];
      this.current$ = of(data[random]);
      this.isLoading = false;
    });
  }
}
