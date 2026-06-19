# src/rag_pipeline.py

import os

from pypdf import PdfReader
from google import genai
from langchain.text_splitter import RecursiveCharacterTextSplitter

import chromadb

from src.config import (
    GEMINI_API_KEY,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)


class RAGPipeline:

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.chroma = chromadb.PersistentClient(
            path="./chroma_db"
        )

        self.collection = self.chroma.get_or_create_collection(
            name="support_kb"
        )

    def load_document(self, file_path):

        ext = os.path.splitext(file_path)[1]

        if ext in [".txt", ".md"]:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as f:

                return f.read()

        if ext == ".pdf":

            reader = PdfReader(file_path)

            text = ""

            for page in reader.pages:
                text += page.extract_text() + "\n"

            return text

        return ""

    def get_embedding(self, text):

        response = self.client.models.embed_content(
            model="text-embedding-004",
            contents=text
        )

        return response.embeddings[0].values

    def ingest_folder(self, folder="data"):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )

        for file in os.listdir(folder):

            path = os.path.join(folder, file)

            content = self.load_document(path)

            chunks = splitter.split_text(content)

            for idx, chunk in enumerate(chunks):

                embedding = self.get_embedding(chunk)

                self.collection.add(
                    ids=[f"{file}_{idx}"],
                    documents=[chunk],
                    embeddings=[embedding],
                    metadatas=[{
                        "source": file,
                        "chunk": idx
                    }]
                )

    def retrieve(self, query, top_k=3):

        query_embedding = self.get_embedding(query)

        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        contexts = []

        docs = result["documents"][0]
        meta = result["metadatas"][0]
        dist = result["distances"][0]

        for d, m, score in zip(docs, meta, dist):

            contexts.append({
                "text": d,
                "source": m["source"],
                "score": 1 - score
            })

        return contexts