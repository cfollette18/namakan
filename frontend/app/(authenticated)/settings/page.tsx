"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { User, Bell, Shield, CreditCard, Key, Globe, Save } from "lucide-react";

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState("profile");

  const tabs = [
    { id: "profile", label: "Profile", icon: User },
    { id: "notifications", label: "Notifications", icon: Bell },
    { id: "security", label: "Security", icon: Shield },
    { id: "billing", label: "Billing", icon: CreditCard },
    { id: "api", label: "API Keys", icon: Key },
    { id: "preferences", label: "Preferences", icon: Globe },
  ];

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-teal-500 to-teal-600 text-transparent bg-clip-text">
            Settings
          </h1>
          <p className="text-slate-400 text-lg">Manage your account and preferences</p>
        </motion.div>

        {/* Tabs & Content */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar Tabs */}
          <div className="lg:col-span-1">
            <div className="bg-slate-900/50 backdrop-blur border border-teal-500/20 rounded-xl p-2">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                      activeTab === tab.id
                        ? "bg-gradient-to-r from-teal-500 to-teal-600 text-white"
                        : "text-slate-400 hover:text-white hover:bg-slate-800"
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span className="font-medium">{tab.label}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Content Area */}
          <div className="lg:col-span-3">
            <div className="bg-slate-900/50 backdrop-blur border border-teal-500/20 rounded-xl p-8">
              {activeTab === "profile" && <ProfileSettings />}
              {activeTab === "notifications" && <NotificationSettings />}
              {activeTab === "security" && <SecuritySettings />}
              {activeTab === "billing" && <BillingSettings />}
              {activeTab === "api" && <APISettings />}
              {activeTab === "preferences" && <PreferencesSettings />}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function ProfileSettings() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-2">Profile Settings</h2>
        <p className="text-slate-400">Update your personal information</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium mb-2">Full Name</label>
          <input
            type="text"
            defaultValue="John Doe"
            className="w-full bg-slate-900/50 border border-slate-700 rounded-xl py-3 px-4 text-white focus:outline-none focus:border-teal-500/50 focus:ring-2 focus:ring-teal-500/20"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-2">Email</label>
          <input
            type="email"
            defaultValue="john@example.com"
            className="w-full bg-slate-900/50 border border-slate-700 rounded-xl py-3 px-4 text-white focus:outline-none focus:border-teal-500/50 focus:ring-2 focus:ring-teal-500/20"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-2">Company</label>
          <input
            type="text"
            placeholder="Your company"
            className="w-full bg-slate-900/50 border border-slate-700 rounded-xl py-3 px-4 text-white focus:outline-none focus:border-teal-500/50 focus:ring-2 focus:ring-teal-500/20"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-2">Industry</label>
          <select className="w-full bg-slate-900/50 border border-slate-700 rounded-xl py-3 px-4 text-white focus:outline-none focus:border-teal-500/50 focus:ring-2 focus:ring-teal-500/20">
            <option>Technology</option>
            <option>Finance</option>
            <option>Healthcare</option>
            <option>Retail</option>
            <option>Other</option>
          </select>
        </div>
      </div>

      <button className="px-6 py-3 bg-gradient-to-r from-teal-500 to-teal-600 rounded-xl font-semibold hover:shadow-lg hover:shadow-teal-500/50 transition-all flex items-center gap-2">
        <Save className="w-4 h-4" />
        Save Changes
      </button>
    </div>
  );
}

function NotificationSettings() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-2">Notification Preferences</h2>
        <p className="text-slate-400">Choose how you want to be notified</p>
      </div>

      <div className="space-y-4">
        {[
          { label: "Agent completed tasks", description: "Get notified when agents finish their work" },
          { label: "Checkpoint approvals", description: "Alerts when your approval is needed" },
          { label: "Project updates", description: "Status updates on your projects" },
          { label: "Weekly summary", description: "Weekly digest of your activity" },
        ].map((item) => (
          <div key={item.label} className="flex items-start justify-between p-4 bg-slate-800/50 rounded-xl">
            <div className="flex-1">
              <h3 className="font-semibold mb-1">{item.label}</h3>
              <p className="text-sm text-slate-400">{item.description}</p>
            </div>
            <input
              type="checkbox"
              defaultChecked
              className="w-5 h-5 rounded border-slate-700 bg-slate-900 text-teal-500 focus:ring-teal-500/20"
            />
          </div>
        ))}
      </div>
    </div>
  );
}

function SecuritySettings() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-2">Security</h2>
        <p className="text-slate-400">Manage your account security</p>
      </div>

      <div className="space-y-4">
        <div className="p-4 bg-slate-800/50 rounded-xl">
          <h3 className="font-semibold mb-2">Change Password</h3>
          <button className="px-4 py-2 bg-teal-500/20 border border-teal-500/30 rounded-lg text-teal-400 hover:bg-teal-500/30 transition-colors">
            Update Password
          </button>
        </div>

        <div className="p-4 bg-slate-800/50 rounded-xl">
          <h3 className="font-semibold mb-2">Two-Factor Authentication</h3>
          <p className="text-sm text-slate-400 mb-3">Add an extra layer of security to your account</p>
          <button className="px-4 py-2 bg-teal-500/20 border border-teal-500/30 rounded-lg text-teal-400 hover:bg-teal-500/30 transition-colors">
            Enable 2FA
          </button>
        </div>
      </div>
    </div>
  );
}

function BillingSettings() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-2">Billing</h2>
        <p className="text-slate-400">Manage your subscription and billing</p>
      </div>

      <div className="p-6 bg-gradient-to-r from-teal-500/10 to-teal-600/10 border border-teal-500/30 rounded-xl">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-xl font-bold">Pro Plan</h3>
            <p className="text-slate-400">$49/month</p>
          </div>
          <span className="px-3 py-1 bg-teal-500/20 text-teal-400 rounded-full text-sm font-semibold">
            Active
          </span>
        </div>
        <p className="text-sm text-slate-400 mb-4">Next billing date: February 18, 2026</p>
        <button className="px-4 py-2 bg-slate-800 rounded-lg hover:bg-slate-700 transition-colors">
          Manage Subscription
        </button>
      </div>
    </div>
  );
}

function APISettings() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-2">API Keys</h2>
        <p className="text-slate-400">Manage your API access tokens</p>
      </div>

      <button className="px-4 py-2 bg-gradient-to-r from-teal-500 to-teal-600 rounded-lg font-semibold">
        Generate New API Key
      </button>

      <div className="p-4 bg-slate-800/50 rounded-xl">
        <p className="text-sm text-slate-400">No API keys yet</p>
      </div>
    </div>
  );
}

function PreferencesSettings() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-2">Preferences</h2>
        <p className="text-slate-400">Customize your Namakan experience</p>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">Language</label>
          <select className="w-full bg-slate-900/50 border border-slate-700 rounded-xl py-3 px-4 text-white focus:outline-none focus:border-teal-500/50 focus:ring-2 focus:ring-teal-500/20">
            <option>English</option>
            <option>Spanish</option>
            <option>French</option>
            <option>German</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Timezone</label>
          <select className="w-full bg-slate-900/50 border border-slate-700 rounded-xl py-3 px-4 text-white focus:outline-none focus:border-teal-500/50 focus:ring-2 focus:ring-teal-500/20">
            <option>UTC-8 (Pacific Time)</option>
            <option>UTC-5 (Eastern Time)</option>
            <option>UTC+0 (GMT)</option>
            <option>UTC+1 (Central European Time)</option>
          </select>
        </div>
      </div>
    </div>
  );
}
