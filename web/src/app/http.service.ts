import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Submissions } from './interfaces/submission';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class HttpService {
  private submissionsPath = 'assets/submissions.json';

  constructor(private http: HttpClient) {}

  public getSubmissions(): Observable<Submissions> {
    return this.http.get<Submissions>(this.submissionsPath);
  }
}
