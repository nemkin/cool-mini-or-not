import { BrowserDynamicTestingModule } from '@angular/platform-browser-dynamic/testing';

export interface Submissions {
  [index: string]: Submission;
}

export interface Submission {
  entry_id: string;
  entry_date: Date;
  entry_name: string;
  entry_image: string;
  user_id: string;
  user_name: string;
  manufacturer: string;
  category: string;
  view_count: number;
  vote_count: number;
  vote_average: number;
}
