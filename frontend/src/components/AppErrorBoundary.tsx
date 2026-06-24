import { Component, type ErrorInfo, type ReactNode } from "react";
import { RefreshCw } from "lucide-react";

interface AppErrorBoundaryProps {
  children: ReactNode;
}

interface AppErrorBoundaryState {
  failed: boolean;
}

export class AppErrorBoundary extends Component<AppErrorBoundaryProps, AppErrorBoundaryState> {
  state: AppErrorBoundaryState = { failed: false };

  static getDerivedStateFromError(): AppErrorBoundaryState {
    return { failed: true };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error("Unexpected frontend render error", error, info);
  }

  render() {
    if (!this.state.failed) {
      return this.props.children;
    }

    return (
      <main className="app-shell">
        <div className="status status-error" role="alert">
          <div>
            <strong>Application error</strong>
            <span>The interface could not be rendered. Reload the page to reset its state.</span>
          </div>
          <button className="secondary-button" type="button" onClick={() => window.location.reload()}>
            <RefreshCw aria-hidden="true" size={18} />
            Reload
          </button>
        </div>
      </main>
    );
  }
}
