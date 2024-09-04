// Add JavaScript functionality here
document.addEventListener("DOMContentLoaded", function() {
    const profileButton = document.querySelector(".profile-button");
    const dropdownContent = document.querySelector(".dropdown-content");

    profileButton.addEventListener("click", function() {
        dropdownContent.classList.toggle("show");
    });
});

function requestFromHospital() {
    // Add functionality for requesting blood from hospital
    console.log("Request from Hospital");
}

function bloodCommunity() {
    // Add functionality for accessing Blood Community
    console.log("Blood Community");
}


// Function to increase units
function increaseUnits(button) {
    var unitCount = button.parentElement.querySelector('.unit-count');
    unitCount.textContent = parseInt(unitCount.textContent) + 1;
}

// Function to decrease units
function decreaseUnits(button) {
    var unitCount = button.parentElement.querySelector('.unit-count');
    var count = parseInt(unitCount.textContent);
    if (count > 0) {
        unitCount.textContent = count - 1;
    }
}

// Dummy function to simulate blood request
function requestBlood(hospitalName) {
    var units = document.querySelector(`.hospital:has(h3:contains("${hospitalName}")) .unit-count`).textContent;
    alert(`Request blood from ${hospitalName} for ${units} units.`);
}

// Add event listeners to all increase buttons
document.querySelectorAll('.increase').forEach(button => {
    button.addEventListener('click', function() {
        increaseUnits(this);
    });
});

// Add event listeners to all decrease buttons
document.querySelectorAll('.decrease').forEach(button => {
    button.addEventListener('click', function() {
        decreaseUnits(this);
    });
});
