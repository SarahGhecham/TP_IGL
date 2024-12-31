import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-calendar',
  imports: [CommonModule],
  templateUrl: './calendar.component.html',
  styleUrls: ['./calendar.component.scss']
})
export class CalendarComponent implements OnInit {
  today: number = 0;
  currentMonth: number = 0;
  currentYear: number = 0;
  daysInMonth: number[] = [];
  emptyDays: number[] = [];  // Pour stocker les jours vides avant le début du mois
  monthNames: string[] = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  weekDays: string[] = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];  // Les jours de la semaine

  ngOnInit(): void {
    const currentDate = new Date();
    this.currentMonth = currentDate.getMonth();
    this.currentYear = currentDate.getFullYear();
    this.today = currentDate.getDate();
    this.updateCalendar();
  }

  updateCalendar(): void {
    // Obtenez le nombre de jours dans le mois en cours
    const daysInCurrentMonth = new Date(this.currentYear, this.currentMonth + 1, 0).getDate();
    this.daysInMonth = [];

    // Obtenez le jour de la semaine où commence le mois
    const firstDayOfMonth = new Date(this.currentYear, this.currentMonth, 1).getDay();
    
    // Remplissez le tableau `emptyDays` pour les jours vides avant le début du mois
    this.emptyDays = [];
    for (let i = 0; i < firstDayOfMonth; i++) {
      this.emptyDays.push(i);
    }

    // Remplissez les jours du mois
    for (let day = 1; day <= daysInCurrentMonth; day++) {
      this.daysInMonth.push(day);
    }
  }

  previousMonth(): void {
    if (this.currentMonth === 0) {
      this.currentMonth = 11;
      this.currentYear--;
    } else {
      this.currentMonth--;
    }
    this.updateCalendar();
  }

  nextMonth(): void {
    if (this.currentMonth === 11) {
      this.currentMonth = 0;
      this.currentYear++;
    } else {
      this.currentMonth++;
    }
    this.updateCalendar();
  }
  isToday(day: number): boolean {
    const todayDate = new Date();
    return this.currentYear === todayDate.getFullYear() &&
           this.currentMonth === todayDate.getMonth() &&
           day === this.today;
  }
}
