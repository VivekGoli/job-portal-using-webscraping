document.addEventListener('DOMContentLoaded', function () {
    // Function to get the value of a query parameter from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const jobId = urlParams.get('id');
  
    if (jobId) {
      console.log('company job.js ' + jobId);
    } else {
      console.error('No job ID provided in the URL.');
    }

    fetch(`http://localhost:5000/client/company_pages/company_job_details_page/job_c.html?id=${jobId}`)
    .then(response => response.json())
    .then(data => loadHTML(data['data']));
});

function loadHTML(data) {
  const title_div = document.querySelector('.job-title');
  const company_div = document.querySelector('.company-name');
  const location_div = document.querySelector('.company-location');
  const jd_div = document.querySelector('.job-description');
  const anchor = document.querySelector('a');

  if (data.length === 0) {
      title_div.innerHTML = "<h2>Hiring is closed for this Job</h2>";
      return;
  }

  let result = data[0];
  title_div.innerHTML = `<h1>${result.title}</h1>`;
  company_div.innerHTML = `<h2>${result.company}</h2>`;
  location_div.innerHTML = `<h4>Location : ${result.location}</h4>`;
  jd_div.innerHTML = `<h4><strong>Job Description</strong></h4><p>${result.description}</p>`;
  anchor.setAttribute("href", `${result.link}`);
  console.log(data);
}