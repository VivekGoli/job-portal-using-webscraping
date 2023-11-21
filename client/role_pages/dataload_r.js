function loadHTMLTable(data) {
    const table = document.querySelector('table tbody');

    if (data.length === 0) {
        table.innerHTML = "<tr><td class='no-data' colspan='3'>No Data</td></tr>";
        return;
    }

    let tableHtml = "";

    data.forEach(function ({id, title, company}) {
        tableHtml += "<tr>";
        tableHtml += `<td>${title}</td>`;
        tableHtml += `<td>${company}</td>`;
        tableHtml += `<td><button class="job-details-btn" data-id=${id}>Details</td>`;
        tableHtml += "</tr>";
    });

    table.innerHTML = tableHtml;

    const buttons = document.querySelectorAll('.job-details-btn');

    // Attach a click event listener to each button
    buttons.forEach(button => {
            button.addEventListener('click', function () {
            // Retrieve the job ID from the data attribute of the parent row
            const jobId = this.getAttribute('data-id');
            console.log(jobId);
            // Redirect to the job details page with the specific job ID
            window.location.href = `http://127.0.0.1:5500/client/role_pages/role_job_details_page/job_r.html?id=${jobId}`;
        });
    });
}