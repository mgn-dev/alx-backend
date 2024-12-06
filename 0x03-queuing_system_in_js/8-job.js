const kue = require('kue');

function createPushNotificationsJobs(jobs, queue) {
    // Check if jobs is an array
    if (!Array.isArray(jobs)) {
        throw new Error('Jobs is not an array');
    }

    // Process each job in the jobs array
    jobs.forEach((jobData) => {
        // Create a job in the queue
        const job = queue.create('push_notification_code_3', jobData);

        // Log when the job is created
        job.save((err) => {
            if (!err) {
                console.log(`Notification job created: ${job.id}`);
            }
        });

        // Log when the job is complete
        job.on('complete', (result) => {
            console.log(`Notification job ${job.id} completed`);
        });

        // Log when the job has failed
        job.on('failed', (error) => {
            console.log(`Notification job ${job.id} failed: ${error.message}`);
        });

        // Log job progress
        job.on('progress', (progress) => {
            console.log(`Notification job ${job.id} ${progress}% complete`);
        });
    });
}

module.exports = createPushNotificationsJobs;
