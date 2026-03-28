'use client'

import { motion } from 'framer-motion'
import {
  Check,
  X,
  Zap,
  Users,
  Shield,
  Cpu,
  BarChart3,
  MessageSquare,
  HelpCircle,
  ArrowRight,
  Sparkles,
  Star,
  Crown,
  Building
} from 'lucide-react'
import Link from 'next/link'
import { useState } from 'react'

export default function PricingPage() {
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'yearly'>('monthly')

  const plans = [
    {
      name: 'Starter',
      icon: Sparkles,
      price: {
        monthly: 0,
        yearly: 0
      },
      description: 'Perfect for individuals and small teams getting started with AI agents',
      features: [
        { name: '5 projects per month', included: true },
        { name: 'Basic agent templates', included: true },
        { name: 'Community support', included: true },
        { name: 'Public marketplace access', included: true },
        { name: 'Email support', included: false },
        { name: 'Custom agent training', included: false },
        { name: 'Private agents', included: false },
        { name: 'Advanced analytics', included: false },
        { name: 'API access', included: false },
        { name: 'Dedicated infrastructure', included: false }
      ],
      cta: 'Get Started Free',
      popular: false,
      color: 'slate'
    },
    {
      name: 'Professional',
      icon: Star,
      price: {
        monthly: 49,
        yearly: 39
      },
      description: 'For growing teams and businesses scaling their AI operations',
      features: [
        { name: 'Unlimited projects', included: true },
        { name: 'All agent templates', included: true },
        { name: 'Priority email support', included: true },
        { name: 'Full marketplace access', included: true },
        { name: 'Custom agent training', included: true },
        { name: 'Private agents', included: true },
        { name: 'Advanced analytics', included: true },
        { name: 'API access', included: true },
        { name: 'Team collaboration', included: true },
        { name: 'Dedicated infrastructure', included: false }
      ],
      cta: 'Start Free Trial',
      popular: true,
      color: 'pink'
    },
    {
      name: 'Enterprise',
      icon: Crown,
      price: {
        monthly: 'Custom',
        yearly: 'Custom'
      },
      description: 'For large organizations requiring enterprise-grade AI solutions',
      features: [
        { name: 'Everything in Professional', included: true },
        { name: 'Dedicated infrastructure', included: true },
        { name: '24/7 phone support', included: true },
        { name: 'SLA guarantees', included: true },
        { name: 'Custom integrations', included: true },
        { name: 'Advanced security', included: true },
        { name: 'Single sign-on (SSO)', included: true },
        { name: 'Compliance (SOC 2, HIPAA)', included: true },
        { name: 'Custom training', included: true },
        { name: 'Dedicated account manager', included: true }
      ],
      cta: 'Contact Sales',
      popular: false,
      color: 'slate'
    }
  ]

  const faqs = [
    {
      question: 'What counts as a project?',
      answer: 'A project is any workflow or task you create with AI agents. This could be a marketing campaign, product development cycle, research analysis, or any other automated process.'
    },
    {
      question: 'Can I change plans at any time?',
      answer: 'Yes! You can upgrade or downgrade your plan at any time. Changes take effect immediately, and we\'ll prorate any billing adjustments.'
    },
    {
      question: 'What happens to my data if I cancel?',
      answer: 'Your data remains accessible for 30 days after cancellation. You can export all your projects, agents, and data during this period. After 30 days, data is permanently deleted.'
    },
    {
      question: 'Do you offer refunds?',
      answer: 'We offer a 30-day money-back guarantee for all paid plans. If you\'re not satisfied, contact our support team for a full refund.'
    },
    {
      question: 'What kind of support do you provide?',
      answer: 'Starter: Community forum. Professional: Priority email support. Enterprise: 24/7 phone and email support with dedicated account manager.'
    },
    {
      question: 'Can I have multiple team members?',
      answer: 'Professional plans include team collaboration features. Enterprise plans support unlimited team members with advanced permission controls.'
    },
    {
      question: 'What payment methods do you accept?',
      answer: 'We accept all major credit cards (Visa, Mastercard, American Express), PayPal, and wire transfers for enterprise customers.'
    },
    {
      question: 'Is there a setup fee?',
      answer: 'No setup fees! You only pay the monthly or yearly subscription. Enterprise plans may have custom terms.'
    }
  ]

  const savings = billingCycle === 'yearly' ? 20 : 0

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
                <Link href="/pricing" className="text-slate-600 dark:text-slate-300 hover:text-pink-500 transition-colors font-medium">
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
              Simple, Transparent Pricing
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="text-5xl md:text-7xl font-bold mb-6 leading-tight"
            >
              Choose Your
              <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-500 via-pink-600 to-pink-500">
                AI Power
              </span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="text-xl md:text-2xl text-slate-600 dark:text-slate-300 mb-8 max-w-2xl mx-auto"
            >
              Start free, scale as you grow. All plans include our core AI agent orchestration platform.
            </motion.p>

            {/* Billing Toggle */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="flex items-center justify-center gap-4 mb-8"
            >
              <span className={`text-lg ${billingCycle === 'monthly' ? 'text-slate-900 dark:text-white font-semibold' : 'text-slate-500'}`}>
                Monthly
              </span>
              <button
                onClick={() => setBillingCycle(billingCycle === 'monthly' ? 'yearly' : 'monthly')}
                className="relative w-16 h-8 bg-slate-200 dark:bg-slate-700 rounded-full transition-colors"
              >
                <div className={`absolute top-1 w-6 h-6 bg-white rounded-full shadow-md transition-transform ${billingCycle === 'yearly' ? 'translate-x-8' : 'translate-x-1'}`} />
              </button>
              <span className={`text-lg ${billingCycle === 'yearly' ? 'text-slate-900 dark:text-white font-semibold' : 'text-slate-500'}`}>
                Yearly
              </span>
              {billingCycle === 'yearly' && (
                <span className="px-2 py-1 bg-green-100 dark:bg-green-500/20 text-green-600 dark:text-green-400 text-sm rounded-full">
                  Save 20%
                </span>
              )}
            </motion.div>
          </div>
        </div>
      </section>

      {/* Pricing Cards */}
      <section className="pb-20 px-6">
        <div className="container mx-auto max-w-7xl">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {plans.map((plan, index) => (
              <motion.div
                key={plan.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className={`relative bg-white dark:bg-slate-900 border rounded-2xl p-8 ${
                  plan.popular
                    ? 'border-pink-500 shadow-xl shadow-pink-500/20 scale-105'
                    : 'border-slate-200 dark:border-slate-800'
                }`}
              >
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 -translate-x-1/2 px-4 py-1 bg-gradient-to-r from-pink-500 to-pink-600 rounded-full text-white text-sm font-bold">
                    Most Popular
                  </div>
                )}

                <div className="text-center mb-8">
                  <div className={`w-16 h-16 mx-auto mb-4 rounded-xl flex items-center justify-center ${
                    plan.popular
                      ? 'bg-gradient-to-br from-pink-500 to-pink-600'
                      : 'bg-slate-100 dark:bg-slate-800'
                  }`}>
                    <plan.icon className={`w-8 h-8 ${
                      plan.popular ? 'text-white' : 'text-slate-600 dark:text-slate-400'
                    }`} />
                  </div>

                  <h3 className="text-2xl font-bold mb-2 text-slate-900 dark:text-white">
                    {plan.name}
                  </h3>

                  <p className="text-slate-600 dark:text-slate-400 mb-6">
                    {plan.description}
                  </p>

                  <div className="mb-6">
                    {plan.price.monthly === 'Custom' ? (
                      <div className="text-4xl font-bold text-slate-900 dark:text-white">
                        Custom
                      </div>
                    ) : (
                      <>
                        <div className="text-4xl font-bold text-slate-900 dark:text-white">
                          ${billingCycle === 'monthly' ? plan.price.monthly : plan.price.yearly}
                        </div>
                        <div className="text-slate-500 dark:text-slate-400">
                          {typeof plan.price.monthly === 'number' && plan.price.monthly > 0 && `per ${billingCycle === 'monthly' ? 'month' : 'month, billed yearly'}`}
                        </div>
                        {billingCycle === 'yearly' && typeof plan.price.monthly === 'number' && typeof plan.price.yearly === 'number' && plan.price.monthly > 0 && (
                          <div className="text-green-600 dark:text-green-400 text-sm font-semibold mt-1">
                            Save ${(plan.price.monthly - plan.price.yearly) * 12} annually
                          </div>
                        )}
                      </>
                    )}
                  </div>
                </div>

                <ul className="space-y-3 mb-8">
                  {plan.features.map((feature) => (
                    <li key={feature.name} className="flex items-start gap-3">
                      {feature.included ? (
                        <Check className="w-5 h-5 text-pink-500 flex-shrink-0 mt-0.5" />
                      ) : (
                        <X className="w-5 h-5 text-slate-400 flex-shrink-0 mt-0.5" />
                      )}
                      <span className={`text-sm ${
                        feature.included
                          ? 'text-slate-700 dark:text-slate-300'
                          : 'text-slate-500 line-through'
                      }`}>
                        {feature.name}
                      </span>
                    </li>
                  ))}
                </ul>

                <Link href={plan.name === 'Enterprise' ? '/contact' : '/auth/signup'} className="block">
                  <button className={`w-full py-4 rounded-xl font-bold transition-all ${
                    plan.popular
                      ? 'bg-gradient-to-r from-pink-500 to-pink-600 text-white hover:shadow-lg hover:shadow-pink-500/30'
                      : 'bg-slate-900 dark:bg-slate-800 text-white hover:bg-slate-800 dark:hover:bg-slate-700'
                  }`}>
                    {plan.cta}
                  </button>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Feature Comparison Table */}
      <section className="py-20 px-6 bg-slate-50 dark:bg-slate-900/50">
        <div className="container mx-auto max-w-6xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Compare Plans
            </h2>
            <p className="text-xl text-slate-600 dark:text-slate-300">
              Find the perfect plan for your team's needs
            </p>
          </motion.div>

          <div className="overflow-x-auto">
            <table className="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl">
              <thead>
                <tr className="border-b border-slate-200 dark:border-slate-800">
                  <th className="text-left p-6 font-bold text-slate-900 dark:text-white">Features</th>
                  <th className="text-center p-6 font-bold text-slate-900 dark:text-white">Starter</th>
                  <th className="text-center p-6 font-bold text-pink-600">Professional</th>
                  <th className="text-center p-6 font-bold text-slate-900 dark:text-white">Enterprise</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { name: 'Projects per month', starter: '5', pro: 'Unlimited', enterprise: 'Unlimited' },
                  { name: 'Agent templates', starter: 'Basic', pro: 'All', enterprise: 'All + Custom' },
                  { name: 'Team members', starter: '1', pro: '10', enterprise: 'Unlimited' },
                  { name: 'API access', starter: 'No', pro: 'Yes', enterprise: 'Advanced' },
                  { name: 'Support', starter: 'Community', pro: 'Priority Email', enterprise: '24/7 Phone' },
                  { name: 'SLA', starter: 'No', pro: '99.9%', enterprise: '99.99%' },
                  { name: 'Custom integrations', starter: 'No', pro: 'Limited', enterprise: 'Unlimited' },
                  { name: 'Security compliance', starter: 'Basic', pro: 'SOC 2', enterprise: 'SOC 2 + HIPAA' }
                ].map((feature, index) => (
                  <tr key={feature.name} className="border-b border-slate-100 dark:border-slate-800">
                    <td className="p-6 font-medium text-slate-900 dark:text-white">{feature.name}</td>
                    <td className="p-6 text-center text-slate-600 dark:text-slate-400">{feature.starter}</td>
                    <td className="p-6 text-center text-pink-600 font-semibold">{feature.pro}</td>
                    <td className="p-6 text-center text-slate-600 dark:text-slate-400">{feature.enterprise}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* FAQs */}
      <section className="py-20 px-6">
        <div className="container mx-auto max-w-4xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Frequently Asked Questions
            </h2>
            <p className="text-xl text-slate-600 dark:text-slate-300">
              Everything you need to know about our pricing
            </p>
          </motion.div>

          <div className="space-y-6">
            {faqs.map((faq, index) => (
              <motion.div
                key={faq.question}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.05 }}
                className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6"
              >
                <h3 className="text-lg font-bold mb-3 text-slate-900 dark:text-white flex items-center gap-3">
                  <HelpCircle className="w-5 h-5 text-pink-500 flex-shrink-0" />
                  {faq.question}
                </h3>
                <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
                  {faq.answer}
                </p>
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
              Ready to Get Started?
            </h2>
            <p className="text-xl text-pink-100 mb-8 max-w-2xl mx-auto">
              Join thousands of teams using Namakan to automate complex workflows.
              Start free today, no credit card required.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/auth/signup">
                <button className="px-8 py-4 bg-white text-pink-600 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transition-all flex items-center gap-2">
                  <Sparkles className="w-5 h-5" />
                  Start Free Trial
                </button>
              </Link>
              <Link href="/contact">
                <button className="px-8 py-4 bg-pink-600/20 text-white border border-white/30 rounded-xl font-bold text-lg hover:bg-pink-600/30 transition-all">
                  Contact Sales
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