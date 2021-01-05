import { Component } from '@angular/core';
import { HttpService } from './http.service';
import { Observable, of } from 'rxjs';
import { Submission, Submissions } from './interfaces/submission';
import { Correlations, CorrelationsContainer } from './interfaces/correlations';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  isSubmissionsLoading = true;
  isCurrentSubmissionLoading = true;
  isCorrelationsLoading = true;
  currentVote = 0;

  entryIdsWithCorrelations: string[] = [];

  title = 'Cool Mini Or Not Homework';
  votes = new Array(10);
  submissions: Submissions | undefined;
  correlations: CorrelationsContainer | undefined;
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
    this.httpService.getSubmissions().subscribe((data) => {
      this.submissions = data;
      this.isSubmissionsLoading = false;
      this.selectRandomSubmission();
    });

    this.httpService.getCorrelations().subscribe((data) => {
      this.correlations = data;
      this.isCorrelationsLoading = false;
      this.entryIdsWithCorrelations = Object.keys(this.correlations).filter(
        (key) => {
          if (this.correlations && this.correlations[key]) {
            var keys = Object.keys(this.correlations[key]);
            if (keys && keys.length > 0) return true;
          }
          return false;
        }
      );
    });
  }

  voteOnCurrent(vote: number) {
    this.currentVote = vote;
    localStorage.setItem(this.current['entry_id'], this.currentVote.toString());
    console.log(`Voted: ${vote}`);
  }

  selectNextSubmission(): void {
    var calculated_votes: Correlations = {};
    var calculated_vote_counts: Correlations = {};
    if (this.correlations) {
      for (var i = 0; i < localStorage.length; i++) {
        var key = localStorage.key(i);
        console.log(`CURRENT KEY: ${key}`);
        if (key) {
          let vote = +(localStorage.getItem(key) || 0);
          console.log(`CURRENT VOTE: ${vote}`);
          let correlations = this.correlations[key];
          console.log(`CORRESPONDING CORRELATIONS: ${correlations}`);
          if (correlations) {
            for (var j = 0; j < Object.keys(correlations).length; j++) {
              var correlation_key = Object.keys(correlations)[j];
              console.log(`CURRENT CORRELATION: ${correlation_key}`);
              var vote_added = vote * correlations[correlation_key];
              console.log(`VOTE ADDED: ${vote_added}`);
              calculated_votes[correlation_key] =
                (calculated_votes[correlation_key] || 0) + vote_added;
              calculated_vote_counts[correlation_key] =
                (calculated_vote_counts[correlation_key] || 0) + 1;
              console.log(`CALCULATED VOTES: ${calculated_votes.toString()}`);
            }
          }
        }
      }
    }
    var keys = Object.keys(calculated_votes);
    for (var i = 0; i < keys.length; i++) {
      calculated_votes[keys[i]] =
        calculated_votes[keys[i]] / calculated_vote_counts[keys[i]];
      console.log(
        `Becsült szavazat: ${keys[i]} -> ${calculated_votes[keys[i]]}`
      );
    }

    var non_voted_correlating_keys = keys
      .filter((key) => localStorage[key] == undefined)
      .sort((a: string, b: string): number => {
        var va = calculated_votes[a];
        var vb = calculated_votes[b];
        if (va > vb) return -1;
        if (va < vb) return 1;
        return 0;
      });
    console.log(`Választhatók: ${non_voted_correlating_keys}`);

    var selected = non_voted_correlating_keys[0];
    console.log(`Választott: ${selected}`);

    if (selected) {
      this.selectSubmission(selected);
    } else {
      this.selectRandomSubmission();
    }
  }

  selectRandomSubmission(): void {
    if (this.entryIdsWithCorrelations) {
      var random = this.entryIdsWithCorrelations[
        (this.entryIdsWithCorrelations.length * Math.random()) << 0
      ];
      this.selectSubmission(random);
    }
  }

  selectSubmission(entry_id: string): void {
    if (this.submissions) {
      this.isCurrentSubmissionLoading = true;
      this.current.entry_image = '';
      this.currentVote = 0;
      this.current = this.submissions[entry_id];
      var savedVote = localStorage.getItem(this.current['entry_id']);
      if (savedVote != null) this.currentVote = +savedVote;
      this.isCurrentSubmissionLoading = false;
    }
  }

  resetVotes(): void {
    localStorage.clear();
    this.currentVote = 0;
  }
}
