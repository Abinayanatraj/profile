import mongoose from "mongoose";

const activitySchema = new mongoose.Schema({
  title: String,
  description: String,
  estimatedCostUSD: Number,
  timeOfDay: String
});

const tripSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User",
      required: true
    },

    destination: String,

    durationDays: Number,

    budgetTier: {
      type: String,
      enum: ["Low", "Medium", "High"]
    },

    interests: [String],

    itinerary: [
      {
        dayNumber: Number,
        activities: [activitySchema]
      }
    ],

    hotels: [
      {
        name: String,
        rating: String,
        tier: String,
        estimatedCostNightUSD: Number
      }
    ],

    estimatedBudget: {
      flights: Number,
      accommodation: Number,
      food: Number,
      activities: Number,
      transport: Number,
      total: Number
    },

    packingList: [
      {
        item: String,
        category: String,
        isPacked: {
          type: Boolean,
          default: false
        }
      }
    ]
  },
  {
    timestamps: true
  }
);

export default mongoose.model("Trip", tripSchema);