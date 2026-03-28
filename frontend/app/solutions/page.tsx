'use client'

import { motion } from 'framer-motion'
import {
  Cpu,
  Zap,
  BarChart3,
  Users,
  Code,
  CheckCircle,
  ArrowRight,
  Sparkles,
  Target,
  TrendingUp,
  Shield,
  Globe,
  Brain,
  Workflow,
  MessageSquare,
  FileText,
  Search,
  Palette,
  Megaphone,
  Calculator,
  Briefcase,
  Heart,
  GraduationCap,
  Building,
  Stethoscope,
  Factory,
  Scale
} from 'lucide-react'
import Link from 'next/link'

export default function SolutionsPage() {
  const solutions = [
    {
      icon: Briefcase,
      title: "Business Operations",
      description: "Streamline workflows, automate repetitive tasks, and optimize business processes with intelligent AI agents.",
      features: [
        "Process automation",
        "Data analysis & reporting",
        "Customer service automation",
        "Inventory management",
        "Financial forecasting"
      ],
      useCase: "Reduce operational overhead by 60% with automated business workflows."
    },
    {
      icon: Megaphone,
      title: "Marketing & Content",
      description: "Create compelling content, manage campaigns, and analyze performance across all marketing channels.",
      features: [
        "Content creation & optimization",
        "Social media management",
        "Email marketing automation",
        "SEO analysis & optimization",
        "Campaign performance tracking"
      ],
      useCase: "Generate 10x more content while maintaining brand consistency."
    },
    {
      icon: Code,
      title: "Software Development",
      description: "Accelerate development cycles with AI-powered coding assistants, testing, and deployment automation.",
      features: [
        "Code generation & review",
        "Automated testing",
        "Documentation generation",
        "Bug detection & fixing",
        "Performance optimization"
      ],
      useCase: "Ship features 3x faster with AI-assisted development workflows."
    },
    {
      icon: Search,
      title: "Research & Analysis",
      description: "Conduct comprehensive research, analyze data, and generate insights across any domain.",
      features: [
        "Market research automation",
        "Competitive analysis",
        "Data visualization",
        "Trend identification",
        "Report generation"
      ],
      useCase: "Complete research projects in hours instead of weeks."
    },
    {
      icon: Heart,
      title: "Customer Experience",
      description: "Enhance customer interactions with personalized experiences and intelligent support systems.",
      features: [
        "Personalized recommendations",
        "Chatbot automation",
        "Customer feedback analysis",
        "Support ticket routing",
        "Satisfaction prediction"
      ],
      useCase: "Improve customer satisfaction scores by 40% with AI-driven experiences."
    },
    {
      icon: TrendingUp,
      title: "Sales & Revenue",
      description: "Optimize sales processes, identify opportunities, and maximize revenue with intelligent automation.",
      features: [
        "Lead qualification & scoring",
        "Sales forecasting",
        "Proposal generation",
        "Customer insights",
        "Revenue optimization"
      ],
      useCase: "Increase conversion rates by 25% with AI-powered sales enablement."
    }
  ]

  const industries = [
    {
      icon: Building,
      name: "Enterprise",
      description: "Large organizations automating complex workflows and scaling operations.",
      metrics: "500+ employees, complex integrations"
    },
    {
      icon: Briefcase,
      name: "Professional Services",
      description: "Consulting firms, agencies, and service providers enhancing client delivery.",
      metrics: "10-500 employees, client-focused"
    },
    {
      icon: Factory,
      name: "Manufacturing",
      description: "Production companies optimizing supply chains and quality control.",
      metrics: "Process automation, quality assurance"
    },
    {
      icon: Stethoscope,
      name: "Healthcare",
      description: "Medical organizations improving patient care and administrative efficiency.",
      metrics: "HIPAA compliant, patient-focused"
    },
    {
      icon: GraduationCap,
      name: "Education",
      description: "Universities and schools personalizing learning experiences.",
      metrics: "Student success, administrative efficiency"
    },
    {
      icon: Scale,
      name: "Legal & Finance",
      description: "Law firms and financial institutions ensuring compliance and accuracy.",
      metrics: "Regulatory compliance, risk management"
    }
  ]

  const workflows = [
    {
      title: "Marketing Campaign Launch",
      steps: [
        "Market research & audience analysis",
        "Content strategy development",
        "Creative asset generation",
        "Multi-channel campaign setup",
        "Performance monitoring & optimization"
      ],
      timeSaved: "From 2 weeks to 2 days",
      agents: ["Research Agent", "Content Creator", "Social Media Manager", "Analytics Agent"]
    },
    {
      title: "Product Development Cycle",
      steps: [
        "Market analysis & competitor research",
        "Feature specification & requirements",
        "Technical architecture design",
        "Implementation planning",
        "Testing strategy development"
      ],
      timeSaved: "From 3 months to 1 week",
      agents: ["Market Analyst", "Technical Architect", "Project Manager", "QA Engineer"]
    },
    {
      title: "Customer Onboarding Process",
      steps: [
        "Lead qualification & scoring",
        "Personalized welcome sequence",
        "Product training materials",
        "Success milestone tracking",
        "Feedback collection & analysis"
      ],
      timeSaved: "From 1 week to 1 hour",
      agents: ["Sales Assistant", "Content Creator", "Customer Success Agent", "Analytics Agent"]
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
                <Link href="/solutions" className="text-slate-600 dark:text-slate-300 hover:text-pink-500 transition-colors font-medium">
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

        <div className="relative z-10 container mx-auto max-w-6xl">
          <div className="text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="inline-flex items-center gap-2 mb-6 px-4 py-2 bg-pink-100 dark:bg-pink-500/10 border border-pink-200 dark:border-pink-500/30 rounded-full text-pink-600 dark:text-pink-400 text-sm font-semibold"
            >
              <Sparkles className="w-4 h-4" />
              AI Solutions for Every Business
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="text-5xl md:text-7xl font-bold mb-6 leading-tight"
            >
              Solutions That
              <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-500 via-pink-600 to-pink-500">
                Scale With You
              </span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="text-xl md:text-2xl text-slate-600 dark:text-slate-300 mb-8 max-w-3xl mx-auto"
            >
              From startups to enterprises, discover how AI agents can transform your business operations,
              marketing, development, and customer experience.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="flex flex-col sm:flex-row gap-4 justify-center items-center"
            >
              <Link href="/auth/signup">
                <button className="px-8 py-4 bg-gradient-to-r from-pink-500 to-pink-600 rounded-xl font-bold text-lg shadow-lg shadow-pink-500/30 hover:shadow-xl hover:shadow-pink-500/40 transition-all flex items-center gap-2">
                  Get Started Free
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
              AI Solutions by Function
            </h2>
            <p className="text-xl text-slate-600 dark:text-slate-300">
              Specialized agent teams for every business need
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {solutions.map((solution, index) => (
              <motion.div
                key={solution.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-8 hover:border-pink-500/50 transition-all group"
              >
                <div className="w-16 h-16 bg-gradient-to-br from-pink-500 to-pink-600 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
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
                      <CheckCircle className="w-5 h-5 text-pink-500 flex-shrink-0" />
                      {feature}
                    </li>
                  ))}
                </ul>

                <div className="p-4 bg-pink-50 dark:bg-pink-500/10 rounded-lg">
                  <p className="text-sm font-semibold text-pink-600 dark:text-pink-400">
                    💡 {solution.useCase}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Industries Section */}
      <section className="py-20 px-6">
        <div className="container mx-auto max-w-6xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Trusted Across Industries
            </h2>
            <p className="text-xl text-slate-600 dark:text-slate-300">
              Solutions tailored for your industry requirements
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {industries.map((industry, index) => (
              <motion.div
                key={industry.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.05 }}
                className="p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl hover:border-pink-500/50 transition-all"
              >
                <industry.icon className="w-12 h-12 text-pink-500 mb-4" />
                <h3 className="text-xl font-bold mb-2 text-slate-900 dark:text-white">
                  {industry.name}
                </h3>
                <p className="text-slate-600 dark:text-slate-400 mb-3">
                  {industry.description}
                </p>
                <p className="text-sm font-semibold text-pink-500">
                  {industry.metrics}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Workflows Section */}
      <section className="py-20 px-6 bg-slate-50 dark:bg-slate-900/50">
        <div className="container mx-auto max-w-6xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Complete Workflow Automation
            </h2>
            <p className="text-xl text-slate-600 dark:text-slate-300">
              End-to-end processes handled by coordinated AI agent teams
            </p>
          </motion.div>

          <div className="space-y-8">
            {workflows.map((workflow, index) => (
              <motion.div
                key={workflow.title}
                initial={{ opacity: 0, x: index % 2 === 0 ? -20 : 20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-8"
              >
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                  <div className="lg:col-span-1">
                    <h3 className="text-2xl font-bold mb-4 text-slate-900 dark:text-white">
                      {workflow.title}
                    </h3>
                    <div className="p-4 bg-pink-50 dark:bg-pink-500/10 rounded-lg mb-4">
                      <p className="text-lg font-semibold text-pink-600 dark:text-pink-400">
                        ⚡ {workflow.timeSaved}
                      </p>
                    </div>
                    <div className="space-y-2">
                      <p className="font-semibold text-slate-700 dark:text-slate-300 mb-2">AI Agents:</p>
                      {workflow.agents.map((agent) => (
                        <div key={agent} className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400">
                          <CheckCircle className="w-4 h-4 text-pink-500" />
                          {agent}
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="lg:col-span-2">
                    <h4 className="font-semibold mb-4 text-slate-700 dark:text-slate-300">Workflow Steps:</h4>
                    <div className="space-y-3">
                      {workflow.steps.map((step, stepIndex) => (
                        <div key={step} className="flex items-start gap-3">
                          <div className="w-8 h-8 bg-pink-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                            <span className="text-white text-sm font-bold">{stepIndex + 1}</span>
                          </div>
                          <p className="text-slate-600 dark:text-slate-400 pt-1">{step}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
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
            className="text-center bg-gradient-to-r from-pink-500/10 to-purple-500/10 border border-pink-500/30 rounded-3xl p-12"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Ready to Transform Your Business?
            </h2>
            <p className="text-xl text-slate-600 dark:text-slate-300 mb-8">
              Join thousands of companies using Namakan to automate complex workflows and scale operations.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/auth/signup">
                <button className="px-8 py-4 bg-gradient-to-r from-pink-500 to-pink-600 rounded-xl font-bold text-lg shadow-lg shadow-pink-500/30 hover:shadow-xl hover:shadow-pink-500/40 transition-all">
                  Start Free Trial
                </button>
              </Link>
              <Link href="/contact">
                <button className="px-8 py-4 bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white rounded-xl font-bold text-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-all">
                  Schedule Demo
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