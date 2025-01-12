// Add these constants at the top
const BASE_API_URL = 'https://mfjyxp6iplic6qib.anvil.app/3AH75NTSE22BJQJAGGCLFJEX/_/api';
let currentStartDate = null;
let initialLoadTimer = null;

// Update the fetchData function to accept a date parameter
async function fetchData(startDate = null) {
  try {
    // Show loader after 500ms if it's the initial load
    if (!startDate) {
      initialLoadTimer = setTimeout(() => {
        document.getElementById('page-loader').classList.add('visible');
      }, 500);
    }

    const url = startDate 
      ? `${BASE_API_URL}/get_records/${startDate}`
      : `${BASE_API_URL}/get_records`;
      
    const response = await fetch(url);
    const data = await response.json();
    
    // Clear the timer and hide loader
    if (initialLoadTimer) {
      clearTimeout(initialLoadTimer);
      initialLoadTimer = null;
    }
    document.getElementById('page-loader').classList.remove('visible');
    
    // Store the first meeting date as our current position
    if (data.length > 0) {
      currentStartDate = data[0].meetingDate;
    }

    // Fill in missing meetings if less than 4 are returned
    if (data.length < 4) {
      const lastMeeting = data[data.length - 1];
      const [day, month, year] = lastMeeting ? lastMeeting.meetingDate.split('-') : currentStartDate.split('-');
      const lastDate = new Date(year, month - 1, day);

      while (data.length < 4) {
        // Add 7 days to get the next meeting date
        lastDate.setDate(lastDate.getDate() + 7);
        
        // Format the new date
        const newMeetingDate = lastDate.toLocaleDateString('en-GB', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric'
        }).replace(/\//g, '-');

        // Create a blank meeting entry
        const blankMeeting = {
          meetingDate: newMeetingDate,
          flowersPerson: '',
          drinksPerson: '',
          doorPerson: '',
          isBlank: true
        };

        data.push(blankMeeting);
      }
    }
    
    const container = document.getElementById('bookings-container');
    container.innerHTML = '';
    
    data.forEach((booking, index) => {
      const card = document.createElement('div');
      card.className = 'booking-card';
      
      // Format the date
      const date = new Date(booking.meetingDate.split('-').reverse().join('-'));
      const formattedDate = date.toLocaleDateString('en-GB', {
        weekday: 'long',
        day: 'numeric',
        month: 'long',
        year: 'numeric'
      });

      card.innerHTML = `
        <h2>${formattedDate}</h2>
        <div class="entry">
          <label for="flowers-${index}">Flowers:</label>
          <input type="text" id="flowers-${index}" data-date="${booking.meetingDate}" value="${booking.flowersPerson}">
          <span class="loading-icon">↻</span>
          <span class="success-icon">✔</span>
        </div>
        <div class="entry">
          <label for="drinks-${index}">Tea and Coffee:</label>
          <input type="text" id="drinks-${index}" data-date="${booking.meetingDate}" value="${booking.drinksPerson}">
          <span class="loading-icon">↻</span>
          <span class="success-icon">✔</span>
        </div>
        <div class="entry">
          <label for="door-${index}">Door:</label>
          <input type="text" id="door-${index}" data-date="${booking.meetingDate}" value="${booking.doorPerson}">
          <span class="loading-icon">↻</span>
          <span class="success-icon">✔</span>
        </div>
      `;
      
      container.appendChild(card);

      // Add event listeners for saving changes
      const inputs = card.querySelectorAll('input');
      inputs.forEach(input => {
        // Add keypress event listener for Enter key
        input.addEventListener('keypress', (e) => {
          if (e.key === 'Enter') {
            input.blur();
          }
        });

        input.addEventListener('blur', async () => {
          const bookingId = input.id.split('-')[1];
          const meetingDate = input.dataset.date;
          const successIcon = input.nextElementSibling.nextElementSibling;
          const loadingIcon = input.nextElementSibling;
          
          // Show loading icon
          loadingIcon.classList.add('visible');
          
          // Get all inputs, using empty string as fallback if not found
          const flowersInput = card.querySelector(`#flowers-${bookingId}`)?.value || '';
          const drinksInput = card.querySelector(`#drinks-${bookingId}`)?.value || '';
          const doorInput = card.querySelector(`#door-${bookingId}`)?.value || '';

          const payload = {
            meeting_date: meetingDate,  // Use the actual date
            flowers_person: flowersInput,
            drinks_person: drinksInput,
            door_person: doorInput
          };

          console.log('Sending payload:', JSON.stringify(payload)); // Debug line

          try {
            const response = await fetch('https://mfjyxp6iplic6qib.anvil.app/3AH75NTSE22BJQJAGGCLFJEX/_/api/add_record', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
              },
              body: JSON.stringify(payload)
            });
            
            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
            }
            const result = await response.json();
            console.log('Save successful:', result);
            
            // Hide loading icon and show success icon
            loadingIcon.classList.remove('visible');
            successIcon.classList.add('visible');
            setTimeout(() => {
              successIcon.classList.remove('visible');
            }, 2000);
          } catch (error) {
            console.error('Error saving data:', error);
            loadingIcon.classList.remove('visible');
            alert('Failed to save changes');
          }
        });
      });
    });
  } catch (error) {
    console.error('Error fetching data:', error);
    // Make sure to hide loader on error too
    if (initialLoadTimer) {
      clearTimeout(initialLoadTimer);
      initialLoadTimer = null;
    }
    document.getElementById('page-loader').classList.remove('visible');
  }
}

// Add the back button handler
document.addEventListener('DOMContentLoaded', () => {
  // Initial data fetch
  fetchData();
  
  // Add back button click handler
  document.getElementById('back-button').addEventListener('click', () => {
    if (currentStartDate) {
      moveWeek(-7);
    }
  });

  // Add forward button click handler
  document.getElementById('forward-button').addEventListener('click', () => {
    if (currentStartDate) {
      moveWeek(7);
    }
  });

  // Add title click handler to return to initial view
  document.getElementById('title').addEventListener('click', () => {
    fetchData();  // Fetch initial data with no date parameter
  });
});

// Add this helper function for date manipulation
function moveWeek(days) {
  // Parse the current date
  const [day, month, year] = currentStartDate.split('-');
  const date = new Date(year, month - 1, day);
  
  // Add or subtract days
  date.setDate(date.getDate() + days);
  
  // Format the date back to DD-MM-YYYY
  const newStartDate = date.toLocaleDateString('en-GB', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  }).replace(/\//g, '-');
  
  // Fetch data from the new date
  fetchData(newStartDate);
}
