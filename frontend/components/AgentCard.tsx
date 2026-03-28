"use client";

import { motion } from "framer-motion";
import { Brain, Zap, Clock, CheckCircle, AlertCircle, Loader } from "lucide-react";

interface Agent {
  id: string;
  name: string;
  role: string;
  status: "idle" | "thinking" | "working" | "completed" | "error";
  currentTask?: string;
  progress?: number;
  confidence?: number;
}

interface AgentCardProps {
  agent: Agent;
  index: number;
}

export default function AgentCard({ agent, index }: AgentCardProps) {
  const statusColors = {
    idle: "bg-slate-700 text-slate-400",
    thinking: "bg-pink-500/20 text-pink-400",
    working: "bg-slate-600/20 text-slate-300",
    completed: "bg-pink-500/30 text-pink-300",
    error: "bg-slate-800/20 text-slate-500",
  };

  const statusIcons = {
    idle: Clock,
    thinking: Brain,
    working: Loader,
    completed: CheckCircle,
    error: AlertCircle,
  };

  const StatusIcon = statusIcons[agent.status];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className="bg-slate-900/50 backdrop-blur-sm border border-pink-500/20 rounded-xl p-6 hover:border-pink-500/40 transition-all"
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-lg font-bold text-white mb-1">{agent.name}</h3>
          <p className="text-sm text-slate-400">{agent.role}</p>
        </div>
        <div
          className={`px-3 py-1 rounded-full text-xs font-semibold flex items-center gap-2 ${
            statusColors[agent.status]
          }`}
        >
          <StatusIcon className={`w-3 h-3 ${agent.status === 'working' ? 'animate-spin' : ''}`} />
          {agent.status}
        </div>
      </div>

      {/* Current Task */}
      {agent.currentTask && (
        <div className="mb-4">
          <p className="text-sm text-slate-300 mb-2">{agent.currentTask}</p>
          {agent.progress !== undefined && (
            <div className="w-full bg-slate-800 rounded-full h-2">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${agent.progress}%` }}
                transition={{ duration: 0.5 }}
                className="bg-gradient-to-r from-pink-500 to-pink-600 h-2 rounded-full"
              />
            </div>
          )}
        </div>
      )}

      {/* Confidence Score */}
      {agent.confidence !== undefined && (
        <div className="flex items-center gap-2">
          <Zap className="w-4 h-4 text-pink-500" />
          <span className="text-sm text-slate-400">Confidence:</span>
          <span className="text-sm font-semibold text-white">
            {(agent.confidence * 100).toFixed(0)}%
          </span>
        </div>
      )}
    </motion.div>
  );
}
