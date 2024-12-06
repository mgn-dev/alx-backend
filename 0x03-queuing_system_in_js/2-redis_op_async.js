// Import the necessary libraries
import { createClient } from 'redis';
import { promisify } from 'util';

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

// Function to set a new school in Redis
function setNewSchool(schoolName, value) {
  redisClient.set(schoolName, value, (error, result) => {
    if (error) {
      console.log(`Error setting value: ${error.message}`);
    } else {
      console.log(`Reply: ${result}`);
    }
  });
}

// Promisify the redisClient.get method
const getAsync = promisify(redisClient.get).bind(redisClient);

// Function to display the value of a school from Redis using async/await
async function displaySchoolValue(schoolName) {
  try {
    const result = await getAsync(schoolName);
    console.log(`${result}`);
  } catch (error) {
    console.log(`Error getting value: ${error.message}`);
  }
}

// Call the functions
displaySchoolValue('ALX');
setNewSchool('ALXSanFrancisco', '100');
displaySchoolValue('ALXSanFrancisco');

// Always remember to close the Redis client when you're done
process.on('exit', () => {
  redisClient.quit();
});
