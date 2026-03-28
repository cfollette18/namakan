'use client'

import { motion } from 'framer-motion'
import {
  Users,
  Target,
  Sparkles,
  Zap,
  Globe,
  Award,
  TrendingUp,
  Heart,
  Brain,
  Rocket,
  Shield,
  Building
} from 'lucide-react'
import Link from 'next/link'

export default function AboutPage() {
  const stats = [
    { number: '10M+', label: 'Hours Automated', icon: Zap },
    { number: '50K+', label: 'Active Agents', icon: Brain },
    { number: '99.9%', label: 'Uptime', icon: Shield },
    { number: '500+', label: 'Enterprise Clients', icon: Building }
  ]

  const values = [
    {
      icon: Target,
      title: 'Mission-Driven',
      description: 'We exist to democratize AI agent technology, making autonomous workflows accessible to teams of all sizes.'
    },
    {
      icon: Users,
      title: 'Community First',
      description: 'Our platform grows stronger with every user. We believe in open collaboration and shared success.'
    },
    {
      icon: Sparkles,
      title: 'Innovation Obsessed',
      description: 'We never stop pushing the boundaries of what\'s possible with AI orchestration and multi-agent systems.'
    },
    {
      icon: Heart,
      title: 'Human-Centered',
      description: 'AI should augment human capabilities, not replace them. We design with empathy and human needs first.'
    }
  ]

  const timeline = [
    {
      year: '2023',
      title: 'Foundation',
      description: 'Namakan was founded with a vision to revolutionize how teams work with AI agents.'
    },
    {
      year: '2024',
      title: 'First Release',
      description: 'Launched our core orchestration platform with support for custom agent workflows.'
    },
    {
      year: '2025',
      title: 'Marketplace Launch',
      description: 'Opened our agent marketplace, enabling users to share and monetize templates.'
    },
    {
      year: '2026',
      title: 'Enterprise Scale',
      description: 'Achieved SOC 2 compliance and expanded to serve Fortune 500 companies.'
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

        <div className="relative z-10 container mx-auto max-w-4xl">
          <div className="text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="inline-flex items-center gap-2 mb-6 px-4 py-2 bg-pink-100 dark:bg-pink-500/10 border border-pink-200 dark:border-pink-500/30 rounded-full text-pink-600 dark:text-pink-400 text-sm font-semibold"
            >
              <Sparkles className="w-4 h-4" />
              Our Story
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="text-5xl md:text-7xl font-bold mb-6 leading-tight"
            >
              Building the
              <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-500 via-pink-600 to-pink-500">
                Future of Work
              </span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="text-xl md:text-2xl text-slate-600 dark:text-slate-300 mb-8 max-w-3xl mx-auto"
            >
              We're on a mission to make AI agents accessible to every team, revolutionizing how work gets done
              through intelligent orchestration and autonomous collaboration.
            </motion.p>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 px-6 bg-slate-50 dark:bg-slate-900/50">
        <div className="container mx-auto max-w-6xl">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="text-center"
              >
                <div className="w-16 h-16 bg-gradient-to-br from-pink-500 to-pink-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                  <stat.icon className="w-8 h-8 text-white" />
                </div>
                <div className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white mb-2">
                  {stat.number}
                </div>
                <div className="text-slate-600 dark:text-slate-400 font-medium">
                  {stat.label}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-20 px-6">
        <div className="container mx-auto max-w-6xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Our Mission
            </h2>
            <p className="text-xl text-slate-600 dark:text-slate-300 max-w-3xl mx-auto">
              To democratize AI agent technology and make autonomous workflows accessible to teams of all sizes,
              revolutionizing how work gets done through intelligent orchestration.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
            >
              <h3 className="text-2xl font-bold mb-4">Why We Exist</h3>
              <div className="space-y-4 text-slate-600 dark:text-slate-400">
                <p>
                  Traditional automation tools are rigid and limited. They handle simple tasks but fail at complex,
                  creative work that requires intelligence, adaptation, and collaboration.
                </p>
                <p>
                  We believe the future of work involves teams of specialized AI agents that can communicate,
                  coordinate, and solve problems autonomously - just like human teams do.
                </p>
                <p>
                  Our platform makes this vision a reality, enabling anyone to orchestrate powerful AI workflows
                  without coding expertise.
                </p>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="bg-gradient-to-br from-pink-50 to-purple-50 dark:from-pink-500/10 dark:to-purple-500/10 rounded-2xl p-8 border border-pink-200 dark:border-pink-500/30"
            >
              <h4 className="font-bold text-lg mb-4 text-slate-900 dark:text-white">The Problem We're Solving</h4>
              <ul className="space-y-3">
                <li className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-pink-500 rounded-full mt-2 flex-shrink-0"></div>
                  <span className="text-slate-600 dark:text-slate-400">
                    Teams spend 80% of their time on repetitive, low-value tasks
                  </span>
                </li>
                <li className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-pink-500 rounded-full mt-2 flex-shrink-0"></div>
                  <span className="text-slate-600 dark:text-slate-400">
                    Current AI tools are isolated and don't collaborate effectively
                  </span>
                </li>
                <li className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-pink-500 rounded-full mt-2 flex-shrink-0"></div>
                  <span className="text-slate-600 dark:text-slate-400">
                    Complex workflows require coding expertise that's hard to find
                  </span>
                </li>
                <li className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-pink-500 rounded-full mt-2 flex-shrink-0"></div>
                  <span className="text-slate-600 dark:text-slate-400">
                    Organizations struggle to scale AI adoption across teams
                  </span>
                </li>
              </ul>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="py-20 px-6 bg-slate-50 dark:bg-slate-900/50">
        <div className="container mx-auto max-w-6xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Our Values
            </h2>
            <p className="text-xl text-slate-600 dark:text-slate-300">
              The principles that guide everything we do
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {values.map((value, index) => (
              <motion.div
                key={value.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-8"
              >
                <div className="w-16 h-16 bg-gradient-to-br from-pink-500 to-pink-600 rounded-xl flex items-center justify-center mb-6">
                  <value.icon className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-xl font-bold mb-4 text-slate-900 dark:text-white">
                  {value.title}
                </h3>
                <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
                  {value.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Timeline Section */}
      <section className="py-20 px-6">
        <div className="container mx-auto max-w-4xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Our Journey
            </h2>
            <p className="text-xl text-slate-600 dark:text-slate-300">
              From vision to reality
            </p>
          </motion.div>

          <div className="space-y-8">
            {timeline.map((item, index) => (
              <motion.div
                key={item.year}
                initial={{ opacity: 0, x: index % 2 === 0 ? -20 : 20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="flex gap-8 items-start"
              >
                <div className="flex-shrink-0">
                  <div className="w-16 h-16 bg-gradient-to-br from-pink-500 to-pink-600 rounded-xl flex items-center justify-center">
                    <span className="text-white font-bold">{item.year}</span>
                  </div>
                </div>
                <div className="flex-1 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6">
                  <h3 className="text-xl font-bold mb-2 text-slate-900 dark:text-white">
                    {item.title}
                  </h3>
                  <p className="text-slate-600 dark:text-slate-400">
                    {item.description}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-6 bg-gradient-to-r from-pink-500 to-pink-600">
        <div className="container mx-auto max-w-4xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6 text-white">
              Join Our Mission
            </h2>
            <p className="text-xl text-pink-100 mb-8 max-w-2xl mx-auto">
              Be part of the AI revolution. Start building autonomous workflows today and help shape the future of work.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/auth/signup">
                <button className="px-8 py-4 bg-white text-pink-600 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transition-all flex items-center gap-2">
                  <Rocket className="w-5 h-5" />
                  Get Started Free
                </button>
              </Link>
              <Link href="/careers">
                <button className="px-8 py-4 bg-pink-600/20 text-white border border-white/30 rounded-xl font-bold text-lg hover:bg-pink-600/30 transition-all">
                  Join Our Team
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
                AI agent orchestration for the future of work
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
                <li><Link href="/about" className="hover:text-pink-500 transition-colors font-medium">About</Link></li>
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