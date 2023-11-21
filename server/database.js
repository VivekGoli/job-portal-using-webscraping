const mysql = require('mysql2');
const dotenv = require('dotenv');
let instance = null;
dotenv.config();

const connection = mysql.createConnection({
    host: process.env.HOST,
    user: process.env.USER,
    password: process.env.PASSWORD,
    database: process.env.DATABASE,
    //port: process.env.DB_PORT
});

connection.connect((err) => {
    if (err) {
        console.log(err.message);
    }
    // console.log('db ' + connection.state);
});

class Database {
    static getDbServiceInstance() {
        return instance ? instance : new Database();
    }

    async getCompanyJobData(company) {
        try {
            const response = await new Promise((resolve, reject) => {
                const query = "SELECT id, title, location FROM jobstable WHERE company = ?;";

                connection.query(query, [company], (err, results) => {
                    if (err) reject(new Error(err.message));
                    resolve(results);
                })
            });
            return response;
        } catch (error) {
            console.log(error);
        }
    }
 
    async getJobRoleData(regex) {
        try {
            const response = await new Promise((resolve, reject) => {
                const query = "SELECT id, title, company FROM jobstable WHERE title LIKE ?;";

                connection.query(query, [regex], (err, results) => {
                    if (err) reject(new Error(err.message));
                    resolve(results);
                })
            });
            return response;
        } catch (error) {
            console.log(error);
        }
    }

    async getDataFromId(jobId) {
        try {
            const response = await new Promise((resolve, reject) => {
                const query = "SELECT title, company, location, description, link FROM jobstable WHERE id = ?;";
                connection.query(query, [jobId], (err, results) => {
                    if (err) reject(new Error(err.message));
                    resolve(results);
                })
            });
            return response;
        } catch (error) {
            console.log(error);
        }
    }
}

module.exports = Database;