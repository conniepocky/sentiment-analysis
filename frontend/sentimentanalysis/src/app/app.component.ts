import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  constructor(private http: HttpClient) { }

  configBase = 'http://127.0.0.1:5000/news';

  formData = {
    subject: "",
    region: "",
    source: "",
    min: "",
    max: ""
  };

  data: any;

  onSubmit(){
    var configURL = this.configBase + `?subject=${this.formData.subject}&region=${this.formData.region}&source=${this.formData.source}&minimumDate=${this.formData.min}&maximumDate=${this.formData.max}`;
    
    console.log(configURL);
    this.http.get(configURL).subscribe(data => this.data = data)

    console.log(this.data); 
  }
}
