interface ProductCardProps {
  tag: string
  title: string
  description: string
  features: string[]
  price: string
  priceHighlight?: string
}

export function ProductCard({ tag, title, description, features, price, priceHighlight }: ProductCardProps) {
  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-8 hover:border-teal-600 hover:shadow-lg hover:shadow-teal-600/10 transition-all">
      <span className="inline-block bg-teal-100 text-teal-600 text-xs font-semibold px-3 py-1 rounded-full mb-4">
        {tag}
      </span>
      <h3 className="text-xl font-semibold text-slate-900 mb-3">{title}</h3>
      <p className="text-slate-500 text-sm mb-4 leading-relaxed">{description}</p>
      <div className="flex flex-col gap-2 mb-4">
        {features.map((feature, index) => (
          <div key={index} className="flex items-center gap-2 text-sm">
            <span className="text-teal-600 font-semibold">✓</span>
            <span className="text-slate-600">{feature}</span>
          </div>
        ))}
      </div>
      <div className="mt-4 pt-4 border-t border-slate-100">
        <span className="text-sm text-slate-400">
          {price}
        </span>
      </div>
    </div>
  )
}
