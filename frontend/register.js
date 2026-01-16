async function registerUser() {
    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const phone_number = document.getElementById("phone_number").value.trim();
    const password = document.getElementById("password").value.trim();
    const msg = document.getElementById("msg");

    msg.style.color = "red"; 
    msg.innerText = "";

    if (!username || !email || !phone_number || !password) {
        msg.innerText = "All fields are required!";
        return;
    }

    const data = {
        username: username,
        email: email,
        phone_number: phone_number,
        password: password
    };

    try {
        const response = await fetch("http://192.168.0.100:8000/signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            msg.style.color = "green";
            msg.innerText = result.message || "Registration successful! Please verify email.";

            // redirect login
            setTimeout(() => {
                window.location.href = "login.html";
            }, 1500);

        } else {
            msg.innerText = result.email || result.username || result.phone_number || result.password || "Registration failed!";
        }

    } catch (error) {
        msg.innerText = "Server error!";
        console.log(error);
    }
}
