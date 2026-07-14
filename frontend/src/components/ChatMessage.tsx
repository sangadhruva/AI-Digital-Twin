export type Message = {
  id: number;
  role: "assistant" | "user";
  content: string;
  sources?: string[];
};

type ChatMessageProps = {
  message: Message;
};

function ChatMessage({ message }: ChatMessageProps) {
  return (
    <article
      className={`message-row ${
        message.role === "user" ? "user-message-row" : ""
      }`}
    >
      <div
        className={`message-avatar ${
          message.role === "user" ? "user-avatar" : ""
        }`}
      >
        {message.role === "assistant" ? "AI" : "You"}
      </div>

      <div
        className={`message-bubble ${
          message.role === "user" ? "user-bubble" : ""
        }`}
      >
        <p>{message.content}</p>

        {message.sources && message.sources.length > 0 && (
          <div className="message-sources">
            <span>Sources</span>

            {message.sources.map((source) => (
              <small key={source}>📄 {source}</small>
            ))}
          </div>
        )}
      </div>
    </article>
  );
}

export default ChatMessage;