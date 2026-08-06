function ResultRow({ icon, label, value }: { icon: React.ReactNode; label: string; value?: string | React.ReactNode }) {
  if (!value) return null;

  return (
    <div className="flex items-start gap-3">
      <span className="flex items-center justify-center size-8 rounded-full bg-slate-100 shrink-0 mt-0.5">
        {icon}
      </span>
      <div className="flex flex-col">
        <span className="text-xs font-medium text-slate-100 uppercase tracking-wide">{label}</span>
        <span className="text-sm text-slate-100">{value}</span>
      </div>
    </div>
  );
}

export default ResultRow