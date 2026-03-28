'use client'

import { motion } from 'framer-motion'
import {
  Mail,
  Phone,
  MapPin,
  MessageSquare,
  Send,
  Clock,
  Users,
  HeadphonesIcon,
  Sparkles
} from 'lucide-react'
import Link from 'next/link'
import { useState } from 'react'

export default function ContactPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    company: '',
    message: '',
    inquiryType: 'general'
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Handle form submission here
    console.log('Form submitted:', formData)
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const contactMethods = [
    {
      icon: Mail,
      title: 'Email Support',
      description: 'Get help from our support team',
      contact: 'support@namakan.ai',
      availability: '24/7 via email'
    },
    {
      icon: MessageSquare,
      title: 'Live Chat',
      description: 'Chat with our AI assistant',
      contact: 'Available 9 AM - 6 PM EST',
      availability: 'Mon-Fri, Business Hours'
    },
    {
      icon: Phone,
      title: 'Phone Support',
      description: 'Speak directly with our team',
      contact: '+1 (555) 123-4567',
      availability: 'Enterprise customers only'
    },
    {
      icon: Users,
      title: 'Community',
      description: 'Join our community forum',
      contact: 'community.namakan.ai',
      availability: 'Always available'
    }
  ]

  const offices = [
    {
      city: 'San Francisco',
      address: '123 AI Street, San Francisco, CA 94105',
      phone: '+1 (555) 123-4567'
    },
    {
      city: 'New York',
      address: '456 Tech Avenue, New York, NY 10001',
      phone: '+1 (555) 987-6543'
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
              <HeadphonesIcon className="w-4 h-4" />
              Get in Touch
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="text-5xl md:text-7xl font-bold mb-6 leading-tight"
            >
              Let's Build
              <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-500 via-pink-600 to-pink-500">
                Something Amazing
              </span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="text-xl md:text-2xl text-slate-600 dark:text-slate-300 mb-8 max-w-2xl mx-auto"
            >
              Have questions about Namakan? Need help with your AI agents?
              We're here to help you succeed.
            </motion.p>
          </div>
        </div>
      </section>

      {/* Contact Methods */}
      <section className="pb-20 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-20">
            {contactMethods.map((method, index) => (
              <motion.div
                key={method.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 text-center hover:border-pink-500/50 transition-all"
              >
                <div className="w-12 h-12 bg-gradient-to-br from-pink-500 to-pink-600 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <method.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="font-bold text-lg mb-2 text-slate-900 dark:text-white">
                  {method.title}
                </h3>
                <p className="text-slate-600 dark:text-slate-400 mb-3 text-sm">
                  {method.description}
                </p>
                <p className="font-semibold text-pink-600 dark:text-pink-400 text-sm">
                  {method.contact}
                </p>
                <p className="text-xs text-slate-500 dark:text-slate-500 mt-1">
                  {method.availability}
                </p>
              </motion.div>
            ))}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {/* Contact Form */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-8"
            >
              <h2 className="text-2xl font-bold mb-6 text-slate-900 dark:text-white">
                Send us a message
              </h2>

              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label htmlFor="name" className="block text-sm font-medium mb-2 text-slate-700 dark:text-slate-300">
                      Full Name *
                    </label>
                    <input
                      type="text"
                      id="name"
                      name="name"
                      required
                      value={formData.name}
                      onChange={handleChange}
                      className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                      placeholder="John Doe"
                    />
                  </div>
                  <div>
                    <label htmlFor="email" className="block text-sm font-medium mb-2 text-slate-700 dark:text-slate-300">
                      Email Address *
                    </label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      required
                      value={formData.email}
                      onChange={handleChange}
                      className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                      placeholder="john@company.com"
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="company" className="block text-sm font-medium mb-2 text-slate-700 dark:text-slate-300">
                    Company
                  </label>
                  <input
                    type="text"
                    id="company"
                    name="company"
                    value={formData.company}
                    onChange={handleChange}
                    className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                    placeholder="Your Company"
                  />
                </div>

                <div>
                  <label htmlFor="inquiryType" className="block text-sm font-medium mb-2 text-slate-700 dark:text-slate-300">
                    How can we help?
                  </label>
                  <select
                    id="inquiryType"
                    name="inquiryType"
                    value={formData.inquiryType}
                    onChange={handleChange}
                    className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                  >
                    <option value="general">General Inquiry</option>
                    <option value="sales">Sales & Pricing</option>
                    <option value="support">Technical Support</option>
                    <option value="partnership">Partnership</option>
                    <option value="enterprise">Enterprise Solutions</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="message" className="block text-sm font-medium mb-2 text-slate-700 dark:text-slate-300">
                    Message *
                  </label>
                  <textarea
                    id="message"
                    name="message"
                    required
                    rows={5}
                    value={formData.message}
                    onChange={handleChange}
                    className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent resize-none"
                    placeholder="Tell us about your project and how we can help..."
                  />
                </div>

                <button
                  type="submit"
                  className="w-full px-6 py-4 bg-gradient-to-r from-pink-500 to-pink-600 text-white rounded-xl font-bold hover:shadow-lg hover:shadow-pink-500/30 transition-all flex items-center justify-center gap-2"
                >
                  <Send className="w-5 h-5" />
                  Send Message
                </button>
              </form>
            </motion.div>

            {/* Office Information */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="space-y-8"
            >
              <div>
                <h2 className="text-2xl font-bold mb-6 text-slate-900 dark:text-white">
                  Visit Our Offices
                </h2>

                <div className="space-y-6">
                  {offices.map((office) => (
                    <div key={office.city} className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6">
                      <h3 className="font-bold text-lg mb-2 text-slate-900 dark:text-white flex items-center gap-2">
                        <MapPin className="w-5 h-5 text-pink-500" />
                        {office.city}
                      </h3>
                      <p className="text-slate-600 dark:text-slate-400 mb-3">
                        {office.address}
                      </p>
                      <p className="text-pink-600 dark:text-pink-400 font-semibold">
                        {office.phone}
                      </p>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-gradient-to-br from-pink-50 to-purple-50 dark:from-pink-500/10 dark:to-purple-500/10 border border-pink-200 dark:border-pink-500/30 rounded-xl p-6">
                <h3 className="font-bold text-lg mb-3 text-slate-900 dark:text-white flex items-center gap-2">
                  <Clock className="w-5 h-5 text-pink-500" />
                  Response Times
                </h3>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-slate-600 dark:text-slate-400">Email Support</span>
                    <span className="font-semibold text-slate-900 dark:text-white">Within 24 hours</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-600 dark:text-slate-400">Priority Support</span>
                    <span className="font-semibold text-slate-900 dark:text-white">Within 4 hours</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-600 dark:text-slate-400">Enterprise Support</span>
                    <span className="font-semibold text-slate-900 dark:text-white">Within 1 hour</span>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
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
                <li><Link href="/contact" className="hover:text-pink-500 transition-colors font-medium">Contact</Link></li>
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