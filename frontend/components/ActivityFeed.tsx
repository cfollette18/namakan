"use client";

import { motion, AnimatePresence } from "framer-motion";
import { Brain, Code, FileText, CheckCircle, AlertTriangle, Info } from "lucide-react";
import { useEffect, useState } from "react";

interface Activity {
  id: string;
  type: "thinking" | "action" | "output" | "success" | "warning" | "info";
  agent: string;
  message: string;
  timestamp: Date;
  details?: string;
}

interface ActivityFeedProps {
  maxItems?: number;
  autoScroll?: boolean;
}

export default function ActivityFeed({ maxItems = 50, autoScroll = true }: ActivityFeedProps) {
  const [activities, setActivities] = useState<Activity[]>([]);

  useEffect(() => {
    // Simulated activities - in production, this would connect to WebSocket
    const demoActivities: Activity[] = [
      {
        id: "1",
        type: "info",
        agent: "Orchestrator",
        message: "Analyzing project requirements...",
        timestamp: new Date(Date.now() - 60000),
      },
      {
        id: "2",
        type: "thinking",
        agent: "Research Agent",
        message: "Gathering market intelligence on competitor landscape",
        timestamp: new Date(Date.now() - 45000),
        details: "Scanning 15 competitor websites and analyzing positioning...",
      },
      {
        id: "3",
        type: "action",
        agent: "Research Agent",
        message: "Completed web scraping of top 10 competitors",
        timestamp: new Date(Date.now() - 30000),
      },
      {
        id: "4",
        type: "success",
        agent: "Research Agent",
        message: "Research phase completed with 94% confidence",
        timestamp: new Date(Date.now() - 15000),
      },
      {
        id: "5",
        type: "thinking",
        agent: "Strategy Agent",
        message: "Developing positioning strategy based on research insights",
        timestamp: new Date(Date.now() - 5000),
      },
    ];

    setActivities(demoActivities);
  }, []);

  const getIcon = (type: Activity["type"]) => {
    switch (type) {
      case "thinking":
        return Brain;
      case "action":
        return Code;
      case "output":
        return FileText;
      case "success":
        return CheckCircle;
      case "warning":
        return AlertTriangle;
      default:
        return Info;
    }
  };

  const getColor = (type: Activity["type"]) => {
    switch (type) {
      case "thinking":
        return "text-pink-400 bg-pink-500/10";
      case "action":
        return "text-slate-300 bg-slate-500/10";
      case "output":
        return "text-slate-400 bg-slate-600/10";
      case "success":
        return "text-pink-300 bg-pink-500/20";
      case "warning":
        return "text-slate-500 bg-slate-700/20";
      default:
        return "text-slate-400 bg-slate-500/10";
    }
  };

  const formatTimestamp = (date: Date) => {
    const now = new Date();
    const diff = Math.floor((now.getTime() - date.getTime()) / 1000);

    if (diff < 60) return `${diff}s ago`;
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
    return date.toLocaleDateString();
  };

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between mb-4 pb-4 border-b border-pink-500/20">
        <h2 className="text-xl font-bold text-white">Activity Feed</h2>
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
          <span className="text-sm text-slate-400">Live</span>
        </div>
      </div>

      {/* Activity List */}
      <div className="flex-1 overflow-y-auto space-y-3 pr-2 scrollbar-thin scrollbar-thumb-pink-500/20 scrollbar-track-transparent">
        <AnimatePresence>
          {activities.map((activity, index) => {
            const Icon = getIcon(activity.type);
            const colorClass = getColor(activity.type);

            return (
              <motion.div
                key={activity.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                transition={{ delay: index * 0.05 }}
                className="bg-slate-900/50 backdrop-blur-sm border border-pink-500/20 rounded-lg p-4 hover:border-pink-500/40 transition-all"
              >
                <div className="flex items-start gap-3">
                  {/* Icon */}
                  <div className={`p-2 rounded-lg ${colorClass}`}>
                    <Icon className="w-4 h-4" />
                  </div>

                  {/* Content */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-2 mb-1">
                      <p className="text-sm font-semibold text-pink-400">
                        {activity.agent}
                      </p>
                      <span className="text-xs text-slate-500 whitespace-nowrap">
                        {formatTimestamp(activity.timestamp)}
                      </span>
                    </div>
                    <p className="text-sm text-slate-300 mb-1">{activity.message}</p>
                    {activity.details && (
                      <p className="text-xs text-slate-500 italic">{activity.details}</p>
                    )}
                  </div>
                </div>
              </motion.div>
            );
          })}
        </AnimatePresence>
      </div>

      {/* Footer Stats */}
      <div className="mt-4 pt-4 border-t border-pink-500/20 flex items-center justify-between text-sm">
        <span className="text-slate-400">{activities.length} events</span>
        <button className="text-pink-400 hover:text-pink-300 transition-colors">
          Clear All
        </button>
      </div>
    </div>
  );
}
