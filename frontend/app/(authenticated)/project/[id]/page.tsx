"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { useParams } from "next/navigation";
import AgentCard from "@/components/AgentCard";
import ActivityFeed from "@/components/ActivityFeed";
import CheckpointCard from "@/components/CheckpointCard";
import { ArrowLeft, Download, Share2, Settings } from "lucide-react";
import Link from "next/link";

interface Agent {
  id: string;
  name: string;
  role: string;
  status: "idle" | "thinking" | "working" | "completed" | "error";
  currentTask?: string;
  progress?: number;
  confidence?: number;
}

interface Checkpoint {
  id: string;
  phase: string;
  description: string;
  status: "completed" | "pending" | "blocked";
  agentCount: number;
  completedAt?: Date;
  deliverables: string[];
}

export default function ProjectPage() {
  const params = useParams();
  const projectId = params.id as string;

  const [project, setProject] = useState<any>(null);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [checkpoints, setCheckpoints] = useState<Checkpoint[]>([]);
  const [loading, setLoading] = useState(true);

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    fetchProjectData();
  }, [projectId]);

  const fetchProjectData = async () => {
    setLoading(true);
    try {
      // Simulated data - in production, fetch from API
      setProject({
        id: projectId,
        name: "SaaS Product Launch Campaign",
        description: "Complete go-to-market strategy and content for new product launch",
        status: "in_progress",
        progress: 65,
      });

      setAgents([
        {
          id: "1",
          name: "Research Master",
          role: "Market Research",
          status: "completed",
          confidence: 0.94,
        },
        {
          id: "2",
          name: "Strategy Architect",
          role: "Strategic Planning",
          status: "working",
          currentTask: "Developing positioning strategy based on research insights",
          progress: 45,
          confidence: 0.82,
        },
        {
          id: "3",
          name: "Creative Genius",
          role: "Copywriting",
          status: "idle",
        },
      ]);

      setCheckpoints([
        {
          id: "1",
          phase: "Research Phase",
          description: "Market analysis, competitor research, and trend identification",
          status: "completed",
          agentCount: 1,
          completedAt: new Date(Date.now() - 86400000),
          deliverables: [
            "Market Analysis Report",
            "Competitor Positioning Matrix",
            "Trend Forecast Document",
          ],
        },
        {
          id: "2",
          phase: "Strategy Phase",
          description: "Positioning, messaging, and go-to-market strategy",
          status: "pending",
          agentCount: 1,
          deliverables: [
            "Positioning Statement",
            "Messaging Framework",
            "GTM Roadmap",
          ],
        },
        {
          id: "3",
          phase: "Creative Phase",
          description: "Landing page copy, email sequences, and ad creative",
          status: "blocked",
          agentCount: 2,
          deliverables: [
            "Landing Page Copy",
            "Email Campaign (5 emails)",
            "Ad Creative Suite",
          ],
        },
      ]);
    } catch (error) {
      console.error("Error fetching project data:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = (checkpointId: string) => {
    console.log("Approved checkpoint:", checkpointId);
    // In production, send approval to API
  };

  const handleRevise = (checkpointId: string) => {
    console.log("Revision requested for checkpoint:", checkpointId);
    // In production, send revision request to API
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 flex items-center justify-center">
        <div className="w-16 h-16 border-4 border-pink-500/30 border-t-pink-500 rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-white p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <Link
            href="/dashboard"
            className="inline-flex items-center gap-2 text-slate-400 hover:text-pink-400 transition-colors mb-4"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Dashboard
          </Link>

          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-pink-500 to-pink-600 text-transparent bg-clip-text">
                {project.name}
              </h1>
              <p className="text-slate-400 text-lg mb-4">{project.description}</p>

              {/* Progress Bar */}
              <div className="w-full max-w-2xl">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-slate-400">Overall Progress</span>
                  <span className="text-sm font-semibold text-pink-400">
                    {project.progress}%
                  </span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-3">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${project.progress}%` }}
                    transition={{ duration: 1, ease: "easeOut" }}
                    className="bg-gradient-to-r from-pink-500 to-pink-600 h-3 rounded-full"
                  />
                </div>
              </div>
            </div>

            {/* Actions */}
            <div className="flex gap-3">
              <button className="p-3 bg-slate-900/50 border border-pink-500/30 rounded-xl hover:border-pink-500/50 transition-all">
                <Share2 className="w-5 h-5 text-pink-400" />
              </button>
              <button className="p-3 bg-slate-900/50 border border-pink-500/30 rounded-xl hover:border-pink-500/50 transition-all">
                <Download className="w-5 h-5 text-pink-400" />
              </button>
              <button className="p-3 bg-slate-900/50 border border-pink-500/30 rounded-xl hover:border-pink-500/50 transition-all">
                <Settings className="w-5 h-5 text-pink-400" />
              </button>
            </div>
          </div>
        </motion.div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Agents & Checkpoints */}
          <div className="lg:col-span-2 space-y-8">
            {/* Active Agents */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
            >
              <h2 className="text-2xl font-bold mb-4">Active Agents</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {agents.map((agent, index) => (
                  <AgentCard key={agent.id} agent={agent} index={index} />
                ))}
              </div>
            </motion.div>

            {/* Checkpoints */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
            >
              <h2 className="text-2xl font-bold mb-4">Project Checkpoints</h2>
              <div className="space-y-4">
                {checkpoints.map((checkpoint, index) => (
                  <CheckpointCard
                    key={checkpoint.id}
                    checkpoint={checkpoint}
                    index={index}
                    onApprove={handleApprove}
                    onRevise={handleRevise}
                  />
                ))}
              </div>
            </motion.div>
          </div>

          {/* Right Column - Activity Feed */}
          <div className="lg:col-span-1">
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
              className="sticky top-8 bg-slate-900/50 backdrop-blur-sm border border-pink-500/20 rounded-2xl p-6 h-[calc(100vh-8rem)]"
            >
              <ActivityFeed />
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
}
