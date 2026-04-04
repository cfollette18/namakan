/* eslint-disable react/no-unescaped-entities */
'use client'

import { motion } from 'framer-motion'
import {
  Shield,
  Lock,
  Eye,
  Database,
  Mail,
  Calendar,
  Sparkles
} from 'lucide-react'
import Link from 'next/link'

export default function PrivacyPage() {
  const sections = [
    {
      title: 'Information We Collect',
      icon: Database,
      content: [
        'Account information (name, email, company)',
        'Usage data and analytics',
        'AI agent configurations and templates',
        'Communication preferences',
        'Payment information (processed securely by third parties)'
      ]
    },
    {
      title: 'How We Use Your Information',
      icon: Eye,
      content: [
        'Provide and improve our AI orchestration platform',
        'Process payments and manage subscriptions',
        'Send important updates and security notifications',
        'Analyze usage patterns to enhance user experience',
        'Comply with legal obligations and prevent fraud'
      ]
    },
    {
      title: 'Information Sharing',
      icon: Mail,
      content: [
        'We do not sell your personal information',
        'Limited sharing with trusted service providers',
        'Legal compliance and safety requirements',
        'Business transfers (with notice)',
        'Aggregated, anonymized data for analytics'
      ]
    },
    {
      title: 'Data Security',
      icon: Lock,
      content: [
        'End-to-end encryption for data in transit and at rest',
        'Regular security audits and penetration testing',
        'SOC 2 Type II compliance',
        'Access controls and employee training',
        'Incident response plan and breach notification'
      ]
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
                <Link href="/solutions" className="text-slate-600 dark:text-slate-300 hover:text-teal-500 transition-colors">
                  Solutions
                </Link>
                <Link href="/pricing" className="text-slate-600 dark:text-slate-300 hover:text-teal-500 transition-colors">
                  Pricing
                </Link>
                <Link href="/services" className="text-slate-600 dark:text-slate-300 hover:text-teal-500 transition-colors">
                  Services
                </Link>
                <Link href="/templates" className="text-slate-600 dark:text-slate-300 hover:text-teal-500 transition-colors">
                  Marketplace
                </Link>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <Link href="/auth/login" className="text-slate-600 dark:text-slate-300 hover:text-teal-500 transition-colors font-medium">
                Log in
              </Link>
              <Link href="/auth/signup">
                <button className="px-6 py-2.5 bg-gradient-to-r from-teal-500 to-teal-600 rounded-lg font-semibold hover:shadow-lg hover:shadow-teal-500/30 transition-all">
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
              <Shield className="w-4 h-4" />
              Privacy Policy
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="text-4xl md:text-6xl font-bold mb-6 leading-tight"
            >
              Your Privacy is
              <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-teal-500 via-teal-600 to-teal-500">
                Our Priority
              </span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="text-xl text-slate-600 dark:text-slate-300 mb-8 max-w-2xl mx-auto"
            >
              We are committed to protecting your privacy and being transparent about how we handle your data.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="flex items-center justify-center gap-2 text-sm text-slate-500 dark:text-slate-400"
            >
              <Calendar className="w-4 h-4" />
              Last updated: January 19, 2026
            </motion.div>
          </div>
        </div>
      </section>

      {/* Overview Section */}
      <section className="py-16 px-6 bg-slate-50 dark:bg-slate-900/50">
        <div className="container mx-auto max-w-4xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-8"
          >
            <h2 className="text-2xl font-bold mb-4 text-slate-900 dark:text-white">Privacy Overview</h2>
            <p className="text-slate-600 dark:text-slate-400 mb-4">
              This Privacy Policy describes how Namakan ("we," "us," or "our") collects, uses, and protects your personal information
              when you use our Custom AI Engineering firm.
            </p>
            <p className="text-slate-600 dark:text-slate-400">
              By using Namakan, you agree to the collection and use of information in accordance with this policy.
              We will not use or share your information except as described in this Privacy Policy.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Privacy Sections */}
      <section className="py-20 px-6">
        <div className="container mx-auto max-w-4xl">
          <div className="space-y-8">
            {sections.map((section, index) => (
              <motion.div
                key={section.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-8"
              >
                <div className="flex items-start gap-4 mb-6">
                  <div className="w-12 h-12 bg-gradient-to-br from-teal-500 to-teal-600 rounded-xl flex items-center justify-center flex-shrink-0">
                    <section.icon className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold mb-2 text-slate-900 dark:text-white">
                      {section.title}
                    </h3>
                  </div>
                </div>

                <ul className="space-y-3">
                  {section.content.map((item, itemIndex) => (
                    <li key={itemIndex} className="flex items-start gap-3 text-slate-600 dark:text-slate-400">
                      <div className="w-2 h-2 bg-teal-500 rounded-full mt-2 flex-shrink-0"></div>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Additional Sections */}
      <section className="py-16 px-6 bg-slate-50 dark:bg-slate-900/50">
        <div className="container mx-auto max-w-4xl">
          <div className="space-y-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-8"
            >
              <h3 className="text-xl font-bold mb-4 text-slate-900 dark:text-white">Your Rights</h3>
              <p className="text-slate-600 dark:text-slate-400 mb-4">
                Depending on your location, you may have certain rights regarding your personal information:
              </p>
              <ul className="space-y-2 text-slate-600 dark:text-slate-400">
                <li>• <strong>Access:</strong> Request a copy of your personal data</li>
                <li>• <strong>Rectification:</strong> Correct inaccurate or incomplete data</li>
                <li>• <strong>Erasure:</strong> Request deletion of your personal data</li>
                <li>• <strong>Portability:</strong> Receive your data in a structured format</li>
                <li>• <strong>Objection:</strong> Object to processing based on legitimate interests</li>
              </ul>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1 }}
              className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-8"
            >
              <h3 className="text-xl font-bold mb-4 text-slate-900 dark:text-white">Data Retention</h3>
              <p className="text-slate-600 dark:text-slate-400 mb-4">
                We retain your personal information for as long as necessary to provide our services and comply with legal obligations:
              </p>
              <ul className="space-y-2 text-slate-600 dark:text-slate-400">
                <li>• <strong>Account data:</strong> Retained while your account is active</li>
                <li>• <strong>Usage data:</strong> Anonymized after 2 years</li>
                <li>• <strong>Communication:</strong> Retained for customer service purposes</li>
                <li>• <strong>Legal compliance:</strong> Retained as required by law</li>
              </ul>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 }}
              className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-8"
            >
              <h3 className="text-xl font-bold mb-4 text-slate-900 dark:text-white">International Data Transfers</h3>
              <p className="text-slate-600 dark:text-slate-400 mb-4">
                Namakan operates globally and may transfer your information to countries other than your own.
                We ensure appropriate safeguards are in place for international transfers.
              </p>
              <ul className="space-y-2 text-slate-600 dark:text-slate-400">
                <li>• Standard contractual clauses approved by relevant authorities</li>
                <li>• Adequacy decisions for certain countries</li>
                <li>• Your consent where required</li>
                <li>• Certification schemes and codes of conduct</li>
              </ul>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section className="py-20 px-6">
        <div className="container mx-auto max-w-4xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center bg-gradient-to-r from-teal-500/10 to-teal-500/10 border border-teal-500/30 rounded-3xl p-12"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Questions About Privacy?
            </h2>
            <p className="text-xl text-slate-600 dark:text-slate-300 mb-8">
              If you have any questions about this Privacy Policy or our data practices,
              please don't hesitate to contact us.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/contact">
                <button className="px-8 py-4 bg-gradient-to-r from-teal-500 to-teal-600 rounded-xl font-bold text-lg shadow-lg shadow-teal-500/30 hover:shadow-xl hover:shadow-teal-500/40 transition-all">
                  Contact Privacy Team
                </button>
              </Link>
              <Link href="mailto:privacy@namakanai.com">
                <button className="px-8 py-4 bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white rounded-xl font-bold text-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-all">
                  privacy@namakanai.com
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
              <h4 className="text-2xl font-bold bg-gradient-to-r from-teal-500 to-teal-600 text-transparent bg-clip-text mb-4">
                Namakan
              </h4>
              <p className="text-slate-600 dark:text-slate-400 mb-4">
                Custom AI built on YOUR data
              </p>
            </div>

            <div>
              <h5 className="font-bold mb-4 text-slate-900 dark:text-white">Solutions</h5>
              <ul className="space-y-2 text-slate-600 dark:text-slate-400">
                <li><Link href="/solutions" className="hover:text-teal-500 transition-colors">Solutions</Link></li>
                <li><Link href="/services" className="hover:text-teal-500 transition-colors">Services</Link></li>
                <li><Link href="/templates" className="hover:text-teal-500 transition-colors">Templates</Link></li>
              </ul>
            </div>

            <div>
              <h5 className="font-bold mb-4 text-slate-900 dark:text-white">Resources</h5>
              <ul className="space-y-2 text-slate-600 dark:text-slate-400">
                <li><Link href="/templates" className="hover:text-teal-500 transition-colors">Templates</Link></li>
                <li><Link href="/about" className="hover:text-teal-500 transition-colors">About</Link></li>
              </ul>
            </div>

            <div>
              <h5 className="font-bold mb-4 text-slate-900 dark:text-white">Company</h5>
              <ul className="space-y-2 text-slate-600 dark:text-slate-400">
                <li><Link href="/about" className="hover:text-teal-500 transition-colors">About</Link></li>
                <li><Link href="/about" className="hover:text-teal-500 transition-colors">Careers</Link></li>
                <li><Link href="/contact" className="hover:text-teal-500 transition-colors">Contact</Link></li>
                <li><Link href="/privacy" className="hover:text-teal-500 transition-colors font-medium">Privacy</Link></li>
                <li><Link href="/terms" className="hover:text-teal-500 transition-colors">Terms</Link></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-slate-200 dark:border-slate-800 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-slate-500 dark:text-slate-400 text-sm">
              &copy; 2026 Namakan. All rights reserved.
            </p>
            <div className="flex items-center gap-6 text-sm text-slate-500 dark:text-slate-400">
              <Link href="/about" className="hover:text-teal-500 transition-colors">About</Link>
              <Link href="/contact" className="hover:text-teal-500 transition-colors">Contact</Link>
            </div>
          </div>
        </div>
      </footer>
    </main>
  )
}