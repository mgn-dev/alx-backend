import express from 'express';
import { promisify } from 'util';
import { createQueue } from 'kue';
import { createClient } from 'redis';

// Initialize Express app, Redis client, and job queue
const app = express();
const redisClient = createClient({ name: 'reserve_seat' });
const seatReservationQueue = createQueue();
const DEFAULT_SEATS_COUNT = 50;
let isReservationEnabled = false;
const PORT = 1245;

/**
 * Updates the number of available seats in Redis.
 * @param {number} seatCount - The new count of available seats.
 */
const updateAvailableSeats = async (seatCount) => {
  const setAsync = promisify(redisClient.SET).bind(redisClient);
  return setAsync('available_seats', seatCount);
};

/**
 * Retrieves the current count of available seats from Redis.
 * @returns {Promise<number>} - The number of currently available seats.
 */
const getAvailableSeats = async () => {
  const getAsync = promisify(redisClient.GET).bind(redisClient);
  const result = await getAsync('available_seats');
  return Number.parseInt(result || 0);
};

/**
 * API endpoint to get the current number of available seats.
 */
app.get('/available_seats', async (_, res) => {
  const numberOfAvailableSeats = await getAvailableSeats();
  res.json({ numberOfAvailableSeats });
});

/**
 * API endpoint to reserve a seat.
 */
app.get('/reserve_seat', (_req, res) => {
  if (!isReservationEnabled) {
    return res.json({ status: 'Reservations are blocked' });
  }
  
  try {
    const job = seatReservationQueue.create('reserve_seat');

    job.on('failed', (error) => {
      console.error('Seat reservation job', job.id, 'failed:', error.message || error.toString());
    });
    job.on('complete', () => {
      console.log('Seat reservation job', job.id, 'completed');
    });

    job.save();
    res.json({ status: 'Reservation in process' });
  } catch (error) {
    res.status(500).json({ status: 'Reservation failed', error: error.message });
  }
});

/**
 * API endpoint to process the reservation queue.
 */
app.get('/process', (_req, res) => {
  res.json({ status: 'Queue processing' });

  seatReservationQueue.process('reserve_seat', async (_job, done) => {
    try {
      const availableSeats = await getAvailableSeats();

      // Update reservation status based on available seats
      isReservationEnabled = availableSeats > 1 ? true : false;

      if (availableSeats >= 1) {
        await updateAvailableSeats(availableSeats - 1);
        done(); // Successfully reserved a seat
      } else {
        done(new Error('Not enough seats available'));
      }
    } catch (error) {
      done(error);
    }
  });
});

/**
 * Resets the available seats to a specified initial count.
 * @param {number} initialSeatsCount - The initial count of available seats.
 */
const resetAvailableSeats = async (initialSeatsCount) => {
  await updateAvailableSeats(Number.parseInt(initialSeatsCount));
};

// Start the server and initialize available seats
app.listen(PORT, async () => {
  await resetAvailableSeats(process.env.INITIAL_SEATS_COUNT || DEFAULT_SEATS_COUNT);
  isReservationEnabled = true;
  console.log(`API available on localhost:${PORT}`);
});

export default app;
