import { useEffect, useRef, useState } from "react";

import ChatMessage, { type Message } from "./ChatMessage";
import { api, type AgentResponse } from "../services/api";

type ChatWindowProps = {
  hasDocuments: boolean;
  activeDocument: string | null;
};

const createStarterMessages = (
  hasDocuments: boolean,
): Message[] => [
  {
    id: 1,
    role: "assistant",
    content: hasDocuments
      ? "The candidate document is ready. You can now ask about skills, education, experience, projects, or certifications."
      : "Please upload a candidate resume or supporting document before asking questions.",
  },
];

function ChatWindow({
  hasDocuments,
  activeDocument,
}: ChatWindowProps) {
  const [messages, setMessages] = useState<Message[]>(
    createStarterMessages(hasDocuments),
  );

  const [question, setQuestion] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  /*
   * Reset the conversation whenever:
   * 1. The first document is uploaded.
   * 2. A different document replaces the previous document.
   */
  useEffect(() => {
    setMessages(createStarterMessages(hasDocuments));
    setQuestion("");
    setIsLoading(false);
  }, [hasDocuments, activeDocument]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, isLoading]);

  const sendMessage = async (customQuestion?: string) => {
    const finalQuestion = (customQuestion ?? question).trim();

    if (!hasDocuments) {
      setMessages((currentMessages) => [
        ...currentMessages,
        {
          id: Date.now(),
          role: "assistant",
          content:
            "Please upload a candidate resume or document before asking questions.",
        },
      ]);

      return;
    }

    if (!finalQuestion || isLoading) {
      return;
    }

    const userMessage: Message = {
      id: Date.now(),
      role: "user",
      content: finalQuestion,
    };

    setMessages((currentMessages) => [
      ...currentMessages,
      userMessage,
    ]);

    setQuestion("");
    setIsLoading(true);

    try {
      const response = await api.post<AgentResponse>(
        "/agent/ask",
        {
          question: finalQuestion,
        },
      );

      const assistantMessage: Message = {
        id: Date.now() + 1,
        role: "assistant",
        content: response.data.answer,
        sources: response.data.sources,
      };

      setMessages((currentMessages) => [
        ...currentMessages,
        assistantMessage,
      ]);
    } catch (error) {
      console.error(error);

      setMessages((currentMessages) => [
        ...currentMessages,
        {
          id: Date.now() + 1,
          role: "assistant",
          content:
            "I could not process the question. Make sure the backend is running and a candidate document has been indexed.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section className="chat-panel">
      <div className="chat-heading">
        <div>
          <span className="eyebrow">
            Recruiter Assistant
          </span>

          <h2>Candidate Digital Twin</h2>

          <p>
            Ask about the candidate&apos;s skills, education,
            projects, experience, or certifications.
          </p>
        </div>

        <div className="online-badge">
          <span />
          {hasDocuments ? "Ready" : "Waiting for document"}
        </div>
      </div>

      <div className="suggestion-row">
        <button
          type="button"
          onClick={() =>
            void sendMessage("Tell me about yourself.")
          }
          disabled={isLoading || !hasDocuments}
        >
          Tell me about yourself
        </button>

        <button
          type="button"
          onClick={() =>
            void sendMessage(
              "What programming languages and technical skills do you know?",
            )
          }
          disabled={isLoading || !hasDocuments}
        >
          Technical skills
        </button>

        <button
          type="button"
          onClick={() =>
            void sendMessage(
              "What certifications do you have?",
            )
          }
          disabled={isLoading || !hasDocuments}
        >
          Certifications
        </button>
      </div>

      <div className="messages-area">
        {messages.map((message) => (
          <ChatMessage
            message={message}
            key={message.id}
          />
        ))}

        {isLoading && (
          <div className="message-row">
            <div className="message-avatar">AI</div>

            <div className="message-bubble loading-bubble">
              <p>Thinking</p>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="chat-composer">
        <textarea
          value={question}
          onChange={(event) =>
            setQuestion(event.target.value)
          }
          onKeyDown={(event) => {
            if (
              event.key === "Enter" &&
              !event.shiftKey
            ) {
              event.preventDefault();
              void sendMessage();
            }
          }}
          placeholder={
            hasDocuments
              ? "Ask anything about this candidate..."
              : "Upload a candidate document first..."
          }
          disabled={isLoading || !hasDocuments}
        />

        <button
          type="button"
          onClick={() => void sendMessage()}
          disabled={
            isLoading ||
            !hasDocuments ||
            !question.trim()
          }
        >
          {isLoading ? "Wait" : "Send"}
        </button>
      </div>

      <p className="composer-note">
        {hasDocuments
          ? `Answers are generated only from ${activeDocument ?? "the indexed document"}.`
          : "Upload a candidate document to activate the assistant."}
      </p>
    </section>
  );
}

export default ChatWindow;