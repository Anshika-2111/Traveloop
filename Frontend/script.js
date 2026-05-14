// =========================
// GLOBAL USER
// =========================

const user = JSON.parse(localStorage.getItem("user"));


// =========================
// TOAST NOTIFICATION
// =========================

function showToast(message, type = "success"){

    const toast = document.createElement("div");

    toast.className = `toast ${type}`;

    toast.innerText = message;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 2500);
}


// =========================
// SIGNUP
// =========================

async function signupUser(){

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const message = document.getElementById("message");

    if(!name || !email || !password){

        message.innerText = "Please fill all fields";
        message.style.color = "red";

        showToast("Please fill all fields", "error");

        return;
    }

    if(password.length < 6){

        message.innerText = "Password must be at least 6 characters";
        message.style.color = "red";

        showToast("Password must be at least 6 characters", "error");

        return;
    }

    const response = await fetch("http://127.0.0.1:5000/signup",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body: JSON.stringify({
            name,
            email,
            password
        })
    });

    const data = await response.json();

    message.innerText = data.message;
    message.style.color = response.ok ? "green" : "red";

    showToast(
        data.message,
        response.ok ? "success" : "error"
    );

    if(response.ok){

        localStorage.setItem("user", JSON.stringify(data.user));

        setTimeout(()=>{
            window.location.href = "dashboard.html";
        },1000);

    }else if(data.redirect === "login"){

        setTimeout(()=>{
            window.location.href = "login.html";
        },1200);
    }
}


// =========================
// LOGIN
// =========================

async function loginUser(){

    const email = document.getElementById("loginEmail").value.trim();
    const password = document.getElementById("loginPassword").value.trim();
    const message = document.getElementById("loginMessage");

    if(!email || !password){

        message.innerText = "Please enter email and password";
        message.style.color = "red";

        showToast("Please enter email and password", "error");

        return;
    }

    const response = await fetch("http://127.0.0.1:5000/login",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body: JSON.stringify({
            email,
            password
        })
    });

    const data = await response.json();

    message.innerText = data.message;
    message.style.color = response.ok ? "green" : "red";

    showToast(
        data.message,
        response.ok ? "success" : "error"
    );

    if(response.ok){

        localStorage.setItem("user", JSON.stringify(data.user));

        setTimeout(()=>{
            window.location.href = "dashboard.html";
        },1000);
    }
}


// =========================
// LOGOUT
// =========================

function logoutUser(){

    localStorage.removeItem("user");
    localStorage.removeItem("selectedTripId");

    showToast("Logged out successfully", "success");

    setTimeout(()=>{
        window.location.href = "login.html";
    },700);
}


// =========================
// CREATE TRIP
// =========================

async function createTrip(){

    if(!user){

        showToast("Please login first", "error");

        setTimeout(()=>{
            window.location.href = "login.html";
        },700);

        return;
    }

    const title = document.getElementById("tripTitle").value.trim();
    const description = document.getElementById("tripDescription").value.trim();
    const startDate = document.getElementById("startDate").value;
    const endDate = document.getElementById("endDate").value;
    const budget = document.getElementById("budget").value;
    const message = document.getElementById("tripMessage");

    if(!title || !startDate || !endDate || !budget){

        message.innerText = "Please fill trip title, dates and budget";
        message.style.color = "red";

        showToast("Please fill trip title, dates and budget", "error");

        return;
    }

    if(Number(budget) <= 0){

        message.innerText = "Budget must be greater than 0";
        message.style.color = "red";

        showToast("Budget must be greater than 0", "error");

        return;
    }

    if(new Date(endDate) < new Date(startDate)){

        message.innerText = "End date cannot be before start date";
        message.style.color = "red";

        showToast("End date cannot be before start date", "error");

        return;
    }

    const response = await fetch("http://127.0.0.1:5000/trips",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body: JSON.stringify({
            user_id:user.id,
            title:title,
            description:description,
            start_date:startDate,
            end_date:endDate,
            budget:budget
        })
    });

    const data = await response.json();

    message.innerText = data.message;
    message.style.color = response.ok ? "green" : "red";

    showToast(
        data.message,
        response.ok ? "success" : "error"
    );

    if(response.ok){

        setTimeout(()=>{
            window.location.href = "dashboard.html";
        },1000);
    }
}


// =========================
// INIT
// =========================

window.addEventListener("DOMContentLoaded",()=>{

    // Dashboard and planner have their own page scripts
});