const chai = require('chai');
const expect = chai.expect;
const kue = require('kue');
const createPushNotificationsJobs = require('./8-job.js');

describe('createPushNotificationsJobs', () => {
    let queue;

    beforeEach(() => {
        // Create a new Kue queue for testing
        queue = kue.createQueue();
        queue.testMode.enter(); // Enter test mode
    });

    afterEach((done) => {
        // Clear the queue and exit test mode
        queue.testMode.exit();
        queue.shutdown(1000, done); // Shut down the queue
    });

    it('should throw an error if jobs is not an array', () => {
        expect(() => createPushNotificationsJobs({}, queue)).to.throw(Error, 'Jobs is not an array');
    });

    it('should create jobs in the queue', () => {
        const jobs = [
            { phoneNumber: '4151234567', message: 'Hello!' },
            { phoneNumber: '4159876543', message: 'World!' }
        ];

        createPushNotificationsJobs(jobs, queue);
        
        const createdJobs = queue.testMode.jobs.push_notification_code_3;

        // Debugging log
        console.log('Created Jobs:', createdJobs);

        // Check that createdJobs exists and is an object
        expect(createdJobs).to.be.an('object').that.is.not.empty; // Expecting the object to exist and not be empty
        const jobIds = Object.keys(createdJobs);
        expect(jobIds.length).to.equal(2); // Expecting two jobs to be in the queue
    });

    it('should create a job with the correct data', () => {
        const jobs = [
            { phoneNumber: '4151234567', message: 'Hello!' }
        ];

        createPushNotificationsJobs(jobs, queue);
        
        const createdJobs = queue.testMode.jobs.push_notification_code_3;

        // Debugging log
        console.log('Created Jobs for Specific Check:', createdJobs);

        // Check that createdJobs exists and is an object
        expect(createdJobs).to.be.an('object').that.is.not.empty; // Expecting the object to exist and not be empty
        const jobId = Object.keys(createdJobs)[0];
        const job = createdJobs[jobId];

        expect(job.data).to.deep.equal(jobs[0]); // Check that the job data matches
    });
});
