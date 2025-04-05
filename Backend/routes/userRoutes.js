import express from 'express';
import { getUser } from '../controllers/userController.js';
import { verifyToken } from '../Controllers/verifyToken.js';

const router = express.Router();

// Protected route to get user data
router.get('/user', verifyToken, getUser);

export default router;
