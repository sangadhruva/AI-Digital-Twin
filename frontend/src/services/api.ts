import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_URL ||
  "http://127.0.0.1:8001";

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000,
});

export type UploadedDocument = {
  original_filename: string;
  stored_filename: string;
  file_type: string;
  size_bytes: number;
  character_count: number;
  word_count: number;
  chunk_count: number;
  vector_store_count: number;
  text_preview: string;
};

export type UploadResponse = {
  message: string;
  document: UploadedDocument;
};

export type DocumentStatusResponse = {
  has_document: boolean;
  original_filename: string | null;
  stored_filename: string | null;
  stored_chunks: number;
};

export type AgentResponse = {
  question: string;
  intent: string;
  answer: string;
  sources: string[];
  retrieved_chunks: number;
};