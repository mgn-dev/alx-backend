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

// Function to create a hash in Redis
function createHash() {
  const key = 'ALX';
  const hashValues = {
    Portland: 50,
    Seattle: 80,
    'New York': 20,
    Bogota: 20,
    Cali: 40,
    Paris: 2
  };

  // Delete the existing key if it exists
  redisClient.del(key, (error, response) => {
    if (error) {
      console.log(`Error deleting key ${key}: ${error.message}`);
    } else {

      // Using hset to store the hash values in Redis
      for (const [field, value] of Object.entries(hashValues)) {
        redisClient.hset(key, field, value, (error, result) => {
          if (error) {
            console.log(`Error setting ${field}: ${error.message}`);
          } else {
            console.log(`Reply: ${result}`);
          }
        });
      }
    }
  });
}

// Function to display the hash from Redis
function displayHash() {
  const key = 'ALX';

  redisClient.hgetall(key, (error, result) => {
    if (error) {
      console.log(`Error retrieving hash: ${error.message}`);
    } else {
      console.log(result);
    }
  });
}

// Create the hash and display it
createHash();
setTimeout(displayHash, 100); // Add a timeout to ensure hash is created before displaying

// Always remember to close the Redis client when you're done
process.on('exit', () => {
  redisClient.quit();
});
