const express = require('express');
const app = express();
const cors = require('cors');
const dotenv = require('dotenv');
dotenv.config();

const dbService = require('./database');

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended : false }));

app.get('/client/role_pages/role_job_details_page/job_r.html', (request, response) => {
    //const { jobId } = request.params;
    const jobId = request.query.id;

    const db = dbService.getDbServiceInstance();
    const result = db.getDataFromId(jobId);
    result
    .then(data => response.json({data : data}))
    .catch(err => console.log(err));
})

app.get('/client/company_pages/company_job_details_page/job_c.html', (request, response) => {
    //const { jobId } = request.params;
    const jobId = request.query.id;

    const db = dbService.getDbServiceInstance();
    const result = db.getDataFromId(jobId);
    result
    .then(data => response.json({data : data}))
    .catch(err => console.log(err));
})

app.get('/client/company_pages/bankofamerica', (request, response) => {
    const db = dbService.getDbServiceInstance();
    const result = db.getCompanyJobData("Bank of America");
    result
    .then(data => response.json({data : data}))
    .catch(err => console.log(err));
})

app.get('/client/company_pages/cisco', (request, response) => {
    const db = dbService.getDbServiceInstance();
    const result = db.getCompanyJobData("Cisco");
    result
    .then(data => response.json({data : data}))
    .catch(err => console.log(err));
})

app.get('/client/company_pages/deloitte', (request, response) => {
    const db = dbService.getDbServiceInstance();
    const result = db.getCompanyJobData("Deloitte");
    result
    .then(data => response.json({data : data}))
    .catch(err => console.log(err));
})

app.get('/client/company_pages/ea', (request, response) => {
    const db = dbService.getDbServiceInstance();
    const result = db.getCompanyJobData("Electronic Arts");
    result
    .then(data => response.json({data : data}))
    .catch(err => console.log(err));
})

app.get('/client/company_pages/ey', (request, response) => {
    const db = dbService.getDbServiceInstance();
    const result = db.getCompanyJobData("Ernest & Young");
    result
    .then(data => response.json({data : data}))
    .catch(err => console.log(err));
})

app.get('/client/company_pages/google', (request, response) => {
    const db = dbService.getDbServiceInstance();
    const result = db.getCompanyJobData("Google");
    result
    .then(data => response.json({data : data}))
    .catch(err => console.log(err));
})

app.get('/client/company_pages/hitachi', (request, response) => {
    const db = dbService.getDbServiceInstance();
    const result = db.getCompanyJobData("Hitachi");
    result
    .then(data => response.json({data : data}))
    .catch(err => console.log(err));
})

app.get('/client/company_pages/hsbc', (request, response) => {
    const db = dbService.getDbServiceInstance();
    const result = db.getCompanyJobData("HSBC");
    result
    .then(data => response.json({data : data}))
    .catch(err => console.log(err));
})

app.get('/client/company_pages/massmutual', (request, response) => {
    const db = dbService.getDbServiceInstance();
    const result = db.getCompanyJobData("Mass Mutual");
    result
    .then(data => response.json({data : data}))
    .catch(err => console.log(err));
})

app.get('/client/company_pages/sap', (request, response) => {
    const db = dbService.getDbServiceInstance();
    const result = db.getCompanyJobData("SAP");
    result
    .then(data => response.json({data : data}))
    .catch(err => console.log(err));
})
 
app.get('/client/role_pages/dataanalyst', (request, response) => {
    const db = dbService.getDbServiceInstance();
    const result = db.getJobRoleData("%Data%Analy%");
    result
    .then(data => response.json({data : data}))
    .catch(err => console.log(err));
})

app.get('/client/role_pages/dataengineer', (request, response) => {
    const db = dbService.getDbServiceInstance();
    const result = db.getJobRoleData("%Data%Engineer%");
    result
    .then(data => response.json({data : data}))
    .catch(err => console.log(err));
})

app.get('/client/role_pages/datascientist', (request, response) => {
    const db = dbService.getDbServiceInstance();
    const result = db.getJobRoleData("%Data%Scientist%");
    result
    .then(data => response.json({data : data}))
    .catch(err => console.log(err));
})

app.get('/client/role_pages/networkengineer', (request, response) => {
    const db = dbService.getDbServiceInstance();
    const result = db.getJobRoleData("%Network%");
    result
    .then(data => response.json({data : data}))
    .catch(err => console.log(err));
})

app.get('/client/role_pages/fullstackdeveloper', (request, response) => {
    const db = dbService.getDbServiceInstance();
    const result = db.getJobRoleData("%Full%Stack%Developer%");
    result
    .then(data => response.json({data : data}))
    .catch(err => console.log(err));
})

app.get('/client/role_pages/hrmanager', (request, response) => {
    const db = dbService.getDbServiceInstance();
    const result = db.getJobRoleData("%Manager%");
    result
    .then(data => response.json({data : data}))
    .catch(err => console.log(err));
})

app.get('/client/role_pages/softwareengineer', (request, response) => {
    const db = dbService.getDbServiceInstance();
    const result = db.getJobRoleData("%Software%Engineer%");
    result
    .then(data => response.json({data : data}))
    .catch(err => console.log(err));
})

app.get('/client/role_pages/softwaretesting', (request, response) => {
    const db = dbService.getDbServiceInstance();
    const result = db.getJobRoleData("%Test%");
    result
    .then(data => response.json({data : data}))
    .catch(err => console.log(err));
})

app.listen(process.env.PORT, () => console.log('app is running'));