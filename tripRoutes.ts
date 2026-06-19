import express from "express";

import {
  createTrip,
  getTrips,
  updateTrip,
  deleteTrip
} from "../controllers/tripController";

import { authMiddleware } from "../middleware/authMiddleware";

const router = express.Router();

router.use(authMiddleware);

router.get("/", getTrips);

router.post("/", createTrip);

router.put("/:id", updateTrip);

router.delete("/:id", deleteTrip);

export default router;