console.log('จันทร์ไรเดอร์');

// Site header
const siteHeaderToggleMenuButton = document.querySelector('.site-header-toggle-menu-button');
const siteHeaderMenu = document.querySelector('.site-header-menu');
siteHeaderToggleMenuButton.addEventListener('click', () => {
  siteHeaderMenu.classList.toggle('is-active')
});

// Subscription form
const subscriptionForm = document.querySelector('.subscription-form');

function foodSetValidation(event) {
  const checkedFoodSet = document.querySelectorAll('input[name="food_set"]:checked');
  if (checkedFoodSet.length === 0) {
    event.preventDefault();
    alert('กรุณาเลือกเมนูอย่างน้อย 1 เมนู');
  }
}

if (!!subscriptionForm) {
  subscriptionForm.addEventListener('submit', foodSetValidation);
}

document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    events: [
      {% for booking in bookings %}
        {
          title: '{{ booking.room.name }}',
          start: '{{ booking.start_time|date:"Y-m-d" }}',
          end: '{{ booking.end_time|date:"Y-m-d" }}'
        },
      {% endfor %}
    ]
  });
  calendar.render();
});
