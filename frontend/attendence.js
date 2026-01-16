fetch('/api/attendance-create/', {
    method: 'POST',
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
        student: document.getElementById("student_id").value,
        date: document.getElementById("date").value,
        status: document.getElementById("status").value,
        remarks: document.getElementById("remarks").value
    })
})
.then(res => res.json())
.then(() => {
    loadAttendance();
    alert("Attendance Saved Successfully");
});
