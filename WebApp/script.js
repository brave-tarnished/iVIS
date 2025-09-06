// Firebase config
const firebaseConfig = {
    apiKey: "AIzaSyDRbU-AP9bY9QX1IGjBv_K-PQ6c9KOPQ_E",
    authDomain: "anpr-bg.firebaseapp.com",
    databaseURL: "https://anpr-bg-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "anpr-bg",
    storageBucket: "anpr-bg.appspot.com",
    messagingSenderId: "1059960578017",
    appId: "1:1059960578017:web:cd2c0158052e4e1388bca0"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const db = firebase.database();

// Add Faculty Vehicle
function addFaculty() {
    const name = document.getElementById("facultyName").value.trim();
    const plate = document.getElementById("facultyPlate").value.trim();

    if (!name || !plate) {
        alert("Please enter both name and number plate!");
        return;
    }

    // Save directly as string
    db.ref("faculty/" + plate).set(name)
    .then(() => {
        console.log("Faculty vehicle added!");
        document.getElementById("facultyName").value = "";
        document.getElementById("facultyPlate").value = "";
    }).catch((error) => {
        console.error("Error adding faculty vehicle:", error);
    });
}

// Display Faculty Vehicles in Table Format
function displayFacultyVehicles() {
    const facultyTable = document.getElementById("facultyTable").getElementsByTagName('tbody')[0];
    facultyTable.innerHTML = ""; // Clear table before updating

    db.ref("faculty").on("value", (snapshot) => {
        facultyTable.innerHTML = ""; 
        snapshot.forEach((childSnapshot) => {
            const name = childSnapshot.val(); // since value is just a string
            let newRow = facultyTable.insertRow();

            let cell1 = newRow.insertCell(0);
            let cell2 = newRow.insertCell(1);
            let cell3 = newRow.insertCell(2); // delete button cell

            cell1.innerText = name;
            cell2.innerText = childSnapshot.key;

            // Create delete button
            let deleteBtn = document.createElement("button");
            deleteBtn.textContent = "Delete";
            deleteBtn.className = "delete-btn"; // optional styling
            deleteBtn.onclick = () => deleteFaculty(childSnapshot.key);

            cell3.appendChild(deleteBtn);
        });
    });
}

// Delete Faculty Vehicle
function deleteFaculty(plate) {
    if (confirm(`Are you sure you want to delete ${plate}?`)) {
        db.ref("faculty/" + plate).remove()
        .then(() => {
            console.log("Deleted successfully");
        })
        .catch((error) => {
            console.error("Error deleting:", error);
        });
    }
}

// Display Outsider Vehicles in Table Format
function displayOutsiderVehicles() {
    const outsidersTable = document.getElementById("outsidersTable").getElementsByTagName('tbody')[0];
    outsidersTable.innerHTML = ""; // Clear table

    db.ref("outsiders").on("value", (snapshot) => {
        outsidersTable.innerHTML = ""; 
        snapshot.forEach((childSnapshot) => {
            const data = childSnapshot.val();
            const row = outsidersTable.insertRow();

            const cell1 = row.insertCell(0);
            const cell2 = row.insertCell(1);
            const cell3 = row.insertCell(2);

            // Support both direct key and nested "plate" key
            const plate = data.plate || childSnapshot.key;
            const entry = data.entry || "Unknown";
            const exit = data.exit || "Not exited yet";

            cell1.innerText = plate;
            cell2.innerText = entry;
            cell3.innerText = exit;
        });
    });
}

// Example function for adding outsider vehicles (call this from a form)
function addOutsiderVehicle(plate, entryTime) {
    if (!plate || !entryTime) return;
    db.ref("outsiders/" + plate).set({
        entry: entryTime,
        exit: null
    });
}

// Attach event listener for faculty button
document.getElementById("addFacultyBtn").addEventListener("click", addFaculty);

// Load tables on page load
displayFacultyVehicles();
displayOutsiderVehicles();
