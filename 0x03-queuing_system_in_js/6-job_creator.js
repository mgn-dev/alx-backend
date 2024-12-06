// Import the necessary libraries
import kue from 'kue';

// Create a queue named push_notification_code
const queue = kue.createQueue();

// Job data object
const jobData = {
  phoneNumber: '123-456-7890',
  message: 'This is the code to verify your account.'
};

// Create a job with the job data
const job = queue.create('push_notification_code', jobData)
  .save((error) => {
    if (!error) {
      console.log(`Notification job created: ${job.id}`);
    }
  });

// Event listeners for job completion and failure
job.on('complete', () => {
  console.log('Notification job completed');
});

job.on('failed', (errorMessage) => {
  console.log(`Notification job failed: ${errorMessage}`);
});
