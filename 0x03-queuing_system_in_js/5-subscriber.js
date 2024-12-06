// Import the ioredis library
import { createClient } from 'redis';

// Create a new Redis client
const redisClient = createClient();

// Connect to the Redis server
redisClient
  .on('connect', () => {
    console.log('Redis client connected to the server');
    // Subscribe to the channel ALXchannel
    redisClient.subscribe('ALXchannel');
  })
  .on('error', (error) => {
    console.log(`Redis client not connected to the server: ${error.message}`);
  });

// When a message is received on the subscribed channel
redisClient.on('message', (channel, message) => {
  console.log(`${message}`);
  
  // If the message is KILL_SERVER, unsubscribe and quit
  if (message === 'KILL_SERVER') {
    redisClient.unsubscribe('ALXchannel', () => {
      redisClient.quit();
    });
  }
});
