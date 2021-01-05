import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Submissions } from './interfaces/submission';
import { Observable } from 'rxjs';
import { CorrelationsContainer } from './interfaces/correlations';

@Injectable({
  providedIn: 'root',
})
export class HttpService {
  private submissionsPath = 'assets/submissions.json';
  private correlationsPath = 'assets/correlations.json';

  constructor(private http: HttpClient) {}

  public getSubmissions(): Observable<Submissions> {
    return this.http.get<Submissions>(this.submissionsPath);
  }

  public getCorrelations(): Observable<CorrelationsContainer> {
    return this.http.get<CorrelationsContainer>(this.correlationsPath);
  }
}
