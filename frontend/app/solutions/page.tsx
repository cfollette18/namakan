'use client'

import { motion } from 'framer-motion'
import {
  Brain,
  Database,
  Workflow,
  Users,
  CheckCircle,
  ArrowRight,
  Sparkles,
  Settings,
  FileSearch,
  Zap,
  Shield,
  TrendingUp
} from 'lucide-react'
import Link from 'next/link'

export default function SolutionsPage() {
  const solutions = [
    {
      icon: Brain,
      title: "Fine-Tuned Models",
      description: "AI models trained specifically on your proprietary data — your industry knowledge, products, customers, and internal processes. Not general language. Your domain.",
      features: [
        "Trained on your documents and data",
        "Knows your brand voice and standards",
        "Always cites your sources",
        "40-60% accuracy improvement over generic AI"
      ],
      useCase: "A law firm fine-tuned a model on their case history. Now it drafts and reviews contracts in their specific practice areas."
    },
    {
      icon: Database,
      title: "RAG Pipelines",
      description: "Your entire knowledge base — contracts, CRM, technical docs, emails — indexed and searchable. Ask any question, get answers grounded in your actual documents.",
      features: [
        "Searches 100s of documents instantly",
        "Always cites the source",
        "Real-time data, not training data",
        "No hallucinations on your data"
      ],
      useCase: "A manufacturer's field team gets AI-generated repair recommendations from 15 years of service records."
    },
    {
      icon: Workflow,
      title: "Agentic Workflows",
      description: "Multi-step tasks completed autonomously in your systems. Research leads, enrich data, draft responses, update records — without human intervention.",
      features: [
        "Multi-step task automation",
        "Integrates with your existing tools",
        "0 human approvals needed",
        "Completes in seconds"
      ],
      useCase: "An incident gets triaged, lot-validated, response drafted, and ops notified — all before a human sees it."
    },
    {
      icon: Users,
      title: "Custom AI Employees",
      description: "AI workers trained on your business that run 24/7 on repeatable work. Researches, drafts, updates, follows up — without constant human input.",
      features: [
        "Handles repetitive tasks continuously",
        "Integrates with your tools and systems",
        "Reports productivity metrics",
        "20+ hours saved per week"
      ],
      useCase: "An AI employee reviews field failure tickets, matches incidents to lot traces, and drafts plant-floor updates every morning."
    }
  ]

  const industries = [
    {
      title: "Manufacturing & Engineering",
      description: "Quality inspection, field service, supply chain, predictive maintenance",
      data: "CAD files, inspection logs, service records, sensor streams"
    },
    {
      title: "Legal & Compliance",
      description: "Contract review, case research, document processing, compliance",
      data: "Case histories, precedents, contracts, regulatory documents"
    },
    {
      title: "Healthcare & Medical",
      description: "Clinical documentation, patient records, claims processing",
      data: "EHR records, clinical notes, treatment protocols"
    },
    {
      title: "Financial Services",
      description: "Modeling, reporting, client data analysis, risk assessment",
      data: "Financial models, client portfolios, market data"
    },
    {
      title: "Professional Services",
      description: "Research, document drafting, client knowledge management",
      data: "Client files, practice area knowledge, internal docs"
    }
  ]

  const howItWorks = [
    {
      step: "01",
      title: "Discovery",
      description: "We spend time understanding your data, your workflows, and your highest-impact opportunity. Not a pitch — a real assessment."
    },
    {
      step: "02",
      title: "Engineering",
      description: "We build a custom system around your specific data and environment. Fine-tuning, RAG, agentic workflows — whatever fits your problem."
    },
    {
      step: "03",
      title: "Delivery",
      description: "We deploy, test, and measure against your specific use cases. You own the system. We measure results."
    }
  ]

  return (
    <main className="min-h-screen bg-white dark:bg-slate-950 text-slate-900 dark:text-white">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 dark:bg-slate-950/80 backdrop-blur-xl border-b border-slate-200 dark:border-slate-800">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-12">
              <Link href="/" className="text-2xl font-bold bg-gradient-to-r from-teal-500 to-teal-600 text-transparent bg-clip-text">
                Namakan
              </Link>
              <div className="hidden md:flex items-center gap-8">
                <Link href="/solutions" className="text-slate-600 dark:text-slate-300 hover:text-teal-500 transition-colors font-medium">
                  Solutions
                </Link>
                <Link href="/pricing" className="text-slate-600 dark:text-slate-300 hover:text-teal-500 transition-colors">
                  Pricing
                </Link>
                <Link href="/contact" className="text-slate-600 dark:text-slate-300 hover:text-teal-500 transition-colors">
                  Contact
                </Link>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <Link href="/contact">
                <button className="px-6 py-2.5 bg-gradient-to-r from-teal-500 to-teal-600 rounded-lg font-semibold hover:shadow-lg hover:shadow-teal-500/30 transition-all text-white">
                  Get Started
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
              'radial-gradient(circle at 20% 50%, rgba(13, 148, 136, 0.08) 0%, transparent 50%)',
              'radial-gradient(circle at 80% 50%, rgba(13, 148, 136, 0.06) 0%, transparent 50%)',
              'radial-gradient(circle at 20% 50%, rgba(13, 148, 136, 0.08) 0%, transparent 50%)',
            ]
          }}
          transition={{ duration: 10, repeat: Infinity }}
          className="absolute inset-0"
        />

        <div className="relative z-10 container mx-auto max-w-6xl">
          <div className="text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="inline-flex items-center gap-2 mb-6 px-4 py-2 bg-teal-100 dark:bg-teal-500/10 border border-teal-200 dark:border-teal-500/30 rounded-full text-teal-600 dark:text-teal-400 text-sm font-semibold"
            >
              <Brain className="w-4 h-4" />
              Custom AI Engineering
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="text-5xl md:text-7xl font-bold mb-6 leading-tight"
            >
              AI Built on
              <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-teal-500 via-teal-600 to-teal-500">
                YOUR Data
              </span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="text-xl md:text-2xl text-slate-600 dark:text-slate-300 mb-8 max-w-3xl mx-auto"
            >
              Not pre-built agents. Not generic tools. Custom AI systems engineered from the ground up — trained on your proprietary data, integrated into your systems, solving your domain problems.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="flex flex-col sm:flex-row gap-4 justify-center items-center"
            >
              <Link href="/contact">
                <button className="px-8 py-4 bg-gradient-to-r from-teal-500 to-teal-600 rounded-xl font-bold text-lg shadow-lg shadow-teal-500/30 hover:shadow-xl hover:shadow-teal-500/40 transition-all text-white flex items-center gap-2">
                  Talk to an Engineer
                  <ArrowRight className="w-5 h-5" />
                </button>
              </Link>
              <Link href="/pricing">
                <button className="px-8 py-4 bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white rounded-xl font-bold text-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-all">
                  View Pricing
                </button>
              </Link>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Solutions Grid */}
      <section className="py-20 px-6 bg-slate-50 dark:bg-slate-900/50">
        <div className="container mx-auto max-w-7xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              What We Build
            </h2>
            <p className="text-xl text-slate-600 dark:text-slate-300">
              Four ways we engineer custom AI for your proprietary data
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {solutions.map((solution, index) => (
              <motion.div
                key={solution.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-8 hover:border-teal-500/50 transition-all group"
              >
                <div className="w-16 h-16 bg-gradient-to-br from-teal-500 to-teal-600 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                  <solution.icon className="w-8 h-8 text-white" />
                </div>

                <h3 className="text-2xl font-bold mb-4 text-slate-900 dark:text-white">
                  {solution.title}
                </h3>

                <p className="text-slate-600 dark:text-slate-400 mb-6">
                  {solution.description}
                </p>

                <ul className="space-y-2 mb-6">
                  {solution.features.map((feature) => (
                    <li key={feature} className="flex items-center gap-3 text-slate-600 dark:text-slate-400">
                      <CheckCircle className="w-5 h-5 text-teal-500 flex-shrink-0" />
                      {feature}
                    </li>
                  ))}
                </ul>

                <div className="p-4 bg-teal-50 dark:bg-teal-500/10 rounded-lg">
                  <p className="text-sm font-semibold text-teal-600 dark:text-teal-400">
                    💡 {solution.useCase}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 px-6">
        <div className="container mx-auto max-w-6xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              How It Works
            </h2>
            <p className="text-xl text-slate-600 dark:text-slate-300">
              Not a configured tool. Not a vendor platform. Custom engineering for your data.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {howItWorks.map((item, index) => (
              <motion.div
                key={item.step}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="text-center"
              >
                <div className="w-16 h-16 bg-gradient-to-br from-teal-500 to-teal-600 rounded-full flex items-center justify-center mx-auto mb-6">
                  <span className="text-white text-xl font-bold">{item.step}</span>
                </div>
                <h3 className="text-xl font-bold mb-3 text-slate-900 dark:text-white">
                  {item.title}
                </h3>
                <p className="text-slate-600 dark:text-slate-400">
                  {item.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Industries Section */}
      <section className="py-20 px-6 bg-slate-50 dark:bg-slate-900/50">
        <div className="container mx-auto max-w-6xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Industries We Work With
            </h2>
            <p className="text-xl text-slate-600 dark:text-slate-300">
              Every engagement is built around your specific proprietary data
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {industries.map((industry, index) => (
              <motion.div
                key={industry.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.05 }}
                className="p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl"
              >
                <h3 className="text-xl font-bold mb-2 text-slate-900 dark:text-white">
                  {industry.title}
                </h3>
                <p className="text-slate-600 dark:text-slate-400 mb-3">
                  {industry.description}
                </p>
                <p className="text-sm font-semibold text-teal-500">
                  Data: {industry.data}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-6">
        <div className="container mx-auto max-w-4xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center bg-gradient-to-r from-teal-500/10 to-teal-500/10 border border-teal-500/30 rounded-3xl p-12"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Ready to Build AI That Knows Your Business?
            </h2>
            <p className="text-xl text-slate-600 dark:text-slate-300 mb-8">
              Generic AI doesn&apos;t know your data. Let&apos;s talk about building AI that does.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/contact">
                <button className="px-8 py-4 bg-gradient-to-r from-teal-500 to-teal-600 rounded-xl font-bold text-lg shadow-lg shadow-teal-500/30 hover:shadow-xl hover:shadow-teal-500/40 transition-all text-white">
                  Start a Conversation
                </button>
              </Link>
              <Link href="/pricing">
                <button className="px-8 py-4 bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white rounded-xl font-bold text-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-all">
                  View Pricing
                </button>
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-200 dark:border-slate-800 py-16 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="flex flex-col md:flex-row justify-between items-center gap-8">
            <div>
              <h4 className="text-2xl font-bold bg-gradient-to-r from-teal-500 to-teal-600 text-transparent bg-clip-text mb-2">
                Namakan AI Engineering
              </h4>
              <p className="text-slate-500 dark:text-slate-400 text-sm">
                Custom AI built on YOUR data.
              </p>
            </div>
            <div className="flex items-center gap-6 text-sm text-slate-500 dark:text-slate-400">
              <Link href="/pricing" className="hover:text-teal-500 transition-colors">Pricing</Link>
              <Link href="/contact" className="hover:text-teal-500 transition-colors">Contact</Link>
              <Link href="/privacy" className="hover:text-teal-500 transition-colors">Privacy</Link>
              <Link href="/terms" className="hover:text-teal-500 transition-colors">Terms</Link>
            </div>
          </div>
          <div className="border-t border-slate-200 dark:border-slate-800 pt-8 mt-8 flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-slate-500 dark:text-slate-400 text-sm">
              © 2026 Namakan AI Engineering. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </main>
  )
}
