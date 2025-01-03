import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { NavbarComponent } from '../../shared/navbar/navbar.component';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-main-consultdpi',
  imports: [RouterLink,NavbarComponent],
  templateUrl: './main-consultdpi.component.html',
  styleUrl: './main-consultdpi.component.scss'
})
export class MainConsultdpiComponent implements OnInit{
  dpiId: any;

  constructor(private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.dpiId = this.route.snapshot.paramMap.get('id');
    console.log('ID du DPI:', this.dpiId);}
}
