// Import the necessary libraries
import kue from 'kue';

// Create a queue named push_notification_code
const queue = kue.createQueue();

// Function to send notifications
function sendNotification(phoneNumber, message) {
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
}

// Process jobs in the push_notification_code queue
queue.process('push_notification_code', (job, done) => {
  // Call sendNotification with phone number and message from the job
  sendNotification(job.data.phoneNumber, job.data.message);
  
  // Simulate successful job completion
  done(); // Call done() when the job is complete, or done(new Error('Error message')) in case of error
});

// Optional: Log when queue starts processing
queue.on('job enqueue', (id, type) => {
  console.log(`Job ${id} of type ${type} has been added to the queue`);
});
