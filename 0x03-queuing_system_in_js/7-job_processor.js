const kue = require('kue');
const queue = kue.createQueue();

const blacklistedNumbers = [
    '4153518780',
    '4153518781'
];

function sendNotification(phoneNumber, message, job, done) {
    // Track progress at 0%
    job.progress(0, 100);

    // Check if the phone number is blacklisted
    if (blacklistedNumbers.includes(phoneNumber)) {
        return done(new Error(`Phone number ${phoneNumber} is blacklisted`));
    }

    // Progress to 50%
    job.progress(50, 100);
    console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);

    // Simulate sending the notification (could be an async operation)
    setTimeout(() => {
        // Complete the job successfully
        done(null, { success: true });
    }, 2000); // Simulate some delay
}

// Process jobs in the queue allowing two jobs at a time
queue.process('push_notification_code_2', 2, (job, done) => {
    const { phoneNumber, message } = job.data;
    sendNotification(phoneNumber, message, job, done);
});

// To listen for job completion/failure
queue.on('job complete', (id) => {
    console.log(`Job ${id} completed`);
}).on('job failed', (id, error) => {
    console.log(`Job ${id} failed: ${error.message}`);
});

// Example of adding jobs to the queue
const jobData = [
    { phoneNumber: '4153518780', message: 'Hello!' },
    { phoneNumber: '4153518781', message: 'World!' },
    { phoneNumber: '4151234567', message: 'Welcome!' }, // Non-blacklisted
];

jobData.forEach((data) => {
    const job = queue.create('push_notification_code_2', data);
    job.save((err) => {
        if (!err) {
            console.log(`Notification job created: ${job.id}`);
        }
    });
});
