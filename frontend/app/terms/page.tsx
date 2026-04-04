/* eslint-disable react/no-unescaped-entities */
'use client'

import { motion } from 'framer-motion'
import {
  FileText,
  Scale,
  Shield,
  AlertTriangle,
  Calendar,
  Sparkles
} from 'lucide-react'
import Link from 'next/link'

export default function TermsPage() {
  const sections = [
    {
      title: 'Acceptance of Terms',
      icon: FileText,
      content: [
        'By accessing and using Namakan, you accept and agree to be bound by the terms and provision of this agreement.',
        'If you do not agree to abide by the above, please do not use this service.',
        'These terms apply to all visitors, users, and others who access or use our service.'
      ]
    },
    {
      title: 'Service Description',
      icon: Sparkles,
      content: [
        'Namakan provides an Custom AI Engineering firm for creating and managing custom AI workflows.',
        'We reserve the right to modify or discontinue the service at any time without notice.',
        'Service availability is not guaranteed and may be subject to maintenance or outages.'
      ]
    },
    {
      title: 'User Responsibilities',
      icon: Shield,
      content: [
        'You must provide accurate and complete information when creating an account.',
        'You are responsible for maintaining the confidentiality of your account credentials.',
        'You agree not to use the service for any unlawful or prohibited activities.',
        'You must not attempt to reverse engineer, modify, or interfere with our platform.'
      ]
    },
    {
      title: 'Payment Terms',
      icon: Scale,
      content: [
        'Subscription fees are billed in advance on a recurring basis.',
        'All fees are non-refundable except as required by law or our refund policy.',
        'We reserve the right to change pricing with 30 days notice.',
        'Late payments may result in service suspension or termination.'
      ]
    },
    {
      title: 'Intellectual Property',
      icon: AlertTriangle,
      content: [
        'All content, features, and functionality are owned by Namakan and protected by copyright.',
        'You retain ownership of your data and AI agent configurations.',
        'We grant you a limited, non-exclusive license to use our platform.',
        'You may not reproduce, distribute, or create derivative works of our service.'
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
              <Scale className="w-4 h-4" />
              Terms of Service
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="text-4xl md:text-6xl font-bold mb-6 leading-tight"
            >
              Terms &
              <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-teal-500 via-teal-600 to-teal-500">
                Conditions
              </span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="text-xl text-slate-600 dark:text-slate-300 mb-8 max-w-2xl mx-auto"
            >
              Please read these terms carefully before using our Custom AI Engineering firm.
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

      {/* Overview */}
      <section className="py-16 px-6 bg-slate-50 dark:bg-slate-900/50">
        <div className="container mx-auto max-w-4xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-8"
          >
            <h2 className="text-2xl font-bold mb-4 text-slate-900 dark:text-white">Agreement Overview</h2>
            <p className="text-slate-600 dark:text-slate-400 mb-4">
              These Terms of Service ("Terms") constitute a legally binding agreement between you and Namakan
              ("we," "us," or "our") governing your use of our Custom AI Engineering firm and related services.
            </p>
            <p className="text-slate-600 dark:text-slate-400">
              By accessing or using our service, you agree to be bound by these Terms.
              If you disagree with any part of these terms, you may not access the service.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Terms Sections */}
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

            {/* Additional Important Sections */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.5 }}
              className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-8"
            >
              <h3 className="text-xl font-bold mb-4 text-slate-900 dark:text-white">Limitation of Liability</h3>
              <p className="text-slate-600 dark:text-slate-400 mb-4">
                In no event shall Namakan, its directors, employees, partners, agents, suppliers, or affiliates be liable
                for any indirect, incidental, special, consequential, or punitive damages, including without limitation,
                loss of profits, data, use, goodwill, or other intangible losses.
              </p>
              <p className="text-slate-600 dark:text-slate-400">
                Our total liability shall not exceed the amount paid by you for the service in the twelve months preceding the claim.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.6 }}
              className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-8"
            >
              <h3 className="text-xl font-bold mb-4 text-slate-900 dark:text-white">Termination</h3>
              <p className="text-slate-600 dark:text-slate-400 mb-4">
                We may terminate or suspend your account immediately, without prior notice or liability,
                for any reason whatsoever, including without limitation if you breach the Terms.
              </p>
              <p className="text-slate-600 dark:text-slate-400">
                Upon termination, your right to use the service will cease immediately.
                All provisions of the Terms which by their nature should survive termination shall survive.
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section className="py-20 px-6 bg-slate-50 dark:bg-slate-900/50">
        <div className="container mx-auto max-w-4xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center bg-gradient-to-r from-teal-500/10 to-teal-500/10 border border-teal-500/30 rounded-3xl p-12"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Questions About These Terms?
            </h2>
            <p className="text-xl text-slate-600 dark:text-slate-300 mb-8">
              If you have any questions about these Terms of Service,
              please contact our legal team.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/contact">
                <button className="px-8 py-4 bg-gradient-to-r from-teal-500 to-teal-600 rounded-xl font-bold text-lg shadow-lg shadow-teal-500/30 hover:shadow-xl hover:shadow-teal-500/40 transition-all">
                  Contact Legal Team
                </button>
              </Link>
              <Link href="mailto:legal@namakanai.com">
                <button className="px-8 py-4 bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white rounded-xl font-bold text-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-all">
                  legal@namakanai.com
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
                <li><Link href="/privacy" className="hover:text-teal-500 transition-colors">Privacy</Link></li>
                <li><Link href="/terms" className="hover:text-teal-500 transition-colors font-medium">Terms</Link></li>
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