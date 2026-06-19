import User from "./User";
import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";

export const register = async (req: any, res: any) => {
  const { email, password } = req.body;

  const exists = await User.findOne({ email });

  if (exists) {
    return res.status(400).json({
      message: "User already exists"
    });
  }

  const hashed = await bcrypt.hash(password, 10);

  const user = await User.create({
    email,
    password: hashed
  });

  const token = jwt.sign(
    { id: user._id },
    process.env.JWT_SECRET!,
    {
      expiresIn: "7d"
    }
  );

  res.json({ token });
};

export const login = async (req: any, res: any) => {
  const { email, password } = req.body;

  const user = await User.findOne({ email });

  if (!user) {
    return res.status(404).json({
      message: "User not found"
    });
  }

  const valid = await bcrypt.compare(
    password,
    user.password
  );

  if (!valid) {
    return res.status(401).json({
      message: "Invalid credentials"
    });
  }

  const token = jwt.sign(
    { id: user._id },
    process.env.JWT_SECRET!,
    {
      expiresIn: "7d"
    }
  );

  res.json({ token });
};