"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Search, Star, TrendingUp, Zap, Users, Clock } from "lucide-react";

interface AgentTemplate {
  template_id: string;
  name: string;
  description: string;
  category: string;
  usage_count: number;
  avg_rating: number;
  success_rate: number;
  tags: string[];
  is_free: boolean;
  price: number;
}

export default function MarketplacePage() {
  const [templates, setTemplates] = useState<AgentTemplate[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    async function fetchTemplates() {
      setLoading(true);
      try {
        const categoryParam = selectedCategory ? `?category=${selectedCategory}` : "";
        const response = await fetch(`/api/marketplace/templates${categoryParam}`);
        const data = await response.json();
        setTemplates(data.templates || []);
      } catch (error) {
        console.error("Error fetching templates:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchTemplates();
  }, [selectedCategory]);

  const handleSearch = async () => {
    if (!searchQuery) {
      fetchTemplates();
      return;
    }

    try {
      const response = await fetch(`/api/marketplace/search?query=${encodeURIComponent(searchQuery)}`);
      const data = await response.json();
      setTemplates(data.results || []);
    } catch (error) {
      console.error("Error searching templates:", error);
    }
  };

  const categories = [
    { id: "research", name: "Research", icon: "🔍" },
    { id: "strategy", name: "Strategy", icon: "🎯" },
    { id: "creative", name: "Creative", icon: "✨" },
    { id: "technical", name: "Technical", icon: "⚙️" },
    { id: "analytics", name: "Analytics", icon: "📊" },
    { id: "operations", name: "Operations", icon: "🔄" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-white p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-12"
        >
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-pink-500 to-pink-600 text-transparent bg-clip-text">
            Agent Marketplace
          </h1>
          <p className="text-slate-400 text-lg">
            Discover, share, and monetize specialized AI agents
          </p>
        </motion.div>

        {/* Search Bar */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-8 relative"
        >
          <div className="flex gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search for agent templates..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && handleSearch()}
                className="w-full bg-slate-900/50 border border-pink-500/30 rounded-xl py-4 pl-12 pr-4 text-white placeholder-slate-500 focus:outline-none focus:border-pink-500/50 focus:ring-2 focus:ring-pink-500/20"
              />
            </div>
            <button
              onClick={handleSearch}
              className="px-8 py-4 bg-gradient-to-r from-pink-500 to-pink-600 rounded-xl font-semibold hover:from-pink-600 hover:to-pink-700 transition-all transform hover:scale-105"
            >
              Search
            </button>
          </div>
        </motion.div>

        {/* Category Filter */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-8 flex gap-3 flex-wrap"
        >
          <button
            onClick={() => {
              setSelectedCategory(null);
              setSearchQuery("");
            }}
            className={`px-6 py-3 rounded-xl font-medium transition-all ${
              selectedCategory === null
                ? "bg-pink-500 text-white"
                : "bg-slate-900/50 text-slate-400 hover:bg-slate-800"
            }`}
          >
            All
          </button>
          {categories.map((category) => (
            <button
              key={category.id}
              onClick={() => {
                setSelectedCategory(category.id);
                setSearchQuery("");
              }}
              className={`px-6 py-3 rounded-xl font-medium transition-all flex items-center gap-2 ${
                selectedCategory === category.id
                  ? "bg-pink-500 text-white"
                  : "bg-slate-900/50 text-slate-400 hover:bg-slate-800"
              }`}
            >
              <span>{category.icon}</span>
              {category.name}
            </button>
          ))}
        </motion.div>

        {/* Loading State */}
        {loading && (
          <div className="flex justify-center items-center py-20">
            <div className="w-16 h-16 border-4 border-pink-500/30 border-t-pink-500 rounded-full animate-spin"></div>
          </div>
        )}

        {/* Templates Grid */}
        {!loading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
          >
            {templates.map((template, index) => (
              <motion.div
                key={template.template_id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
                className="bg-slate-900/50 backdrop-blur-sm border border-pink-500/20 rounded-2xl p-6 hover:border-pink-500/40 transition-all cursor-pointer group"
              >
                {/* Header */}
                <div className="mb-4">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="text-xl font-bold text-white group-hover:text-pink-400 transition-colors">
                      {template.name}
                    </h3>
                    {template.is_free ? (
                      <span className="px-3 py-1 bg-pink-500/20 text-pink-400 rounded-full text-xs font-semibold">
                        FREE
                      </span>
                    ) : (
                      <span className="px-3 py-1 bg-slate-700/50 text-slate-300 rounded-full text-xs font-semibold">
                        ${template.price}
                      </span>
                    )}
                  </div>
                  <p className="text-slate-400 text-sm line-clamp-2">
                    {template.description}
                  </p>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-3 gap-4 mb-4">
                  <div className="flex items-center gap-2">
                    <Star className="w-4 h-4 text-pink-500" />
                    <span className="text-sm font-semibold">{template.avg_rating.toFixed(1)}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Users className="w-4 h-4 text-slate-400" />
                    <span className="text-sm font-semibold">{template.usage_count}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Zap className="w-4 h-4 text-pink-400" />
                    <span className="text-sm font-semibold">{(template.success_rate * 100).toFixed(0)}%</span>
                  </div>
                </div>

                {/* Tags */}
                <div className="flex flex-wrap gap-2 mb-4">
                  {template.tags.slice(0, 3).map((tag) => (
                    <span
                      key={tag}
                      className="px-2 py-1 bg-slate-800/50 text-slate-400 rounded-lg text-xs"
                    >
                      #{tag}
                    </span>
                  ))}
                </div>

                {/* Action Button */}
                <button className="w-full py-3 bg-gradient-to-r from-pink-500/20 to-pink-600/20 border border-pink-500/30 rounded-xl font-semibold text-pink-400 hover:from-pink-500 hover:to-pink-600 hover:text-white transition-all transform hover:scale-105">
                  Use Template
                </button>
              </motion.div>
            ))}
          </motion.div>
        )}

        {/* Empty State */}
        {!loading && templates.length === 0 && (
          <div className="text-center py-20">
            <div className="text-6xl mb-4">🔍</div>
            <h3 className="text-2xl font-bold mb-2">No templates found</h3>
            <p className="text-slate-400">Try adjusting your search or filters</p>
          </div>
        )}

        {/* Trending Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mt-16"
        >
          <div className="flex items-center gap-3 mb-6">
            <TrendingUp className="w-6 h-6 text-pink-500" />
            <h2 className="text-3xl font-bold">Trending This Week</h2>
          </div>
          <div className="bg-slate-900/30 border border-pink-500/20 rounded-2xl p-6">
            <p className="text-slate-400">
              Trending templates will appear here based on usage and ratings.
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
