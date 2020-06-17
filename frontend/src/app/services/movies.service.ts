import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { AuthService } from './auth.service';
import { environment } from 'src/environments/environment';

export interface Movie {
  id: number;
  title: string;
  release_date: string;
}

@Injectable({
  providedIn: 'root'
})
export class MoviesService {
  url = environment.apiServerUrl;
  public items: {[key: number]: Movie} = {};

  constructor(private auth: AuthService, private http: HttpClient) { }

  getHeaders() {
    const header = {
      headers: new HttpHeaders()
        .set('Authorization',  `Bearer ${this.auth.activeJWT()}`)
    };
    return header;
  }

  getMovies() {
    if (this.auth.can('get: movies')) {
      this.http.get(this.url + '/movies', this.getHeaders())
      .subscribe((res: any) => {
        this.moviesToItems(res.movies);
        console.log(res);
      });
    }
  }

  moviesToItems( movies: Array<Movie>) {
    for (const movie of movies) {
      this.items[movie.id] = movie;
    }
  }
}
