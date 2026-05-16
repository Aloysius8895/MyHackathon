import express from 'express';
import { GoogleGenAI } from '@google/genai';
import admin from 'firebase-admin';
import dotenv from 'dotenv';
import serviceAccount from './firebase-key.json' with { type: 'json' };

dotenv.config();

const app = express();
app.use(express.json());
app.use(express.static('public')); 

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

if (!admin.apps.length) {
  admin.initializeApp({
    credential: admin.credential.cert(serviceAccount)
  });
}
const db = admin.firestore();

function cosineSimilarity(vecA, vecB) {
  let dotProduct = 0.0, normA = 0.0, normB = 0.0;
  for (let i = 0; i < vecA.length; i++) {
    dotProduct += vecA[i] * vecB[i];
    normA += vecA[i] * vecA[i];
    normB += vecB[i] * vecB[i];
  }
  return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}

// Dynamic Search Endpoint
app.post('/api/search', async (req, res) => {
  try {
    // Read both query and collection choice from the incoming request payload
    const { query, collection } = req.body;
    
    if (!query) return res.status(400).json({ error: "Query cannot be blank." });
    
    // Default to 'startups' if the frontend fails to supply one for safety
    const targetCollection = collection || 'startups';

    // Generate vector embedding for the search query text string
    const response = await ai.models.embedContent({
      model: 'gemini-embedding-001',
      contents: [query],
    });

    const queryVector = response.embeddings?.[0]?.values || response.values;
    
    // DYNAMIC MATCHING POINT: Pass targetCollection variable right here!
    const snapshot = await db.collection(targetCollection).get();
    const results = [];

    snapshot.forEach(doc => {
      const data = doc.data();
      if (data.embedding && Array.isArray(data.embedding)) {
        const score = cosineSimilarity(queryVector, data.embedding);
        results.push({
          name: data.name,
          content: data.content,
          similarity: score
        });
      }
    });

    results.sort((a, b) => b.similarity - a.similarity);
    res.json(results.slice(0, 3)); 

  } catch (error) {
    console.error("❌ Web search endpoint crashed:", error);
    res.status(500).json({ error: error.message });
  }
});

const PORT = 3000;
app.listen(PORT, () => console.log(`🚀 Matchmaker Web UI live at http://localhost:${PORT}`));

// Automated Cross-Match Engine Endpoint
app.post('/api/cross-match', async (req, res) => {
  try {
    // 1. Get all startups and all mentors from the cloud
    const startupSnapshot = await db.collection('startups').get();
    const mentorSnapshot = await db.collection('mentors').get();

    if (startupSnapshot.empty || mentorSnapshot.empty) {
      return res.status(400).json({ error: "Need data in both collections to cross-match!" });
    }

    const totalMatchMap = [];

    // 2. Loop through every single startup
    startupSnapshot.forEach(sDoc => {
      const startupData = sDoc.data();
      const startupMatches = [];

      // 3. Compare it against every single mentor vector
      mentorSnapshot.forEach(mDoc => {
        const mentorData = mDoc.data();
        if (startupData.embedding && mentorData.embedding) {
          const score = cosineSimilarity(startupData.embedding, mentorData.embedding);
          startupMatches.push({
            mentorName: mDoc.id.replace(/-/g, ' '),
            score: score
          });
        }
      });

      // Sort matches for this specific startup group
      startupMatches.sort((a, b) => b.score - a.score);

      totalMatchMap.push({
        startupName: sDoc.id.replace(/-/g, ' '),
        bestMentor: startupMatches[0]?.mentorName || "None",
        matchPercentage: ((startupMatches[0]?.score || 0) * 100).toFixed(2)
      });
    });

    res.json(totalMatchMap);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});