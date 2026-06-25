// controllers/authController.js

const User = require("../models/User");
const bcrypt = require("bcryptjs");

exports.register = async (req, res) => {

    const { name, email, password } = req.body;

    const userExists = await User.findOne({ email });

    if (userExists) {
        return res.status(400).json({
            success: false,
            message: "Email already exists"
        });
    }

    const hashedPassword = await bcrypt.hash(password, 10);

    const user = await User.create({
        name,
        email,
        password: hashedPassword,
        role: "member"
    });

    res.status(201).json({
        success: true,
        user
    });
};