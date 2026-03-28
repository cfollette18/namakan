'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import {
  Sparkles,
  Plus,
  TrendingUp,
  Clock,
  CheckCircle,
  Users,
  BarChart3,
  Activity,
  Zap,
  Target,
  DollarSign,
  ArrowRight,
  Play,
  Pause,
  Settings,
  Eye,
  LayoutDashboard,
  FileText,
  ShoppingBag,
  PieChart,
  UserPlus,
  Search,
  Filter,
  Download,
  Star,
  MessageSquare,
  Calendar,
  Briefcase,
  Award,
  BookOpen
} from 'lucide-react'

interface Project {
  id: string
  name: string
  status: 'active' | 'completed' | 'paused'
  progress: number
  agents: number
  startDate: Date
  estimatedCompletion: Date
  budget: number
  spent: number
}

interface AgentActivity {
  id: string
  agentName: string
  action: string
  timestamp: Date
  projectId: string
}

interface Metric {
  label: string
  value: string
  change: string
  trend: 'up' | 'down' | 'neutral'
}

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('overview')
  const [showCreateProject, setShowCreateProject] = useState(false)
  const [projectDescription, setProjectDescription] = useState('')
  const [projects, setProjects] = useState<Project[]>([])
  const [recentActivity, setRecentActivity] = useState<AgentActivity[]>([])
  const [templates, setTemplates] = useState<any[]>([])
  const [analytics, setAnalytics] = useState<any>({})

  const tabs = [
    { id: 'overview', label: 'Overview', icon: LayoutDashboard },
    { id: 'projects', label: 'Projects', icon: Briefcase },
    { id: 'templates', label: 'Templates', icon: FileText },
    { id: 'marketplace', label: 'Marketplace', icon: ShoppingBag },
    { id: 'analytics', label: 'Analytics', icon: PieChart },
    { id: 'team', label: 'Team', icon: Users },
    { id: 'learning', label: 'Learning', icon: BookOpen }
  ]

  // Mock data - in production, this would come from API
  useEffect(() => {
    setProjects([
      {
        id: '1',
        name: 'SaaS Product Launch Campaign',
        status: 'active',
        progress: 75,
        agents: 7,
        startDate: new Date(Date.now() - 86400000 * 2),
        estimatedCompletion: new Date(Date.now() + 86400000 * 3),
        budget: 150,
        spent: 87
      },
      {
        id: '2',
        name: 'Market Research & Analysis',
        status: 'completed',
        progress: 100,
        agents: 3,
        startDate: new Date(Date.now() - 86400000 * 7),
        estimatedCompletion: new Date(Date.now() - 86400000 * 1),
        budget: 75,
        spent: 62
      },
      {
        id: '3',
        name: 'Content Strategy Development',
        status: 'paused',
        progress: 45,
        agents: 4,
        startDate: new Date(Date.now() - 86400000 * 5),
        estimatedCompletion: new Date(Date.now() + 86400000 * 7),
        budget: 200,
        spent: 95
      }
    ])

    setRecentActivity([
      {
        id: '1',
        agentName: 'Research Agent',
        action: 'Completed competitor analysis for 15 SaaS platforms',
        timestamp: new Date(Date.now() - 1800000),
        projectId: '1'
      },
      {
        id: '2',
        agentName: 'Copywriter Agent',
        action: 'Generated 3 positioning statement options',
        timestamp: new Date(Date.now() - 3600000),
        projectId: '1'
      },
      {
        id: '3',
        agentName: 'Strategy Agent',
        action: 'Updated project timeline based on new requirements',
        timestamp: new Date(Date.now() - 7200000),
        projectId: '3'
      }
    ])

    setTemplates([
      {
        id: '1',
        name: 'Product Launch Suite',
        description: 'Complete product launch campaign with research, strategy, and content creation',
        category: 'Marketing',
        agents: ['Research Agent', 'Strategy Agent', 'Copywriter Agent', 'Social Media Agent'],
        usageCount: 245,
        rating: 4.8,
        isCustom: false
      },
      {
        id: '2',
        name: 'Market Research Team',
        description: 'Comprehensive market analysis and competitive intelligence gathering',
        category: 'Research',
        agents: ['Research Agent', 'Data Analyst', 'Strategy Agent'],
        usageCount: 189,
        rating: 4.9,
        isCustom: false
      },
      {
        id: '3',
        name: 'Content Creation Hub',
        description: 'Blog posts, social media, and marketing copy generation',
        category: 'Content',
        agents: ['Copywriter Agent', 'Editor Agent', 'Social Media Agent'],
        usageCount: 312,
        rating: 4.7,
        isCustom: true
      }
    ])

    setAnalytics({
      totalProjects: 24,
      activeProjects: 8,
      completedProjects: 16,
      totalAgentHours: 1560,
      averageProjectTime: 3.2,
      successRate: 94.2,
      costEfficiency: 87,
      monthlyGrowth: 12.5,
      topCategories: [
        { name: 'Marketing', count: 8, percentage: 33 },
        { name: 'Product Development', count: 6, percentage: 25 },
        { name: 'Research', count: 5, percentage: 21 },
        { name: 'Content Creation', count: 5, percentage: 21 }
      ]
    })
  }, [])

  const metrics: Metric[] = [
    { label: 'Projects Completed', value: '24', change: '+12%', trend: 'up' },
    { label: 'Active Agents', value: '18', change: '+3', trend: 'up' },
    { label: 'Time Saved', value: '156h', change: '+23%', trend: 'up' },
    { label: 'Cost Efficiency', value: '87%', change: '+5%', trend: 'up' }
  ]

  const handleCreateProject = () => {
    // TODO: Implement project creation logic
    console.log('Creating project:', projectDescription)
    setShowCreateProject(false)
    setProjectDescription('')
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-400 bg-green-500/20'
      case 'completed': return 'text-blue-400 bg-blue-500/20'
      case 'paused': return 'text-yellow-400 bg-yellow-500/20'
      default: return 'text-slate-400 bg-slate-500/20'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active': return <Play className="w-3 h-3" />
      case 'completed': return <CheckCircle className="w-3 h-3" />
      case 'paused': return <Pause className="w-3 h-3" />
      default: return <Clock className="w-3 h-3" />
    }
  }

  return (
    <div className="min-h-screen p-8">
      {/* Main Content */}
      <main className="max-w-7xl mx-auto">
        {/* Header Section */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-5xl font-bold mb-4 bg-gradient-to-r from-pink-500 to-pink-600 text-transparent bg-clip-text">
                Dashboard
              </h2>
              <p className="text-slate-400 text-lg">
                Your command center for AI agent orchestration and project management
              </p>
            </div>
            {activeTab === 'overview' && (
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setShowCreateProject(true)}
                className="px-6 py-3 bg-gradient-to-r from-pink-500 to-pink-600 rounded-xl font-semibold shadow-lg shadow-pink-500/50 hover:shadow-pink-500/70 transition-all flex items-center gap-2"
              >
                <Plus className="w-5 h-5" />
                New Project
              </motion.button>
            )}
          </div>
        </motion.div>

        {/* Navigation Tabs */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-8"
        >
          <div className="flex flex-wrap gap-2 p-2 bg-slate-900/50 backdrop-blur border border-pink-500/20 rounded-2xl">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex-1 min-w-0 px-4 py-3 rounded-xl font-medium transition-all flex items-center justify-center gap-2 ${
                    activeTab === tab.id
                      ? 'bg-gradient-to-r from-pink-500 to-pink-600 text-white shadow-lg shadow-pink-500/30'
                      : 'text-slate-400 hover:text-white hover:bg-slate-800'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span className="hidden sm:inline">{tab.label}</span>
                </button>
              )
            })}
          </div>
        </motion.div>

        {/* Tab Content */}
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          {activeTab === 'overview' && <OverviewTab
            metrics={metrics}
            projects={projects}
            recentActivity={recentActivity}
            showCreateProject={showCreateProject}
            setShowCreateProject={setShowCreateProject}
            projectDescription={projectDescription}
            setProjectDescription={setProjectDescription}
            handleCreateProject={handleCreateProject}
          />}
          {activeTab === 'projects' && <ProjectsTab projects={projects} />}
          {activeTab === 'templates' && <TemplatesTab templates={templates} />}
          {activeTab === 'marketplace' && <MarketplaceTab />}
          {activeTab === 'analytics' && <AnalyticsTab analytics={analytics} />}
          {activeTab === 'team' && <TeamTab />}
          {activeTab === 'learning' && <LearningTab />}
        </motion.div>

      </main>

      {/* Create Project Modal */}
      {showCreateProject && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
          onClick={() => setShowCreateProject(false)}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="bg-slate-900/90 backdrop-blur border border-pink-500/20 rounded-2xl p-8 max-w-2xl w-full"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-start gap-4 mb-6">
              <div className="p-3 bg-pink-500/10 rounded-xl">
                <Sparkles className="w-8 h-8 text-pink-500" />
              </div>
              <div className="flex-1">
                <h3 className="text-2xl font-bold mb-2">Create New Project</h3>
                <p className="text-slate-400">
                  Describe what you want to accomplish and let AI agents handle the execution
                </p>
              </div>
            </div>

            <div className="space-y-4 mb-6">
              <textarea
                value={projectDescription}
                onChange={(e) => setProjectDescription(e.target.value)}
                placeholder="e.g., 'Launch a SaaS product for freelance designers. I need market research, competitor analysis, positioning strategy, website copy, email sequences, social media content, and a launch plan. Timeline: 5 days.'"
                className="w-full h-40 px-4 py-3 bg-slate-900/50 border border-slate-700 rounded-xl focus:border-pink-500/50 focus:ring-2 focus:ring-pink-500/20 outline-none resize-none text-white placeholder:text-slate-500"
              />
            </div>

            <div className="flex gap-3 justify-end">
              <button
                onClick={() => setShowCreateProject(false)}
                className="px-6 py-3 bg-slate-800 border border-slate-700 rounded-xl font-semibold hover:bg-slate-700 transition-all"
              >
                Cancel
              </button>
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={handleCreateProject}
                disabled={!projectDescription.trim()}
                className="px-6 py-3 bg-gradient-to-r from-pink-500 to-pink-600 rounded-xl font-semibold shadow-lg shadow-pink-500/50 hover:shadow-pink-500/70 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                <Sparkles className="w-5 h-5" />
                Create Agent Team
              </motion.button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </div>
  )
}

// Tab Components
function OverviewTab({ metrics, projects, recentActivity, showCreateProject, setShowCreateProject, projectDescription, setProjectDescription, handleCreateProject }: any) {
  return (
    <>
      {/* Metrics Overview */}
      <motion.div
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12"
      >
        {metrics.map((metric: any, index: number) => (
          <motion.div
            key={metric.label}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 + index * 0.1 }}
            className="bg-slate-900/50 backdrop-blur border border-pink-500/20 rounded-2xl p-6 hover:border-pink-500/40 transition-all"
          >
            <div className="flex items-center justify-between mb-4">
              <span className="text-slate-400 text-sm font-medium">{metric.label}</span>
              <TrendingUp className={`w-4 h-4 ${metric.trend === 'up' ? 'text-green-400' : metric.trend === 'down' ? 'text-red-400' : 'text-slate-400'}`} />
            </div>
            <div className="text-3xl font-bold mb-1">{metric.value}</div>
            <div className={`text-sm ${metric.trend === 'up' ? 'text-green-400' : metric.trend === 'down' ? 'text-red-400' : 'text-slate-400'}`}>
              {metric.change} from last month
            </div>
          </motion.div>
        ))}
      </motion.div>

      {/* Main Dashboard Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column - Projects & Quick Actions */}
        <div className="lg:col-span-2 space-y-8">
          {/* Active Projects */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-2xl font-bold">Active Projects</h3>
              <button className="text-pink-400 hover:text-pink-300 transition-colors flex items-center gap-2">
                <Eye className="w-4 h-4" />
                View All
              </button>
            </div>

            <div className="space-y-4">
              {projects.slice(0, 3).map((project: any, index: number) => (
                <motion.div
                  key={project.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.2 + index * 0.1 }}
                  className="bg-slate-900/50 backdrop-blur border border-pink-500/20 rounded-2xl p-6 hover:border-pink-500/40 transition-all cursor-pointer group"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <h4 className="text-xl font-semibold mb-2 group-hover:text-pink-400 transition-colors">
                        {project.name}
                      </h4>
                      <div className="flex items-center gap-4 text-sm text-slate-400 mb-3">
                        <span className="flex items-center gap-1">
                          <Users className="w-4 h-4" />
                          {project.agents} agents
                        </span>
                        <span className="flex items-center gap-1">
                          <DollarSign className="w-4 h-4" />
                          ${project.spent}/${project.budget}
                        </span>
                        <span className={`flex items-center gap-1 px-2 py-1 rounded-full text-xs ${getStatusColor(project.status)}`}>
                          {getStatusIcon(project.status)}
                          {project.status}
                        </span>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-pink-400">{project.progress}%</div>
                      <div className="text-sm text-slate-500">Complete</div>
                    </div>
                  </div>

                  {/* Progress Bar */}
                  <div className="w-full bg-slate-800 rounded-full h-2 mb-4">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${project.progress}%` }}
                      transition={{ duration: 1, delay: index * 0.1 }}
                      className="bg-gradient-to-r from-pink-500 to-pink-600 h-2 rounded-full"
                    />
                  </div>

                  {/* Actions */}
                  <div className="flex gap-2">
                    <button className="flex-1 py-2 bg-slate-800 border border-slate-700 rounded-lg font-medium hover:bg-slate-700 hover:border-pink-500/50 transition-all flex items-center justify-center gap-2">
                      <Settings className="w-4 h-4" />
                      Manage
                    </button>
                    <button className="flex-1 py-2 bg-pink-500/20 border border-pink-500/30 rounded-lg font-medium text-pink-400 hover:bg-pink-500/30 transition-all flex items-center justify-center gap-2">
                      <Activity className="w-4 h-4" />
                      View Live
                    </button>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* Quick Actions */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-slate-900/50 backdrop-blur border border-pink-500/20 rounded-2xl p-6"
          >
            <h3 className="text-xl font-bold mb-4">Quick Actions</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <button className="p-4 bg-slate-800/50 border border-slate-700 rounded-xl hover:border-pink-500/50 transition-all text-left group">
                <div className="flex items-center gap-3 mb-2">
                  <BarChart3 className="w-5 h-5 text-pink-400 group-hover:text-pink-300" />
                  <span className="font-semibold">View Analytics</span>
                </div>
                <p className="text-sm text-slate-400">Performance metrics and ROI tracking</p>
              </button>

              <button className="p-4 bg-slate-800/50 border border-slate-700 rounded-xl hover:border-pink-500/50 transition-all text-left group">
                <div className="flex items-center gap-3 mb-2">
                  <Target className="w-5 h-5 text-pink-400 group-hover:text-pink-300" />
                  <span className="font-semibold">Browse Templates</span>
                </div>
                <p className="text-sm text-slate-400">Pre-built agent configurations</p>
              </button>

              <button className="p-4 bg-slate-800/50 border border-slate-700 rounded-xl hover:border-pink-500/50 transition-all text-left group">
                <div className="flex items-center gap-3 mb-2">
                  <Zap className="w-5 h-5 text-pink-400 group-hover:text-pink-300" />
                  <span className="font-semibold">API Usage</span>
                </div>
                <p className="text-sm text-slate-400">Monitor costs and usage limits</p>
              </button>

              <button className="p-4 bg-slate-800/50 border border-slate-700 rounded-xl hover:border-pink-500/50 transition-all text-left group">
                <div className="flex items-center gap-3 mb-2">
                  <Settings className="w-5 h-5 text-pink-400 group-hover:text-pink-300" />
                  <span className="font-semibold">Settings</span>
                </div>
                <p className="text-sm text-slate-400">Configure preferences and limits</p>
              </button>
            </div>
          </motion.div>
        </div>

        {/* Right Column - Activity Feed & Stats */}
        <div className="space-y-8">
          {/* Recent Activity */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
            className="bg-slate-900/50 backdrop-blur border border-pink-500/20 rounded-2xl p-6"
          >
            <div className="flex items-center gap-3 mb-6">
              <Activity className="w-5 h-5 text-pink-400" />
              <h3 className="text-xl font-bold">Recent Activity</h3>
            </div>

            <div className="space-y-4">
              {recentActivity.map((activity: any, index: number) => (
                <motion.div
                  key={activity.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 + index * 0.1 }}
                  className="flex gap-3 p-3 bg-slate-800/30 rounded-lg hover:bg-slate-800/50 transition-all"
                >
                  <div className="w-2 h-2 bg-pink-500 rounded-full mt-2 flex-shrink-0"></div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-slate-200 truncate">
                      {activity.agentName}
                    </p>
                    <p className="text-xs text-slate-400 mt-1">
                      {activity.action}
                    </p>
                    <p className="text-xs text-slate-500 mt-1">
                      {activity.timestamp.toLocaleTimeString()}
                    </p>
                  </div>
                </motion.div>
              ))}
            </div>

            <button className="w-full mt-4 py-2 text-pink-400 hover:text-pink-300 transition-colors text-sm font-medium flex items-center justify-center gap-2">
              View All Activity
              <ArrowRight className="w-4 h-4" />
            </button>
          </motion.div>

          {/* Performance Summary */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 }}
            className="bg-slate-900/50 backdrop-blur border border-pink-500/20 rounded-2xl p-6"
          >
            <div className="flex items-center gap-3 mb-6">
              <TrendingUp className="w-5 h-5 text-pink-400" />
              <h3 className="text-xl font-bold">Performance</h3>
            </div>

            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-slate-400">Success Rate</span>
                <span className="text-lg font-bold text-pink-400">94.2%</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2">
                <div className="bg-pink-500 h-2 rounded-full" style={{ width: '94.2%' }}></div>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-sm text-slate-400">Avg. Project Time</span>
                <span className="text-lg font-bold text-slate-300">3.2 days</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2">
                <div className="bg-slate-400 h-2 rounded-full" style={{ width: '75%' }}></div>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-sm text-slate-400">Cost Efficiency</span>
                <span className="text-lg font-bold text-pink-400">87%</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2">
                <div className="bg-pink-500 h-2 rounded-full" style={{ width: '87%' }}></div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </>
  )
}

function ProjectsTab({ projects }: any) {
  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h3 className="text-2xl font-bold">All Projects</h3>
        <div className="flex gap-4">
          <select className="bg-slate-900/50 border border-slate-700 rounded-xl px-4 py-2 text-white">
            <option>All Status</option>
            <option>Active</option>
            <option>Completed</option>
            <option>Paused</option>
          </select>
          <button className="px-4 py-2 bg-gradient-to-r from-pink-500 to-pink-600 rounded-xl font-semibold">
            + New Project
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {projects.map((project: any, index: number) => (
          <motion.div
            key={project.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="bg-slate-900/50 backdrop-blur border border-pink-500/20 rounded-2xl p-6 hover:border-pink-500/40 transition-all"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <h4 className="text-xl font-semibold mb-2">{project.name}</h4>
                <div className="flex items-center gap-4 text-sm text-slate-400 mb-3">
                  <span className="flex items-center gap-1">
                    <Users className="w-4 h-4" />
                    {project.agents} agents
                  </span>
                  <span className="flex items-center gap-1">
                    <Calendar className="w-4 h-4" />
                    {project.startDate.toLocaleDateString()}
                  </span>
                </div>
              </div>
              <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(project.status)}`}>
                {project.status}
              </span>
            </div>

            <div className="text-right mb-4">
              <div className="text-2xl font-bold text-pink-400">{project.progress}%</div>
              <div className="text-sm text-slate-500">Complete</div>
            </div>

            <div className="w-full bg-slate-800 rounded-full h-2 mb-4">
              <div className="bg-gradient-to-r from-pink-500 to-pink-600 h-2 rounded-full" style={{ width: `${project.progress}%` }}></div>
            </div>

            <div className="flex gap-2">
              <button className="flex-1 py-2 bg-slate-800 border border-slate-700 rounded-lg font-medium hover:bg-slate-700 transition-all">
                View Details
              </button>
              <button className="flex-1 py-2 bg-pink-500/20 border border-pink-500/30 rounded-lg font-medium text-pink-400 hover:bg-pink-500/30 transition-all">
                Manage
              </button>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}

function TemplatesTab({ templates }: any) {
  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h3 className="text-2xl font-bold">Agent Templates</h3>
        <div className="flex gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              placeholder="Search templates..."
              className="pl-10 pr-4 py-2 bg-slate-900/50 border border-slate-700 rounded-xl text-white placeholder-slate-500"
            />
          </div>
          <button className="px-4 py-2 bg-gradient-to-r from-pink-500 to-pink-600 rounded-xl font-semibold">
            Create Custom
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {templates.map((template: any, index: number) => (
          <motion.div
            key={template.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="bg-slate-900/50 backdrop-blur border border-pink-500/20 rounded-2xl p-6 hover:border-pink-500/40 transition-all"
          >
            <div className="flex items-start justify-between mb-4">
              <div>
                <h4 className="text-lg font-semibold mb-1">{template.name}</h4>
                <p className="text-sm text-slate-400">{template.category}</p>
              </div>
              {template.isCustom && (
                <span className="px-2 py-1 bg-pink-500/20 text-pink-400 text-xs rounded-full">
                  Custom
                </span>
              )}
            </div>

            <p className="text-slate-300 text-sm mb-4 line-clamp-2">{template.description}</p>

            <div className="flex flex-wrap gap-1 mb-4">
              {template.agents.slice(0, 2).map((agent: string) => (
                <span key={agent} className="px-2 py-1 bg-slate-800/50 text-slate-300 text-xs rounded-md">
                  {agent}
                </span>
              ))}
              {template.agents.length > 2 && (
                <span className="px-2 py-1 bg-slate-800/50 text-slate-400 text-xs rounded-md">
                  +{template.agents.length - 2} more
                </span>
              )}
            </div>

            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-1">
                <Star className="w-4 h-4 text-yellow-400 fill-current" />
                <span className="text-sm font-medium">{template.rating}</span>
                <span className="text-sm text-slate-500">({template.usageCount})</span>
              </div>
            </div>

            <button className="w-full py-3 bg-gradient-to-r from-pink-500/20 to-pink-600/20 border border-pink-500/30 rounded-xl font-semibold text-pink-400 hover:from-pink-500 hover:to-pink-600 hover:text-white transition-all">
              Use Template
            </button>
          </motion.div>
        ))}
      </div>
    </div>
  )
}

function MarketplaceTab() {
  return (
    <div className="space-y-8">
      <div className="text-center py-20">
        <ShoppingBag className="w-16 h-16 text-slate-600 mx-auto mb-4" />
        <h3 className="text-2xl font-bold mb-2">Marketplace Coming Soon</h3>
        <p className="text-slate-400">
          Buy and sell custom agent templates from the community
        </p>
      </div>
    </div>
  )
}

function AnalyticsTab({ analytics }: any) {
  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-slate-900/50 backdrop-blur border border-pink-500/20 rounded-2xl p-6">
          <div className="flex items-center gap-3 mb-4">
            <Briefcase className="w-6 h-6 text-pink-400" />
            <span className="text-slate-400 text-sm">Total Projects</span>
          </div>
          <div className="text-3xl font-bold">{analytics.totalProjects}</div>
        </div>

        <div className="bg-slate-900/50 backdrop-blur border border-pink-500/20 rounded-2xl p-6">
          <div className="flex items-center gap-3 mb-4">
            <Activity className="w-6 h-6 text-green-400" />
            <span className="text-slate-400 text-sm">Active Projects</span>
          </div>
          <div className="text-3xl font-bold">{analytics.activeProjects}</div>
        </div>

        <div className="bg-slate-900/50 backdrop-blur border border-pink-500/20 rounded-2xl p-6">
          <div className="flex items-center gap-3 mb-4">
            <CheckCircle className="w-6 h-6 text-blue-400" />
            <span className="text-slate-400 text-sm">Completed</span>
          </div>
          <div className="text-3xl font-bold">{analytics.completedProjects}</div>
        </div>

        <div className="bg-slate-900/50 backdrop-blur border border-pink-500/20 rounded-2xl p-6">
          <div className="flex items-center gap-3 mb-4">
            <Zap className="w-6 h-6 text-yellow-400" />
            <span className="text-slate-400 text-sm">Agent Hours</span>
          </div>
          <div className="text-3xl font-bold">{analytics.totalAgentHours}</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-slate-900/50 backdrop-blur border border-pink-500/20 rounded-2xl p-6">
          <h3 className="text-xl font-bold mb-6">Project Categories</h3>
          <div className="space-y-4">
            {analytics.topCategories.map((category: any, index: number) => (
              <div key={category.name} className="flex items-center justify-between">
                <span className="text-slate-300">{category.name}</span>
                <div className="flex items-center gap-2">
                  <div className="w-24 bg-slate-800 rounded-full h-2">
                    <div
                      className="bg-pink-500 h-2 rounded-full"
                      style={{ width: `${category.percentage}%` }}
                    ></div>
                  </div>
                  <span className="text-sm text-slate-400 w-12 text-right">{category.percentage}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-slate-900/50 backdrop-blur border border-pink-500/20 rounded-2xl p-6">
          <h3 className="text-xl font-bold mb-6">Performance Metrics</h3>
          <div className="space-y-6">
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-slate-400">Success Rate</span>
                <span className="text-pink-400 font-semibold">{analytics.successRate}%</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2">
                <div className="bg-pink-500 h-2 rounded-full" style={{ width: `${analytics.successRate}%` }}></div>
              </div>
            </div>

            <div>
              <div className="flex justify-between mb-2">
                <span className="text-slate-400">Avg Project Time</span>
                <span className="text-slate-300 font-semibold">{analytics.averageProjectTime} days</span>
              </div>
            </div>

            <div>
              <div className="flex justify-between mb-2">
                <span className="text-slate-400">Cost Efficiency</span>
                <span className="text-pink-400 font-semibold">{analytics.costEfficiency}%</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2">
                <div className="bg-pink-500 h-2 rounded-full" style={{ width: `${analytics.costEfficiency}%` }}></div>
              </div>
            </div>

            <div>
              <div className="flex justify-between mb-2">
                <span className="text-slate-400">Monthly Growth</span>
                <span className="text-green-400 font-semibold">+{analytics.monthlyGrowth}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function TeamTab() {
  return (
    <div className="space-y-8">
      <div className="text-center py-20">
        <Users className="w-16 h-16 text-slate-600 mx-auto mb-4" />
        <h3 className="text-2xl font-bold mb-2">Team Collaboration</h3>
        <p className="text-slate-400">
          Invite team members and manage collaborative projects
        </p>
        <button className="mt-6 px-6 py-3 bg-gradient-to-r from-pink-500 to-pink-600 rounded-xl font-semibold">
          Invite Team Members
        </button>
      </div>
    </div>
  )
}

function LearningTab() {
  return (
    <div className="space-y-8">
      <div className="text-center py-20">
        <BookOpen className="w-16 h-16 text-slate-600 mx-auto mb-4" />
        <h3 className="text-2xl font-bold mb-2">AI Learning Hub</h3>
        <p className="text-slate-400">
          Discover insights and best practices from your agent teams
        </p>
      </div>
    </div>
  )
}

// Helper functions
function getStatusColor(status: string) {
  switch (status) {
    case 'active': return 'bg-green-500/20 text-green-400'
    case 'completed': return 'bg-blue-500/20 text-blue-400'
    case 'paused': return 'bg-yellow-500/20 text-yellow-400'
    default: return 'bg-slate-500/20 text-slate-400'
  }
}

function getStatusIcon(status: string) {
  switch (status) {
    case 'active': return <Play className="w-3 h-3" />
    case 'completed': return <CheckCircle className="w-3 h-3" />
    case 'paused': return <Pause className="w-3 h-3" />
    default: return <Clock className="w-3 h-3" />
  }
}
