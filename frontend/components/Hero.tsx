export function Hero() {
  return (
    <section className="pt-36 pb-20 px-12 max-w-6xl mx-auto">
      <h1 className="text-5xl font-bold text-center leading-tight tracking-tight mb-4 text-slate-900">
        Your AI has no idea who your customers are.
      </h1>
      <p className="text-xl text-center text-teal-600 mb-16">
        We fix that.
      </p>

      <div className="grid grid-cols-2 gap-8 mb-12">
        {/* Generic AI Card */}
        <div className="bg-slate-50 border border-slate-200 rounded-2xl p-6 opacity-90">
          <div className="text-xs font-bold uppercase tracking-widest text-slate-400 mb-5">
            Generic AI
          </div>
          <div className="flex flex-col gap-4">
            <div className="bg-slate-100 text-slate-900 px-5 py-4 rounded-xl text-sm">
              What&apos;s our return policy for enterprise clients?
            </div>
            <div className="bg-slate-200 text-slate-500 px-5 py-4 rounded-xl text-sm">
              Our standard enterprise return policy typically follows industry norms of 30-90 days. We aim to accommodate all customer needs on a case-by-case basis.
            </div>
          </div>
          <div className="mt-6 pt-6 border-t border-slate-200 flex flex-col gap-3">
            <div className="flex items-center gap-3 text-sm text-slate-400 font-medium">
              <span>✗</span> No company data
            </div>
            <div className="flex items-center gap-3 text-sm text-slate-400 font-medium">
              <span>✗</span> Generic response
            </div>
            <div className="flex items-center gap-3 text-sm text-slate-400 font-medium">
              <span>✗</span> No citations
            </div>
          </div>
          <div className="mt-6 pt-4 border-t border-slate-200 text-xs text-slate-400 font-medium">
            Source: Unknown
          </div>
        </div>

        {/* Namakan Card */}
        <div className="bg-white border-2 border-teal-600 rounded-2xl p-6 shadow-lg shadow-teal-600/10">
          <div className="text-xs font-bold uppercase tracking-widest text-teal-600 mb-5">
            Namakan
          </div>
          <div className="flex flex-col gap-4">
            <div className="bg-slate-50 text-slate-900 px-5 py-4 rounded-xl text-sm">
              What&apos;s our return policy for enterprise clients?
            </div>
            <div className="bg-teal-50 text-slate-900 border border-teal-200 px-5 py-4 rounded-xl text-sm">
              Based on your Contract Template v2.3 Section 4.2: Enterprise clients receive a 2-week acceptance period, followed by 90-day warranty. After warranty, credits are issued at management discretion.
            </div>
          </div>
          <div className="mt-6 pt-6 border-t border-slate-200 flex flex-col gap-3">
            <div className="flex items-center gap-3 text-sm text-teal-600 font-medium">
              <span>✓</span> From Contract v2.3
            </div>
            <div className="flex items-center gap-3 text-sm text-teal-600 font-medium">
              <span>✓</span> Exact policy cited
            </div>
            <div className="flex items-center gap-3 text-sm text-teal-600 font-medium">
              <span>✓</span> Your brand voice
            </div>
          </div>
          <div className="mt-6 pt-4 border-t border-slate-200 text-xs text-teal-600 font-medium">
            Source: Your Knowledge Base
          </div>
        </div>
      </div>

      <div className="flex justify-center">
        <button className="bg-teal-600 text-white text-base font-semibold px-8 py-4 rounded-lg hover:bg-teal-700 hover:-translate-y-0.5 transition-all cursor-pointer">
          Talk to Us →
        </button>
      </div>
    </section>
  )
}
