type HeaderProps = {
  documentCount: number;
};

function Header({ documentCount }: HeaderProps) {
  return (
    <header className="app-header">
      <div className="brand">
        <div className="brand-icon">AI</div>

        <div>
          <h1>Candidate Digital Twin</h1>
          <p>
            An AI recruiter assistant grounded in candidate documents
          </p>
        </div>
      </div>

      <div className="header-status">
        <span className="status-dot" />

        <span>
          {documentCount > 0
            ? `${documentCount} candidate document${
                documentCount === 1 ? "" : "s"
              } indexed`
            : "No candidate document indexed"}
        </span>
      </div>
    </header>
  );
}

export default Header;