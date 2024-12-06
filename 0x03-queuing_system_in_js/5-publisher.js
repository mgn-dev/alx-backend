// Import the ioredis library
import { createClient } from 'redis';

// Create a new Redis client
const redisClient = createClient();

// Connect to the Redis server
redisClient
  .on('connect', () => {
    console.log('Redis client connected to the server');
  })
  .on('error', (error) => {
    console.log(`Redis client not connected to the server: ${error.message}`);
  });

// Function to publish a message
function publishMessage(message, time) {
  setTimeout(() => {
    console.log(`About to send ${message}`);
    redisClient.publish('ALXchannel', message);
  }, time);
}

// Call the publishMessage function with various messages and delays
publishMessage("ALX Student #1 starts course", 100);
publishMessage("ALX Student #2 starts course", 200);
publishMessage("KILL_SERVER", 300);
publishMessage("ALX Student #3 starts course", 400);
