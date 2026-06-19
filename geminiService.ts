import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI(
  process.env.GEMINI_API_KEY!
);

export const generateTripPlan = async (
  destination: string,
  durationDays: number,
  budgetTier: string,
  interests: string[]
) => {
  const model = genAI.getGenerativeModel({
    model: "gemini-2.5-flash"
  });

  const prompt = `
Generate valid JSON only.

Destination: ${destination}
Duration: ${durationDays}
Budget: ${budgetTier}
Interests: ${interests.join(",")}

Return:
{
 "itinerary":[],
 "hotels":[],
 "estimatedBudget":{},
 "packingList":[]
}
`;

  const result = await model.generateContent(prompt);

  const text = result.response.text();

  return JSON.parse(text);
};