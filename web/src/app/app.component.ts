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
  currentVote = 0;

  title = 'Cool Mini Or Not Homework';
  votes = new Array(10);
  submissions$: Observable<Submissions>;
  current: Submission = {
    entry_id: '',
    entry_date: new Date(),
    entry_name: '',
    entry_image: '',
    user_id: '',
    user_name: '',
    manufacturer: '',
    category: '',
    view_count: 0,
    vote_count: 0,
    vote_average: 0,
  };

  constructor(private readonly httpService: HttpService) {
    this.submissions$ = this.httpService.getSubmissions();
    this.selectRandomSubmission();
  }

  voteOnCurrent(vote: number) {
    this.currentVote = vote;

    localStorage.setItem(
      this.current ? this.current['entry_id'] : 'FAKENEWS',
      this.currentVote.toString()
    );
    console.log(`Voted: ${vote}`);
  }
  selectRandomSubmission(): void {
    this.isLoading = true;
    this.currentVote = 0;
    this.submissions$.subscribe((data) => {
      var keys = Object.keys(data);
      var random = keys[(keys.length * Math.random()) << 0];
      this.current = data[random];
      var savedVote = localStorage.getItem(this.current['entry_id']);
      if (savedVote != null) this.currentVote = +savedVote;
      this.isLoading = false;
    });
  }

  resetVotes(): void {
    localStorage.clear();
    this.currentVote = 0;
  }
}
