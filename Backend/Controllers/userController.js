import User from '../models/User.js';

export const getUser = async (req, res) => {
  try {
    // req.user is set in verifyToken middleware (it has the user's id)
    const user = await User.findById(req.user.id).select('-password');

    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }

    res.status(200).json({ user });
  } catch (error) {
    console.error("Error fetching user:", error);
    res.status(500).json({ message: 'Server error' });
  }
};
