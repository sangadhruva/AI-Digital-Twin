import { useRef, useState } from "react";

type UploadPanelProps = {
  uploadedFiles: string[];
  onUpload: (file: File) => Promise<void>;
  onClear: () => Promise<void>;
};

function UploadPanel({
  uploadedFiles,
  onUpload,
  onClear,
}: UploadPanelProps) {
  const inputRef = useRef<HTMLInputElement | null>(null);

  const [isUploading, setIsUploading] = useState(false);
  const [isClearing, setIsClearing] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");

  const selectFile = () => {
    inputRef.current?.click();
  };

  const handleFileChange = async (
    event: React.ChangeEvent<HTMLInputElement>,
  ) => {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    const extension = file.name
      .split(".")
      .pop()
      ?.toLowerCase();

    if (
      !extension ||
      !["pdf", "docx", "txt"].includes(extension)
    ) {
      setStatusMessage(
        "Only PDF, DOCX, and TXT files are supported.",
      );

      event.target.value = "";
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setStatusMessage("Maximum file size is 10 MB.");
      event.target.value = "";
      return;
    }

    try {
      setIsUploading(true);
      setStatusMessage(
        "Uploading and indexing candidate document...",
      );

      await onUpload(file);

      setStatusMessage(
        "Candidate document indexed successfully.",
      );
    } catch (error) {
      console.error(error);

      setStatusMessage(
        "Document upload failed. Check that the backend is running.",
      );
    } finally {
      setIsUploading(false);
      event.target.value = "";
    }
  };

  const handleClearCandidate = async () => {
    const confirmed = window.confirm(
      "Clear the active candidate document and reset the assistant?",
    );

    if (!confirmed) {
      return;
    }

    try {
      setIsClearing(true);
      setStatusMessage("Clearing candidate profile...");

      await onClear();

      setStatusMessage(
        "Candidate profile cleared successfully.",
      );
    } catch (error) {
      console.error(error);

      setStatusMessage(
        "Unable to clear the candidate profile.",
      );
    } finally {
      setIsClearing(false);
    }
  };

  return (
    <aside className="upload-panel">
      <div className="panel-heading">
        <span className="panel-icon">📄</span>

        <div>
          <h2>Candidate Documents</h2>
          <p>
            Upload a resume or supporting document for recruiter
            questions.
          </p>
        </div>
      </div>

      <div className="upload-box">
        <div className="upload-circle">⬆</div>

        <h3>Upload Candidate Resume</h3>

        <p>PDF, DOCX, or TXT files up to 10 MB</p>

        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.docx,.txt"
          hidden
          onChange={handleFileChange}
        />

        <button
          type="button"
          className="primary-button"
          onClick={selectFile}
          disabled={isUploading || isClearing}
        >
          {isUploading
            ? "Uploading..."
            : uploadedFiles.length > 0
              ? "Replace document"
              : "Choose file"}
        </button>

        {statusMessage && (
          <p className="upload-status">
            {statusMessage}
          </p>
        )}
      </div>

      <section className="uploaded-section">
        <div className="section-title-row">
          <h3>Active Candidate Document</h3>
          <span>{uploadedFiles.length}</span>
        </div>

        {uploadedFiles.length === 0 ? (
          <div className="empty-documents">
            <span>📂</span>
            <p>No candidate document uploaded yet.</p>
          </div>
        ) : (
          <>
            <div className="document-list">
              {uploadedFiles.map((file, index) => (
                <div
                  className="document-card"
                  key={`${file}-${index}`}
                >
                  <span className="document-icon">
                    {file
                      .split(".")
                      .pop()
                      ?.toUpperCase() || "FILE"}
                  </span>

                  <div>
                    <strong>{file}</strong>
                    <small>
                      Ready for recruiter questions
                    </small>
                  </div>
                </div>
              ))}
            </div>

            <button
              type="button"
              className="clear-candidate-button"
              onClick={handleClearCandidate}
              disabled={isUploading || isClearing}
            >
              {isClearing
                ? "Clearing..."
                : "Clear Candidate"}
            </button>
          </>
        )}
      </section>
    </aside>
  );
}

export default UploadPanel;