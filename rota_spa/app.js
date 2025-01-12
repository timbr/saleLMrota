// Fetch data from the API
const API_URL = 'https://mfjyxp6iplic6qib.anvil.app/3AH75NTSE22BJQJAGGCLFJEX/_/api/get_records'
async function fetchData() {
  try {
    const response = await fetch(API_URL);
    const data = await response.json();

    // Update the DOM with data
    document.getElementById('meetingDate').textContent = data[0].meetingDate;
    document.getElementById('flowers').value = data[0].flowersPerson;
    document.getElementById('drinks').value = data[0].drinksPerson;
    document.getElementById('door').value = data[0].doorPerson;
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}

// Call fetchData when the page loads
document.addEventListener('DOMContentLoaded', fetchData);
