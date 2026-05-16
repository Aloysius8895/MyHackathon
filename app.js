import { GoogleGenAI } from '@google/genai';
import admin from 'firebase-admin';
import dotenv from 'dotenv';
import fs from 'fs';
import path from 'path';

// Load your service account JSON file securely
import serviceAccount from './firebase-key.json' with { type: 'json' };

dotenv.config();

// 1. Initialize Google Gen AI & Firebase Admin
const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});
const db = admin.firestore();

// 2. Main Processing Function
async function processPipeline(folderName, collectionName) {
  const directoryPath = path.join(process.cwd(), 'data', folderName);
  
  if (!fs.existsSync(directoryPath)) {
    console.log(`Directory data/${folderName} not found. Skipping.`);
    return;
  }

  const files = fs.readdirSync(directoryPath);
  console.log(`\n📂 Found ${files.length} files in data/${folderName}...`);

  for (const file of files) {
    if (!file.endsWith('.txt')) continue;

    const filePath = path.join(directoryPath, file);
    const rawContent = fs.readFileSync(filePath, 'utf-8');
    const docId = path.parse(file).name;

    try {
      console.log(`✨ Vectorizing document: ${docId}...`);

      // FIX: Wrapped rawContent in array brackets [] so the SDK validates it correctly
      const response = await ai.models.embedContent({
        model: 'gemini-embedding-001',
        contents: [rawContent], 
      });

      // Extract the vector values from the plural embeddings array structure
      const embeddingVector = response.embeddings?.[0]?.values || response.values;
    
      if (!embeddingVector) {
        console.log("⚠️ Full SDK Response:", JSON.stringify(response, null, 2));
        throw new Error("Could not find the embedding vector array in the response.");
      }

      // Structure data and upsert to Firestore
      await db.collection(collectionName).doc(docId).set({
        name: docId.replace(/-/g, ' '),
        content: rawContent,
        embedding: embeddingVector, // Vector coordinates saved here
        updatedAt: admin.firestore.FieldValue.serverTimestamp()
      });

      console.log(`✅ Successfully loaded ${docId} to Firestore.`);
    } catch (error) {
      console.error(`❌ Failed processing ${file}:`, error.message || error);
    }
  }
}

// 3. Execution Wrapper
async function run() {
  console.log('🚀 Launching Ingestion Pipeline...');
  await processPipeline('startups', 'startups');
  await processPipeline('mentors', 'mentors');
  console.log('\n🏁 Pipeline process complete!');
}

run();