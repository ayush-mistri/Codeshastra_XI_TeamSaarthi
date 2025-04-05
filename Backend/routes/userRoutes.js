import express from 'express';
import { getUser } from '../controllers/userController.js';
import { verifyToken } from '../Controllers/verifyToken.js';
import mongoose from 'mongoose';

const router = express.Router();

// Protected route to get user data
router.get('/user', verifyToken, getUser);

router.get('/Anamoly', async (req, res) => {
    try {
      const collection = mongoose.connection.collection('Anamoly'); // Your MongoDB collection name
      const data = await collection.find({}).toArray();
      res.json({ anomalies: data });
    } catch (err) {
      console.error("Error fetching anomalies:", err);
      res.status(500).json({ error: "Server error" });
    }
  });
  

export default router;
