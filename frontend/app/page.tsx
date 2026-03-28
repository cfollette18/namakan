'use client'

import { motion, AnimatePresence } from 'framer-motion'
import {
  Sparkles,
  Cpu,
  Rocket,
  BarChart3,
  ShieldCheck,
  Zap,
  Users,
  Code,
  Check,
  ArrowRight,
  Play,
  FlaskConical,
  Lightbulb,
  Database
} from 'lucide-react'
import Link from 'next/link'
import { useState, useEffect } from 'react'

export default function Home() {
  const [currentPhrase, setCurrentPhrase] = useState(0)

  const rotatingPhrases = [
    "next big thing",
    "one to watch",
    "category creator", 
    "unicorn startup",
    "industry leader",
    "game changer",
    "market innovator"
  ]

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentPhrase((prev) => (prev + 1) % rotatingPhrases.length)
    }, 2500)
    return () => clearInterval(interval)
  }, [])

  const showcaseProjects = [
    { name: "Research Agent", domain: "research.namakan.ai" },
    { name: "Content Creator", domain: "content.namakan.ai" },
    { name: "Code Reviewer", domain: "code.namakan.ai" },
    { name: "Marketing Team", domain: "marketing.namakan.ai" },
    { name: "Data Analyst", domain: "data.namakan.ai" },
    { name: "Strategy Planner", domain: "strategy.namakan.ai" },
  ]

  const successStories = [
    {
      company: "TechStartup Inc",
      result: "Reduced time-to-market by 70%",
      quote: "Namakan's AI agents helped us ship features 3x faster than our competitors."
    },
    {
      company: "Marketing Agency Pro",
      result: "10x content output",
      quote: "We went from 5 campaigns per month to 50, maintaining the same quality standards."
    },
    {
      company: "Enterprise Solutions",
      result: "$2M saved annually",
      quote: "The agent teams handle tasks that would require 15 full-time employees."
    }
  ]

  const capabilities = [
    {
      title: "Build & Deploy",
      items: ["Create agent teams", "Define workflows", "Deploy instantly", "Scale automatically"]
    },
    {
      title: "Collaborate & Share",
      items: ["Team workspaces", "Agent marketplace", "Cross-project agents", "Real-time updates"]
    },
    {
      title: "Monitor & Learn",
      items: ["Live dashboards", "Performance metrics", "Continuous learning", "Quality insights"]
    }
  ]

  return (
    <main className="min-h-screen bg-white dark:bg-slate-950 text-slate-900 dark:text-white">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 dark:bg-slate-950/80 backdrop-blur-xl border-b border-slate-200 dark:border-slate-800">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-12">
              <Link href="/" className="text-2xl font-bold bg-gradient-to-r from-pink-500 to-pink-600 text-transparent bg-clip-text">
                Namakan
              </Link>
              <div className="hidden md:flex items-center gap-8">
                <Link href="/solutions" className="text-slate-600 dark:text-slate-300 hover:text-pink-500 transition-colors">
                  Solutions
                </Link>
                <Link href="/pricing" className="text-slate-600 dark:text-slate-300 hover:text-pink-500 transition-colors">
                  Pricing
                </Link>
                <Link href="/resources" className="text-slate-600 dark:text-slate-300 hover:text-pink-500 transition-colors">
                  Resources
                </Link>
                <Link href="/templates" className="text-slate-600 dark:text-slate-300 hover:text-pink-500 transition-colors">
                  Marketplace
                </Link>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <Link href="/auth/login" className="text-slate-600 dark:text-slate-300 hover:text-pink-500 transition-colors font-medium">
                Log in
              </Link>
              <Link href="/auth/signup">
                <button className="px-6 py-2.5 bg-gradient-to-r from-pink-500 to-pink-600 rounded-lg font-semibold hover:shadow-lg hover:shadow-pink-500/30 transition-all">
                  Start for free
                </button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 px-6 overflow-hidden">
        {/* Animated Background */}
        <div className="absolute inset-0 bg-gradient-to-br from-pink-50 via-white to-slate-50 dark:from-slate-950 dark:via-slate-900 dark:to-slate-950" />
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
        
        <div className="relative z-10 container mx-auto max-w-7xl">
          <div className="text-center">
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="inline-flex items-center gap-2 mb-8 px-4 py-2 bg-pink-100 dark:bg-pink-500/10 border border-pink-200 dark:border-pink-500/30 rounded-full text-pink-600 dark:text-pink-400 text-sm font-semibold"
            >
              <Sparkles className="w-4 h-4" />
              The Future of Work is Autonomous
            </motion.div>

            {/* Main Headline with Rotating Text */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="mb-8"
            >
              <h1 className="text-6xl md:text-8xl font-bold mb-4 leading-tight">
                Be the
              </h1>
              <div className="h-[100px] md:h-[140px] overflow-hidden">
                <AnimatePresence mode="wait">
                  <motion.h2
                    key={currentPhrase}
                    initial={{ y: 100, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    exit={{ y: -100, opacity: 0 }}
                    transition={{ duration: 0.5 }}
                    className="text-6xl md:text-8xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-500 via-pink-600 to-pink-500 bg-[length:200%_auto]"
                  >
                    {rotatingPhrases[currentPhrase]}
                  </motion.h2>
                </AnimatePresence>
              </div>
            </motion.div>

            {/* Subheadline */}
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="text-xl md:text-2xl text-slate-600 dark:text-slate-300 mb-10 max-w-3xl mx-auto leading-relaxed"
            >
              Build fast, scale far, and grow exponentially with autonomous AI agent teams that work 24/7
            </motion.p>

            {/* CTA Buttons */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12"
            >
              <Link href="/auth/signup">
                <button className="px-8 py-4 bg-gradient-to-r from-pink-500 to-pink-600 rounded-xl font-bold text-lg shadow-lg shadow-pink-500/30 hover:shadow-xl hover:shadow-pink-500/40 transition-all flex items-center gap-2">
                  Start for free
                  <ArrowRight className="w-5 h-5" />
                </button>
              </Link>
              
              <button className="px-8 py-4 bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white rounded-xl font-bold text-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-all flex items-center gap-2">
                <Play className="w-5 h-5" />
                Watch Demo
              </button>
            </motion.div>

            {/* Trust Indicators */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4 }}
              className="flex flex-wrap items-center justify-center gap-6 text-sm text-slate-500 dark:text-slate-400"
            >
              <div className="flex items-center gap-2">
                <Check className="w-5 h-5 text-green-500" />
                No credit card required
              </div>
              <div className="flex items-center gap-2">
                <Check className="w-5 h-5 text-green-500" />
                5 free projects included
              </div>
              <div className="flex items-center gap-2">
                <Check className="w-5 h-5 text-green-500" />
                Setup in under 2 minutes
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Showcase Carousel Section */}
      <section className="py-16 px-6 bg-slate-50 dark:bg-slate-900/50">
        <div className="container mx-auto">
          <motion.p
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center text-sm font-semibold text-slate-500 dark:text-slate-400 mb-8 uppercase tracking-wider"
          >
            Powered by cutting-edge AI orchestration
          </motion.p>
          
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {showcaseProjects.map((project, index) => (
              <motion.div
                key={project.domain}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.05 }}
                className="p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl hover:border-pink-500/50 transition-all group cursor-pointer"
              >
                <div className="text-center">
                  <div className="w-12 h-12 mx-auto mb-3 bg-gradient-to-br from-pink-500 to-pink-600 rounded-lg flex items-center justify-center">
                    <Cpu className="w-6 h-6 text-white" />
                  </div>
                  <h4 className="font-semibold text-sm mb-1 text-slate-900 dark:text-white">{project.name}</h4>
                  <p className="text-xs text-slate-500 dark:text-slate-400">{project.domain}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 px-6 bg-gradient-to-b from-white to-slate-50 dark:from-slate-950 dark:to-slate-900">
        <div className="container mx-auto max-w-6xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              For everyone from solopreneurs to enterprise
            </h2>
            <p className="text-xl text-slate-600 dark:text-slate-300">
              Teams of every size have collectively saved over 10 million hours using Namakan
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-20">
            {successStories.map((story, index) => (
              <motion.div
                key={story.company}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="p-8 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl"
              >
                <h4 className="font-bold text-lg mb-2 text-slate-900 dark:text-white">{story.result}</h4>
                <p className="text-slate-600 dark:text-slate-400 mb-4 italic">"{story.quote}"</p>
                <p className="text-sm font-semibold text-pink-500">{story.company}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Capabilities Grid */}
      <section className="py-20 px-6">
        <div className="container mx-auto max-w-6xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              The complete AI agent platform
            </h2>
            <p className="text-xl text-slate-600 dark:text-slate-300">
              Build, deploy, and scale your AI workforce
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {capabilities.map((capability, index) => (
              <motion.div
                key={capability.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="p-8 bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-800 rounded-2xl"
              >
                <h3 className="text-2xl font-bold mb-6 text-slate-900 dark:text-white">{capability.title}</h3>
                <ul className="space-y-3">
                  {capability.items.map((item) => (
                    <li key={item} className="flex items-center gap-3 text-slate-600 dark:text-slate-300">
                      <Check className="w-5 h-5 text-pink-500 flex-shrink-0" />
                      {item}
                    </li>
                  ))}
                </ul>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Feature Showcase */}
      <section className="py-20 px-6 bg-slate-50 dark:bg-slate-900/30">
        <div className="container mx-auto max-w-6xl">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center mb-20">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
            >
              <h3 className="text-3xl md:text-4xl font-bold mb-4">
                Multi-agent orchestration that just works
              </h3>
              <p className="text-lg text-slate-600 dark:text-slate-300 mb-6">
                Create coordinated teams of specialized AI agents that collaborate like a real organization. From research to execution, your agents handle it all.
              </p>
              <ul className="space-y-3 mb-6">
                <li className="flex items-start gap-3">
                  <Check className="w-6 h-6 text-pink-500 flex-shrink-0 mt-1" />
                  <span className="text-slate-600 dark:text-slate-300">
                    <strong className="text-slate-900 dark:text-white">Intelligent routing:</strong> Tasks automatically assigned to the best agent
                  </span>
                </li>
                <li className="flex items-start gap-3">
                  <Check className="w-6 h-6 text-pink-500 flex-shrink-0 mt-1" />
                  <span className="text-slate-600 dark:text-slate-300">
                    <strong className="text-slate-900 dark:text-white">Real-time collaboration:</strong> Agents share context and learn from each other
                  </span>
                </li>
                <li className="flex items-start gap-3">
                  <Check className="w-6 h-6 text-pink-500 flex-shrink-0 mt-1" />
                  <span className="text-slate-600 dark:text-slate-300">
                    <strong className="text-slate-900 dark:text-white">Human oversight:</strong> Review and approve at every checkpoint
                  </span>
                </li>
              </ul>
              <Link href="/features/orchestration">
                <button className="text-pink-500 font-semibold flex items-center gap-2 hover:gap-3 transition-all">
                  Learn more about orchestration
                  <ArrowRight className="w-5 h-5" />
                </button>
              </Link>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="relative"
            >
              <div className="aspect-square bg-gradient-to-br from-pink-500/20 to-pink-600/20 rounded-3xl border border-slate-200 dark:border-slate-700 p-8 flex items-center justify-center">
                <div className="text-center">
                  <Cpu className="w-24 h-24 text-pink-500 mx-auto mb-4" />
                  <p className="text-slate-600 dark:text-slate-400">Interactive Demo Placeholder</p>
                </div>
              </div>
            </motion.div>
          </div>

          {/* Additional Features */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: Zap,
                title: "Lightning fast setup",
                description: "From idea to execution in minutes. Just describe your goal and watch your agent team get to work."
              },
              {
                icon: BarChart3,
                title: "Continuous learning",
                description: "Every project makes your agents smarter. Personal and collective intelligence that compounds."
              },
              {
                icon: ShieldCheck,
                title: "Enterprise security",
                description: "SOC 2 compliant with end-to-end encryption. Your data stays private and secure."
              },
              {
                icon: Users,
                title: "Team collaboration",
                description: "Share agents across teams. Let your best agents work on multiple projects simultaneously."
              },
              {
                icon: FlaskConical,
                title: "Agent marketplace",
                description: "Discover and share specialized agent templates from the community."
              },
              {
                icon: Database,
                title: "Unlimited scale",
                description: "Handle projects of any size. From simple tasks to complex multi-week initiatives."
              }
            ].map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.05 }}
                className="p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl hover:border-pink-500/50 transition-all group"
              >
                <feature.icon className="w-12 h-12 text-pink-500 mb-4 group-hover:scale-110 transition-transform" />
                <h4 className="text-lg font-bold mb-2 text-slate-900 dark:text-white">{feature.title}</h4>
                <p className="text-slate-600 dark:text-slate-400">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Metrics Section */}
      <section className="py-20 px-6 bg-gradient-to-r from-pink-500 to-pink-600 text-white">
        <div className="container mx-auto max-w-6xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              There's no better platform to build with AI
            </h2>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center"
            >
              <div className="text-5xl md:text-6xl font-bold mb-2">10M+</div>
              <div className="text-xl opacity-90">Hours saved</div>
              <p className="text-sm opacity-75 mt-2">Namakan agents have automated millions of hours of work</p>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1 }}
              className="text-center"
            >
              <div className="text-5xl md:text-6xl font-bold mb-2">99.9%</div>
              <div className="text-xl opacity-90">Uptime</div>
              <p className="text-sm opacity-75 mt-2">Enterprise-grade reliability you can count on</p>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 }}
              className="text-center"
            >
              <div className="text-5xl md:text-6xl font-bold mb-2">50K+</div>
              <div className="text-xl opacity-90">Active agents</div>
              <p className="text-sm opacity-75 mt-2">Thousands of specialized agents working right now</p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="py-20 px-6">
        <div className="container mx-auto max-w-6xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Pick a plan that fits
            </h2>
            <p className="text-xl text-slate-600 dark:text-slate-300">
              Start free, scale as you grow
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                name: "Starter",
                price: "Free",
                description: "Perfect for trying out Namakan",
                features: [
                  "5 projects per month",
                  "Basic agent templates",
                  "Community support",
                  "Public marketplace access"
                ]
              },
              {
                name: "Pro",
                price: "$49",
                period: "/month",
                description: "For professionals and small teams",
                features: [
                  "Unlimited projects",
                  "All agent templates",
                  "Priority support",
                  "Custom agent training",
                  "Private agents",
                  "Advanced analytics"
                ],
                popular: true
              },
              {
                name: "Enterprise",
                price: "Custom",
                description: "For large organizations",
                features: [
                  "Everything in Pro",
                  "Dedicated infrastructure",
                  "SLA guarantees",
                  "Custom integrations",
                  "Team collaboration",
                  "SOC 2 compliance"
                ]
              }
            ].map((tier, index) => (
              <motion.div
                key={tier.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className={`p-8 rounded-2xl border relative ${
                  tier.popular
                    ? 'bg-gradient-to-b from-pink-50 to-white dark:from-pink-500/10 dark:to-slate-900 border-pink-500 shadow-xl scale-105'
                    : 'bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800'
                }`}
              >
                {tier.popular && (
                  <div className="absolute -top-4 left-1/2 -translate-x-1/2 px-4 py-1 bg-pink-500 rounded-full text-white text-sm font-bold">
                    Most Popular
                  </div>
                )}
                <h3 className="text-2xl font-bold mb-2 text-slate-900 dark:text-white">{tier.name}</h3>
                <div className="mb-4">
                  <span className="text-5xl font-bold text-slate-900 dark:text-white">{tier.price}</span>
                  {tier.period && <span className="text-slate-600 dark:text-slate-400">{tier.period}</span>}
                </div>
                <p className="text-slate-600 dark:text-slate-400 mb-6">{tier.description}</p>
                <ul className="space-y-3 mb-8">
                  {tier.features.map((feature) => (
                    <li key={feature} className="flex items-start gap-3">
                      <Check className="w-5 h-5 text-pink-500 flex-shrink-0 mt-0.5" />
                      <span className="text-slate-600 dark:text-slate-300">{feature}</span>
                    </li>
                  ))}
                </ul>
                <Link href="/auth/signup">
                  <button className={`w-full py-4 rounded-xl font-bold transition-all ${
                    tier.popular
                      ? 'bg-gradient-to-r from-pink-500 to-pink-600 text-white hover:shadow-lg hover:shadow-pink-500/30'
                      : 'bg-slate-900 dark:bg-slate-800 text-white hover:bg-slate-800 dark:hover:bg-slate-700'
                  }`}>
                    Get Started
                  </button>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-20 px-6 bg-slate-50 dark:bg-slate-900/30">
        <div className="container mx-auto max-w-4xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center bg-gradient-to-r from-pink-500/10 to-purple-500/10 border border-pink-500/30 rounded-3xl p-12"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Take your shot
            </h2>
            <p className="text-xl text-slate-600 dark:text-slate-300 mb-8">
              Join thousands of teams building the future with AI agents
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/auth/signup">
                <button className="px-8 py-4 bg-gradient-to-r from-pink-500 to-pink-600 rounded-xl font-bold text-lg shadow-lg shadow-pink-500/30 hover:shadow-xl hover:shadow-pink-500/40 transition-all">
                  Start for free
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
              <h4 className="text-2xl font-bold bg-gradient-to-r from-pink-500 to-pink-600 text-transparent bg-clip-text mb-4">
                Namakan
              </h4>
              <p className="text-slate-600 dark:text-slate-400 mb-4">
                Build anything with autonomous AI agent teams
              </p>
            </div>
            
            <div>
              <h5 className="font-bold mb-4 text-slate-900 dark:text-white">Solutions</h5>
              <ul className="space-y-2 text-slate-600 dark:text-slate-400">
                <li><Link href="/start" className="hover:text-pink-500 transition-colors">Start your project</Link></li>
                <li><Link href="/templates" className="hover:text-pink-500 transition-colors">Agent templates</Link></li>
                <li><Link href="/templates" className="hover:text-pink-500 transition-colors">Templates</Link></li>
              </ul>
            </div>
            
            <div>
              <h5 className="font-bold mb-4 text-slate-900 dark:text-white">Resources</h5>
              <ul className="space-y-2 text-slate-600 dark:text-slate-400">
                <li><Link href="/docs" className="hover:text-pink-500 transition-colors">Documentation</Link></li>
                <li><Link href="/blog" className="hover:text-pink-500 transition-colors">Blog</Link></li>
                <li><Link href="/guides" className="hover:text-pink-500 transition-colors">Guides</Link></li>
                <li><Link href="/api" className="hover:text-pink-500 transition-colors">API Reference</Link></li>
              </ul>
            </div>
            
            <div>
              <h5 className="font-bold mb-4 text-slate-900 dark:text-white">Company</h5>
              <ul className="space-y-2 text-slate-600 dark:text-slate-400">
                <li><Link href="/about" className="hover:text-pink-500 transition-colors">About</Link></li>
                <li><Link href="/careers" className="hover:text-pink-500 transition-colors">Careers</Link></li>
                <li><Link href="/contact" className="hover:text-pink-500 transition-colors">Contact</Link></li>
                <li><Link href="/privacy" className="hover:text-pink-500 transition-colors">Privacy</Link></li>
                <li><Link href="/terms" className="hover:text-pink-500 transition-colors">Terms</Link></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-slate-200 dark:border-slate-800 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-slate-500 dark:text-slate-400 text-sm">
              &copy; 2026 Namakan. All rights reserved.
            </p>
            <div className="flex items-center gap-6 text-sm text-slate-500 dark:text-slate-400">
              <Link href="/status" className="hover:text-pink-500 transition-colors">Service Status</Link>
              <Link href="/security" className="hover:text-pink-500 transition-colors">Security</Link>
            </div>
          </div>
        </div>
      </footer>
    </main>
  )
}
