import { AlertCircle, CheckCircle2 } from "lucide-react";

interface StatusMessageProps {
  tone: "error" | "success";
  title: string;
  detail?: string;
}

export function StatusMessage({ tone, title, detail }: StatusMessageProps) {
  const Icon = tone === "error" ? AlertCircle : CheckCircle2;

  return (
    <div className={`status status-${tone}`} role={tone === "error" ? "alert" : "status"}>
      <Icon aria-hidden="true" size={18} />
      <div>
        <strong>{title}</strong>
        {detail ? <span>{detail}</span> : null}
      </div>
    </div>
  );
}
