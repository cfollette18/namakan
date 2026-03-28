"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";
import {
  Home,
  LayoutDashboard,
  ShoppingBag,
  Settings,
  User,
  LogOut,
  Bell,
  Search
} from "lucide-react";
import ThemeToggle from "@/components/ThemeToggle";

export default function AuthenticatedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();

  const navItems = [
    { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
    { href: "/marketplace", label: "Marketplace", icon: ShoppingBag },
    { href: "/settings", label: "Settings", icon: Settings },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      {/* Top Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-950/80 backdrop-blur-xl border-b border-pink-500/20">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <Link href="/dashboard" className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-pink-500 to-pink-600 rounded-xl flex items-center justify-center">
                <span className="text-white font-bold text-xl">N</span>
              </div>
              <span className="text-2xl font-bold bg-gradient-to-r from-pink-500 to-pink-600 text-transparent bg-clip-text">
                Namakan
              </span>
            </Link>

            {/* Search Bar */}
            <div className="hidden md:flex flex-1 max-w-xl mx-12">
              <div className="relative w-full">
                <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input
                  type="text"
                  placeholder="Search projects, agents, templates..."
                  className="w-full bg-slate-900/50 border border-slate-700 rounded-xl py-3 pl-12 pr-4 text-white placeholder-slate-500 focus:outline-none focus:border-pink-500/50 focus:ring-2 focus:ring-pink-500/20"
                />
              </div>
            </div>

            {/* Right Side Actions */}
            <div className="flex items-center gap-3">
              <ThemeToggle />
              <button className="p-2 rounded-xl bg-slate-900/50 border border-slate-700 hover:border-pink-500/50 transition-all relative">
                <Bell className="w-5 h-5 text-slate-400" />
                <span className="absolute top-1 right-1 w-2 h-2 bg-pink-500 rounded-full"></span>
              </button>

              <div className="relative group">
                <button className="p-2 rounded-xl bg-slate-900/50 border border-slate-700 hover:border-pink-500/50 transition-all flex items-center gap-2">
                  <User className="w-5 h-5 text-pink-400" />
                  <span className="hidden md:block text-sm font-medium">John Doe</span>
                </button>

                {/* Dropdown Menu */}
                <div className="absolute right-0 mt-2 w-48 bg-slate-900 border border-slate-700 rounded-xl shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all">
                  <Link
                    href="/settings"
                    className="flex items-center gap-3 px-4 py-3 hover:bg-slate-800 transition-colors first:rounded-t-xl"
                  >
                    <Settings className="w-4 h-4 text-slate-400" />
                    <span>Settings</span>
                  </Link>
                  <Link
                    href="/"
                    className="flex items-center gap-3 px-4 py-3 hover:bg-slate-800 transition-colors"
                  >
                    <Home className="w-4 h-4 text-slate-400" />
                    <span>Home</span>
                  </Link>
                  <button
                    className="flex items-center gap-3 px-4 py-3 hover:bg-slate-800 transition-colors w-full text-left last:rounded-b-xl text-slate-400 hover:text-pink-400"
                  >
                    <LogOut className="w-4 h-4" />
                    <span>Sign Out</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Side Navigation */}
      <aside className="fixed left-0 top-20 bottom-0 w-64 bg-slate-900/50 backdrop-blur border-r border-pink-500/20 p-6 hidden lg:block">
        <nav className="space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href || pathname.startsWith(item.href + '/');

            return (
              <Link key={item.href} href={item.href}>
                <motion.div
                  whileHover={{ scale: 1.02, x: 4 }}
                  whileTap={{ scale: 0.98 }}
                  className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
                    isActive
                      ? "bg-gradient-to-r from-pink-500 to-pink-600 text-white shadow-lg shadow-pink-500/30"
                      : "text-slate-400 hover:text-white hover:bg-slate-800"
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="font-medium">{item.label}</span>
                </motion.div>
              </Link>
            );
          })}
        </nav>

        {/* Quick Actions */}
        <div className="mt-8 p-4 bg-gradient-to-br from-pink-500/10 to-pink-600/10 border border-pink-500/30 rounded-xl">
          <h3 className="text-sm font-semibold text-pink-400 mb-3">Quick Actions</h3>
          <div className="space-y-2">
            <Link href="/dashboard?action=new-project">
              <button className="w-full text-left px-3 py-2 text-sm text-slate-300 hover:text-white hover:bg-slate-800 rounded-lg transition-colors">
                + New Project
              </button>
            </Link>
            <Link href="/marketplace?action=browse">
              <button className="w-full text-left px-3 py-2 text-sm text-slate-300 hover:text-white hover:bg-slate-800 rounded-lg transition-colors">
                🔍 Browse Agents
              </button>
            </Link>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="lg:ml-64 pt-20">
        {children}
      </main>

      {/* Mobile Bottom Navigation */}
      <nav className="fixed bottom-0 left-0 right-0 lg:hidden bg-slate-950/95 backdrop-blur border-t border-pink-500/20 z-50">
        <div className="flex items-center justify-around py-3">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;

            return (
              <Link key={item.href} href={item.href}>
                <motion.div
                  whileTap={{ scale: 0.9 }}
                  className={`flex flex-col items-center gap-1 px-4 py-2 ${
                    isActive ? "text-pink-500" : "text-slate-400"
                  }`}
                >
                  <Icon className="w-6 h-6" />
                  <span className="text-xs font-medium">{item.label}</span>
                </motion.div>
              </Link>
            );
          })}
        </div>
      </nav>
    </div>
  );
}
