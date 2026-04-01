"use client";

import { motion } from "framer-motion";
import { CheckCircle, Clock, AlertCircle, ChevronRight } from "lucide-react";

interface Checkpoint {
  id: string;
  phase: string;
  description: string;
  status: "completed" | "pending" | "blocked";
  agentCount: number;
  completedAt?: Date;
  deliverables: string[];
}

interface CheckpointCardProps {
  checkpoint: Checkpoint;
  index: number;
  onApprove?: (id: string) => void;
  onRevise?: (id: string) => void;
}

export default function CheckpointCard({
  checkpoint,
  index,
  onApprove,
  onRevise,
}: CheckpointCardProps) {
  const statusConfig = {
    completed: {
      icon: CheckCircle,
      color: "text-teal-400",
      bg: "bg-teal-500/10",
      border: "border-teal-500/30",
    },
    pending: {
      icon: Clock,
      color: "text-slate-400",
      bg: "bg-slate-500/10",
      border: "border-slate-500/30",
    },
    blocked: {
      icon: AlertCircle,
      color: "text-slate-500",
      bg: "bg-slate-600/10",
      border: "border-slate-600/30",
    },
  };

  const config = statusConfig[checkpoint.status];
  const StatusIcon = config.icon;

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.1 }}
      className={`bg-slate-900/50 backdrop-blur-sm border ${config.border} rounded-xl p-6`}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-start gap-3 flex-1">
          <div className={`p-2 rounded-lg ${config.bg}`}>
            <StatusIcon className={`w-5 h-5 ${config.color}`} />
          </div>
          <div className="flex-1">
            <h3 className="text-lg font-bold text-white mb-1">{checkpoint.phase}</h3>
            <p className="text-sm text-slate-400">{checkpoint.description}</p>
          </div>
        </div>
        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${config.bg} ${config.color}`}>
          {checkpoint.status}
        </span>
      </div>

      {/* Metadata */}
      <div className="flex items-center gap-4 mb-4 text-sm text-slate-400">
        <span>{checkpoint.agentCount} agents</span>
        {checkpoint.completedAt && (
          <span>Completed {checkpoint.completedAt.toLocaleDateString()}</span>
        )}
      </div>

      {/* Deliverables */}
      <div className="mb-4">
        <p className="text-xs font-semibold text-slate-500 uppercase mb-2">Deliverables</p>
        <div className="space-y-2">
          {checkpoint.deliverables.map((deliverable, idx) => (
            <div
              key={idx}
              className="flex items-center gap-2 text-sm text-slate-300"
            >
              <ChevronRight className="w-4 h-4 text-teal-500" />
              {deliverable}
            </div>
          ))}
        </div>
      </div>

      {/* Actions */}
      {checkpoint.status === "completed" && onApprove && onRevise && (
        <div className="flex gap-3">
          <button
            onClick={() => onApprove(checkpoint.id)}
            className="flex-1 py-3 bg-gradient-to-r from-teal-500/20 to-teal-600/20 border border-teal-500/30 rounded-lg font-semibold text-teal-400 hover:from-teal-500 hover:to-teal-600 hover:text-white transition-all"
          >
            Approve
          </button>
          <button
            onClick={() => onRevise(checkpoint.id)}
            className="flex-1 py-3 bg-slate-800/50 border border-slate-700 rounded-lg font-semibold text-slate-400 hover:bg-slate-700 hover:text-white transition-all"
          >
            Request Revision
          </button>
        </div>
      )}

      {checkpoint.status === "pending" && (
        <div className="py-3 bg-slate-500/10 border border-slate-500/30 rounded-lg text-center">
          <p className="text-sm text-slate-400 font-semibold">
            Agents are working on this phase...
          </p>
        </div>
      )}

      {checkpoint.status === "blocked" && (
        <div className="py-3 bg-slate-600/10 border border-slate-600/30 rounded-lg text-center">
          <p className="text-sm text-slate-500 font-semibold">
            Your input required to continue
          </p>
        </div>
      )}
    </motion.div>
  );
}
