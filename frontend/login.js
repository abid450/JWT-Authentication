async function loginUser() {
    const msg = document.getElementById("msg");
    msg.innerHTML = "";

    const device = navigator.userAgent;

    const data = {
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
        device: device
    };

    try {
        let res = await fetch("http://192.168.0.100:8000/login", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
        });

        let result = await res.json();

        if (res.ok) {

            localStorage.setItem("access", result.access);

        

            setTimeout(() => {
                window.location.href = "login.html";
            }, 1000);

        } else {
            msg.innerHTML = `<span class="error">${result.error || "Invalid credentials!"}</span>`;
        }

    } catch (err) {
        msg.innerHTML = `<span class="error">${err.message}</span>`;
    }
}
