interface ProductCardProps {
  tag: string
  title: string
  description: string
  features: string[]
  price: string
}

export function ProductCard({ tag, title, description, features, price }: ProductCardProps) {
  return (
    <div className="product-card">
      <span className="product-tag">{tag}</span>
      <h3 className="product-title">{title}</h3>
      <p className="product-desc">{description}</p>
      <div className="product-features">
        {features.map((feature, index) => (
          <div key={index} className="product-feature">
            <span className="product-feature-check">✓</span>
            <span>{feature}</span>
          </div>
        ))}
      </div>
      <div className="product-price">{price}</div>
    </div>
  )
}
