// 🔥 Auto detect base URL (localhost / IP / production safe)
const API_BASE = `${window.location.origin}/api`;

/* ================================
   LOAD ATTENDANCE SUMMARY
================================ */
function loadAttendance() {
    const search = document.getElementById("search")?.value || "";

    fetch(`${API_BASE}/attendance/?search=${encodeURIComponent(search)}`)
        .then(res => {
            if (!res.ok) {
                throw new Error("Failed to load attendance");
            }
            return res.json();
        })
        .then(data => {
            // ✅ Pagination safe
            const rows = data.results || data;

            const tbody = document.getElementById("attendance-body");
            if (!tbody) return;

            tbody.innerHTML = "";

            if (rows.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="9" class="text-center text-muted">
                            No attendance data found
                        </td>
                    </tr>
                `;
                return;
            }

            rows.forEach(row => {
                tbody.innerHTML += `
                    <tr>
                        <td>${row.rank ?? "-"}</td>
                        <td>${row.student_name}</td>
                        <td>${row.roll}</td>
                        <td>${row.Class_name}</td>
                        <td>${row.Section}</td>
                        <td class="text-success fw-bold">${row.present_days}</td>
                        <td class="text-danger fw-bold">${row.absent_days}</td>
                        <td class="text-warning fw-bold">${row.late_days}</td>
                        <td class="fw-bold">${row.total_present_days}</td>
                    </tr>
                `;
            });
        })
        .catch(err => {
            console.error("Attendance Load Error:", err);
            alert("Attendance load failed. Check console.");
        });
}

/* ================================
   SAVE ATTENDANCE (CREATE)
================================ */
function saveAttendance() {
    const student = document.getElementById("student_id").value;
    const date = document.getElementById("date").value;
    const status = document.getElementById("status").value;
    const remarks = document.getElementById("remarks").value;

    // 🔐 Basic validation
    if (!student || !date || !status) {
        alert("Student, Date and Status are required");
        return;
    }

    const payload = {
        student: Number(student), // ✅ MUST be number
        date: date,
        status: status,
        remarks: remarks
    };

    fetch(`${API_BASE}/attendance-create/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })
        .then(res => {
            if (!res.ok) {
                return res.json().then(err => {
                    throw err;
                });
            }
            return res.json();
        })
        .then(() => {
            // ✅ Close modal
            const modal = document.getElementById("attendanceModal");
            if (modal) {
                const bsModal = bootstrap.Modal.getInstance(modal);
                bsModal?.hide();
            }

            // ✅ Reset form
            document.getElementById("student_id").value = "";
            document.getElementById("date").value = "";
            document.getElementById("remarks").value = "";

            // ✅ Reload table
            loadAttendance();

            alert("✅ Attendance Saved Successfully");
        })
        .catch(err => {
            console.error("Attendance Save Error:", err);
            alert("❌ Attendance save failed. Check console.");
        });
}

/* ================================
   AUTO LOAD ON PAGE LOAD
================================ */
document.addEventListener("DOMContentLoaded", () => {
    loadAttendance();
});
