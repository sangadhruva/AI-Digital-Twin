import { useEffect, useState } from "react";

import Header from "./components/Header";
import UploadPanel from "./components/UploadPanel";
import ChatWindow from "./components/ChatWindow";

import {
  api,
  type DocumentStatusResponse,
  type UploadResponse,
} from "./services/api";

import "./styles/app.css";

function App() {
  const [uploadedFiles, setUploadedFiles] =
    useState<string[]>([]);

  const [isCheckingDocument, setIsCheckingDocument] =
    useState(true);

  useEffect(() => {
    const loadActiveDocument = async () => {
      try {
        const response =
          await api.get<DocumentStatusResponse>(
            "/documents/status",
          );

        if (
          response.data.has_document &&
          response.data.original_filename
        ) {
          setUploadedFiles([
            response.data.original_filename,
          ]);
        } else {
          setUploadedFiles([]);
        }
      } catch (error) {
        console.error(
          "Unable to load active candidate document:",
          error,
        );

        setUploadedFiles([]);
      } finally {
        setIsCheckingDocument(false);
      }
    };

    void loadActiveDocument();
  }, []);

  const uploadDocument = async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await api.post<UploadResponse>(
      "/documents/upload",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      },
    );

    const uploadedFilename =
      response.data.document.original_filename;

    setUploadedFiles([
      uploadedFilename,
    ]);
  };

  const clearCandidate = async () => {
    await api.delete(
      "/documents/clear",
    );

    setUploadedFiles([]);
  };

  const activeDocument =
    uploadedFiles.length > 0
      ? uploadedFiles[0]
      : null;

  if (isCheckingDocument) {
    return (
      <div className="app-shell">
        <div className="app-loading-screen">
          <div className="brand-icon">AI</div>

          <h2>Loading Candidate Digital Twin</h2>

          <p>
            Checking for an active candidate document...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="app-shell">
      <Header
        documentCount={uploadedFiles.length}
      />

      <main className="dashboard-layout">
        <UploadPanel
          uploadedFiles={uploadedFiles}
          onUpload={uploadDocument}
          onClear={clearCandidate}
        />

        <ChatWindow
          hasDocuments={
            uploadedFiles.length > 0
          }
          activeDocument={activeDocument}
        />
      </main>
    </div>
  );
}

export default App;