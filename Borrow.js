// models/Borrow.js

const mongoose = require("mongoose");

const borrowSchema = new mongoose.Schema(
{
    member: {
        type: mongoose.Schema.Types.ObjectId,
        ref: "User"
    },

    book: {
        type: mongoose.Schema.Types.ObjectId,
        ref: "Book"
    },

    borrowedAt: {
        type: Date,
        default: Date.now
    },

    returned: {
        type: Boolean,
        default: false
    }
});

module.exports = mongoose.model("Borrow", borrowSchema);