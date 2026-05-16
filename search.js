import { GoogleGenAI } from '@google/genai';
import admin from 'firebase-admin';
import dotenv from 'dotenv';

// Import your service account JSON file securely
import serviceAccount from './firebase-key.json' with { type: 'json' };

dotenv.config();

// 1. Initialize Google Gen AI & Firebase Admin
const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

if (!admin.apps.length) {
  admin.initializeApp({
    credential: admin.credential.cert(serviceAccount)
  });
}
const db = admin.firestore();

/**
 * Calculates the semantic cosine similarity between two vector coordinate arrays
 */
function cosineSimilarity(vecA, vecB) {
  let dotProduct = 0.0;
  let normA = 0.0;
  let normB = 0.0;
  for (let i = 0; i < vecA.length; i++) {
    dotProduct += vecA[i] * vecB[i];
    normA += vecA[i] * vecA[i];
    normB += vecB[i] * vecB[i];
  }
  return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}

// 2. Main Search Function
async function searchVector(queryText, collectionName = 'startups') {
  try {
    console.log(`🔍 Searching across ${collectionName} for: "${queryText}"...`);

    // Fetch the vector coordinates for the user's query
    // Notice the brackets [queryText] to pass it as a list!
    const response = await ai.models.embedContent({
      model: 'gemini-embedding-001',
      contents: [queryText],
    });

    const queryVector = response.embeddings?.[0]?.values || response.values;
    if (!queryVector) {
      throw new Error("Could not generate vector for your search query.");
    }

    // Fetch all stored profile entries from Firestore
    const snapshot = await db.collection(collectionName).get();
    if (snapshot.empty) {
      console.log(`⚠️ No documents found in your '${collectionName}' collection. Run app.js first!`);
      return;
    }

    const results = [];

    // Loop through records and calculate mathematical similarity
    snapshot.forEach(doc => {
      const data = doc.data();
      if (data.embedding && Array.isArray(data.embedding)) {
        const score = cosineSimilarity(queryVector, data.embedding);
        results.push({
          id: doc.id,
          name: data.name,
          content: data.content,
          similarity: score
        });
      }
    });

    // Sort the entries so the absolute best match is on top
    results.sort((a, b) => b.similarity - a.similarity);

    // Print out the top matches cleanly
    console.log("\n🎯 Top Matching Results:");
    results.slice(0, 3).forEach((match, index) => {
      console.log(`\n[${index + 1}] ${match.name} (Match Score: ${(match.similarity * 100).toFixed(2)}%)`);
      console.log(`📝 Description: ${match.content.substring(0, 140)}...`);
    });

  } catch (error) {
    console.error("❌ Search operation failed:", error.message || error);
  }
}

// --- Run a Test Query ---
// Go ahead and change this text to try out different matching concepts!
const testQuery = "We are seeking cloud computing, software engineering, and advanced web tech";
searchVector(testQuery);