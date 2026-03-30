/* eslint-disable react/no-unescaped-entities */
'use client'

import { motion } from 'framer-motion'
import {
  Search,
  Filter,
  Star,
  Download,
  Cpu,
  Zap,
  BarChart3,
  MessageSquare,
  FileText,
  Palette,
  Megaphone,
  Calculator,
  Sparkles,
  ArrowRight,
  Heart,
  ShoppingCart
} from 'lucide-react'
import Link from 'next/link'
import { useState } from 'react'
import ThemeToggle from '@/components/ThemeToggle'

export default function MarketplacePage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')

  const categories = [
    { id: 'all', name: 'All Templates', icon: Sparkles },
    { id: 'marketing', name: 'Marketing', icon: Megaphone },
    { id: 'analytics', name: 'Analytics', icon: BarChart3 },
    { id: 'content', name: 'Content', icon: FileText },
    { id: 'sales', name: 'Sales', icon: Calculator },
    { id: 'design', name: 'Design', icon: Palette },
    { id: 'communication', name: 'Communication', icon: MessageSquare }
  ]

  const templates = [
    {
      id: 1,
      name: 'Content Marketing Agent',
      description: 'Creates compelling blog posts, social media content, and marketing copy optimized for engagement.',
      category: 'marketing',
      rating: 4.8,
      downloads: 1250,
      price: 'Free',
      author: 'Namakan Team',
      tags: ['Content Creation', 'SEO', 'Social Media'],
      icon: FileText,
      featured: true
    },
    {
      id: 2,
      name: 'Data Analysis Agent',
      description: 'Analyzes datasets, generates insights, creates visualizations, and produces comprehensive reports.',
      category: 'analytics',
      rating: 4.9,
      downloads: 890,
      price: '$29',
      author: 'Analytics Pro',
      tags: ['Data Science', 'Visualization', 'Reporting'],
      icon: BarChart3,
      featured: true
    },
    {
      id: 3,
      name: 'Customer Support Agent',
      description: 'Handles customer inquiries, provides instant responses, and escalates complex issues.',
      category: 'communication',
      rating: 4.7,
      downloads: 2100,
      price: 'Free',
      author: 'SupportAI',
      tags: ['Customer Service', 'Chatbots', 'Support'],
      icon: MessageSquare,
      featured: false
    },
    {
      id: 4,
      name: 'Sales Lead Generator',
      description: 'Identifies prospects, qualifies leads, and creates personalized outreach sequences.',
      category: 'sales',
      rating: 4.6,
      downloads: 675,
      price: '$49',
      author: 'SalesForce AI',
      tags: ['Lead Generation', 'CRM', 'Outreach'],
      icon: Calculator,
      featured: false
    },
    {
      id: 5,
      name: 'UI/UX Design Agent',
      description: 'Creates wireframes, mockups, and design systems for web and mobile applications.',
      category: 'design',
      rating: 4.8,
      downloads: 445,
      price: '$39',
      author: 'DesignStudio',
      tags: ['UI/UX', 'Wireframes', 'Prototyping'],
      icon: Palette,
      featured: true
    },
    {
      id: 6,
      name: 'Code Review Agent',
      description: 'Reviews code for bugs, security issues, and best practices with detailed feedback.',
      category: 'development',
      rating: 4.9,
      downloads: 1200,
      price: 'Free',
      author: 'DevTools AI',
      tags: ['Code Review', 'Security', 'Best Practices'],
      icon: Cpu,
      featured: false
    }
  ]

  const filteredTemplates = templates.filter(template => {
    const matchesSearch = template.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         template.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         template.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))
    const matchesCategory = selectedCategory === 'all' || template.category === selectedCategory
    return matchesSearch && matchesCategory
  })

  return (
    <main className="min-h-screen bg-white dark:bg-slate-950 text-slate-900 dark:text-white">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 dark:bg-slate-950/80 backdrop-blur-xl border-b border-slate-200 dark:border-slate-800">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-12">
              <Link href="/" className="text-2xl font-bold bg-gradient-to-r to-teal-500 to-teal-600 text-transparent bg-clip-text">
                Namakan
              </Link>
              <div className="hidden md:flex items-center gap-8">
                <Link href="/solutions" className="text-slate-600 dark:text-slate-300 hover:text-teal-500 transition-colors">
                  Solutions
                </Link>
                <Link href="/pricing" className="text-slate-600 dark:text-slate-300 hover:text-teal-500 transition-colors">
                  Pricing
                </Link>
                <Link href="/resources" className="text-slate-600 dark:text-slate-300 hover:text-teal-500 transition-colors">
                  Resources
                </Link>
                <Link href="/templates" className="text-slate-600 dark:text-slate-300 hover:text-teal-500 transition-colors font-medium">
                  Marketplace
                </Link>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <ThemeToggle />
              <Link href="/auth/login" className="text-slate-600 dark:text-slate-300 hover:text-teal-500 transition-colors font-medium">
                Log in
              </Link>
              <Link href="/auth/signup">
                <button className="px-6 py-2.5 bg-gradient-to-r to-teal-500 to-teal-600 rounded-lg font-semibold hover:shadow-lg hover:shadow-teal-500/30 transition-all">
                  Start for free
                </button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 px-6 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-teal-50 via-white to-slate-50 dark:from-slate-950 dark:via-slate-900 dark:to-slate-950" />
        <motion.div
          animate={{
            background: [
              'radial-gradient(circle at 20% 50%, rgba(244, 63, 94, 0.1) 0%, transparent 50%)',
              'radial-gradient(circle at 80% 50%, rgba(244, 63, 94, 0.08) 0%, transparent 50%)',
              'radial-gradient(circle at 20% 50%, rgba(244, 63, 94, 0.1) 0%, transparent 50%)',
            ]
          }}
          transition={{ duration: 10, repeat: Infinity }}
          className="absolute inset-0"
        />

        <div className="relative z-10 container mx-auto max-w-4xl">
          <div className="text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="inline-flex items-center gap-2 mb-6 px-4 py-2 bg-teal-100 dark:bg-teal-500/10 border border-teal-200 dark:border-teal-500/30 rounded-full text-teal-600 dark:text-teal-400 text-sm font-semibold"
            >
              <Sparkles className="w-4 h-4" />
              Agent Marketplace
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="text-5xl md:text-7xl font-bold mb-6 leading-tight"
            >
              Pre-built
              <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r to-teal-500 via-teal-600 to-teal-500">
                AI Agents
              </span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="text-xl md:text-2xl text-slate-600 dark:text-slate-300 mb-8 max-w-2xl mx-auto"
            >
              Browse, download, and customize ready-to-use AI agent templates.
              Get started instantly with proven workflows.
            </motion.p>

            {/* Search Bar */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="max-w-2xl mx-auto mb-8"
            >
              <div className="relative">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input
                  type="text"
                  placeholder="Search agents, templates, or tags..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-12 pr-4 py-4 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl text-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent shadow-lg"
                />
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Categories */}
      <section className="pb-8 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="flex flex-wrap gap-3 justify-center">
            {categories.map((category) => (
              <button
                key={category.id}
                onClick={() => setSelectedCategory(category.id)}
                className={`px-4 py-2 rounded-lg font-medium transition-all flex items-center gap-2 ${
                  selectedCategory === category.id
                    ? 'bg-teal-500 text-white shadow-lg shadow-teal-500/30'
                    : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700'
                }`}
              >
                <category.icon className="w-4 h-4" />
                {category.name}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Templates Grid */}
      <section className="pb-20 px-6">
        <div className="container mx-auto max-w-7xl">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredTemplates.map((template, index) => (
              <motion.div
                key={template.id}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.05 }}
                className={`bg-white dark:bg-slate-900 border rounded-xl p-6 hover:border-teal-500/50 transition-all group ${
                  template.featured
                    ? 'border-teal-500/50 shadow-lg shadow-teal-500/20'
                    : 'border-slate-200 dark:border-slate-800'
                }`}
              >
                {template.featured && (
                  <div className="inline-flex items-center gap-1 px-2 py-1 bg-teal-100 dark:bg-teal-500/20 text-teal-600 dark:text-teal-400 text-xs font-semibold rounded-full mb-3">
                    <Star className="w-3 h-3" />
                    Featured
                  </div>
                )}

                <div className="flex items-start gap-4 mb-4">
                  <div className="w-12 h-12 bg-gradient-to-br to-teal-500 to-teal-600 rounded-lg flex items-center justify-center flex-shrink-0">
                    <template.icon className="w-6 h-6 text-white" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="font-bold text-lg mb-1 text-slate-900 dark:text-white truncate">
                      {template.name}
                    </h3>
                    <p className="text-sm text-slate-500 dark:text-slate-400">
                      by {template.author}
                    </p>
                  </div>
                </div>

                <p className="text-slate-600 dark:text-slate-400 mb-4 text-sm leading-relaxed">
                  {template.description}
                </p>

                <div className="flex flex-wrap gap-1 mb-4">
                  {template.tags.map((tag) => (
                    <span
                      key={tag}
                      className="px-2 py-1 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 text-xs rounded-md"
                    >
                      {tag}
                    </span>
                  ))}
                </div>

                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-1">
                    <Star className="w-4 h-4 text-yellow-400 fill-current" />
                    <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                      {template.rating}
                    </span>
                    <span className="text-sm text-slate-500 dark:text-slate-400">
                      ({template.downloads})
                    </span>
                  </div>
                  <span className={`font-bold ${
                    template.price === 'Free'
                      ? 'text-green-600 dark:text-green-400'
                      : 'text-slate-900 dark:text-white'
                  }`}>
                    {template.price}
                  </span>
                </div>

                <div className="flex gap-2">
                  <button className="flex-1 px-4 py-2 bg-gradient-to-r to-teal-500 to-teal-600 text-white rounded-lg font-medium hover:shadow-lg hover:shadow-teal-500/30 transition-all flex items-center justify-center gap-2">
                    <Download className="w-4 h-4" />
                    Get Template
                  </button>
                  <button className="p-2 text-slate-400 hover:text-teal-500 transition-colors">
                    <Heart className="w-5 h-5" />
                  </button>
                </div>
              </motion.div>
            ))}
          </div>

          {filteredTemplates.length === 0 && (
            <div className="text-center py-12">
              <Search className="w-12 h-12 text-slate-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-slate-600 dark:text-slate-400 mb-2">
                No templates found
              </h3>
              <p className="text-slate-500 dark:text-slate-500">
                Try adjusting your search or browse different categories.
              </p>
            </div>
          )}
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-6 bg-gradient-to-r to-teal-500 to-teal-600">
        <div className="container mx-auto max-w-4xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6 text-white">
              Can't Find What You Need?
            </h2>
            <p className="text-xl text-teal-100 mb-8 max-w-2xl mx-auto">
              Build custom AI agents tailored to your specific needs, or contribute your own templates to the community.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/auth/signup">
                <button className="px-8 py-4 bg-white text-teal-600 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transition-all flex items-center gap-2">
                  <Sparkles className="w-5 h-5" />
                  Create Custom Agent
                </button>
              </Link>
              <Link href="/contact">
                <button className="px-8 py-4 bg-teal-600/20 text-white border border-white/30 rounded-xl font-bold text-lg hover:bg-teal-600/30 transition-all">
                  Request Template
                </button>
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-200 dark:border-slate-800 py-16 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="grid grid-cols-2 md:grid-cols-5 gap-8 mb-12">
            <div className="col-span-2">
              <h4 className="text-2xl font-bold bg-gradient-to-r to-teal-500 to-teal-600 text-transparent bg-clip-text mb-4">
                Namakan
              </h4>
              <p className="text-slate-600 dark:text-slate-400 mb-4">
                AI agent orchestration for the future of work
              </p>
            </div>

            <div>
              <h5 className="font-bold mb-4 text-slate-900 dark:text-white">Solutions</h5>
              <ul className="space-y-2 text-slate-600 dark:text-slate-400">
                <li><Link href="/start" className="hover:text-teal-500 transition-colors">Start your project</Link></li>
                <li><Link href="/templates" className="hover:text-teal-500 transition-colors font-medium">Agent templates</Link></li>
                <li><Link href="/templates" className="hover:text-teal-500 transition-colors">Templates</Link></li>
              </ul>
            </div>

            <div>
              <h5 className="font-bold mb-4 text-slate-900 dark:text-white">Resources</h5>
              <ul className="space-y-2 text-slate-600 dark:text-slate-400">
                <li><Link href="/docs" className="hover:text-teal-500 transition-colors">Documentation</Link></li>
                <li><Link href="/blog" className="hover:text-teal-500 transition-colors">Blog</Link></li>
                <li><Link href="/guides" className="hover:text-teal-500 transition-colors">Guides</Link></li>
                <li><Link href="/api" className="hover:text-teal-500 transition-colors">API Reference</Link></li>
              </ul>
            </div>

            <div>
              <h5 className="font-bold mb-4 text-slate-900 dark:text-white">Company</h5>
              <ul className="space-y-2 text-slate-600 dark:text-slate-400">
                <li><Link href="/about" className="hover:text-teal-500 transition-colors">About</Link></li>
                <li><Link href="/careers" className="hover:text-teal-500 transition-colors">Careers</Link></li>
                <li><Link href="/contact" className="hover:text-teal-500 transition-colors">Contact</Link></li>
                <li><Link href="/privacy" className="hover:text-teal-500 transition-colors">Privacy</Link></li>
                <li><Link href="/terms" className="hover:text-teal-500 transition-colors">Terms</Link></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-slate-200 dark:border-slate-800 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-slate-500 dark:text-slate-400 text-sm">
              &copy; 2026 Namakan. All rights reserved.
            </p>
            <div className="flex items-center gap-6 text-sm text-slate-500 dark:text-slate-400">
              <Link href="/status" className="hover:text-teal-500 transition-colors">Service Status</Link>
              <Link href="/security" className="hover:text-teal-500 transition-colors">Security</Link>
            </div>
          </div>
        </div>
      </footer>
    </main>
  )
}