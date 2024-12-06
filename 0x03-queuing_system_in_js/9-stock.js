import express from 'express';
import { promisify } from 'util';
import { createClient } from 'redis';

// Sample product list
const products = [
  { itemId: 1, itemName: 'Suitcase 250', price: 50, initialStock: 4 },
  { itemId: 2, itemName: 'Suitcase 450', price: 100, initialStock: 10 },
  { itemId: 3, itemName: 'Suitcase 650', price: 350, initialStock: 2 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialStock: 5 },
];

// Initialize Express app and Redis client
const app = express();
const redisClient = createClient();
const PORT = 1245;

/**
 * Retrieves a product by its ID.
 * @param {number} id - The ID of the product.
 * @returns {Object|null} The found product or null if not found.
 */
const getProductById = (id) => {
  return products.find(product => product.itemId === id) || null;
};

/**
 * Reserves a specified number of stock for a given product ID in Redis.
 * @param {number} productId - The ID of the product.
 * @param {number} quantity - The quantity to reserve.
 */
const reserveStockById = async (productId, quantity) => {
  const setAsync = promisify(redisClient.SET).bind(redisClient);
  return setAsync(`item.${productId}`, quantity);
};

/**
 * Retrieves the current reserved stock for a given product ID from Redis.
 * @param {number} productId - The ID of the product.
 * @returns {Promise<number>} The current reserved quantity.
 */
const getReservedStockById = async (productId) => {
  const getAsync = promisify(redisClient.GET).bind(redisClient);
  const result = await getAsync(`item.${productId}`);
  return Number.parseInt(result || 0);
};

/**
 * API endpoint to get the list of all products.
 */
app.get('/list_products', (_, res) => {
  res.json(products);
});

/**
 * API endpoint to get product details by ID.
 */
app.get('/list_products/:itemId(\\d+)', async (req, res) => {
  const itemId = Number.parseInt(req.params.itemId, 10);
  const product = getProductById(itemId);

  if (!product) {
    return res.status(404).json({ status: 'Product not found' });
  }

  const reservedStock = await getReservedStockById(itemId);
  product.currentStock = product.initialStock - reservedStock;
  res.json(product);
});

/**
 * API endpoint to reserve a product by ID.
 */
app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = Number.parseInt(req.params.itemId, 10);
  const product = getProductById(itemId);

  if (!product) {
    return res.status(404).json({ status: 'Product not found' });
  }

  const reservedStock = await getReservedStockById(itemId);

  if (reservedStock >= product.initialStock) {
    return res.status(400).json({ status: 'Not enough stock available', itemId });
  }

  await reserveStockById(itemId, reservedStock + 1);
  res.json({ status: 'Reservation confirmed', itemId });
});

/**
 * Resets the stock of all products in Redis to zero.
 */
const resetProductStocks = async () => {
  const setAsync = promisify(redisClient.SET).bind(redisClient);
  await Promise.all(products.map(product => setAsync(`item.${product.itemId}`, 0)));
};

// Start the server
app.listen(PORT, async () => {
  await resetProductStocks();
  console.log(`API available on localhost:${PORT}`);
});

export default app;
