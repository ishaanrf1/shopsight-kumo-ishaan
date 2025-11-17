/**
 * SearchBar component for natural language product search
 * Features autocomplete and displays search results
 */
import { useState } from 'react'
import { searchProducts } from '../services/api'

export default function SearchBar({ onProductSelect, disabled }) {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [searching, setSearching] = useState(false)
  const [showResults, setShowResults] = useState(false)

  /**
   * Handle search submission
   */
  const handleSearch = async (e) => {
    e.preventDefault()
    
    if (!query.trim() || disabled) return

    setSearching(true)
    setShowResults(true)

    try {
      const data = await searchProducts(query, 10)
      setResults(data.results || [])
    } catch (error) {
      console.error('Search error:', error)
      setResults([])
    } finally {
      setSearching(false)
    }
  }

  /**
   * Handle product selection from results
   */
  const handleSelectProduct = (product) => {
    onProductSelect(product)
    setQuery('')
    setResults([])
    setShowResults(false)
  }

  /**
   * Handle input change
   */
  const handleInputChange = (e) => {
    setQuery(e.target.value)
    if (!e.target.value.trim()) {
      setResults([])
      setShowResults(false)
    }
  }

  return (
    <div className="relative">
      {/* Search Form */}
      <form onSubmit={handleSearch} className="relative">
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <svg 
              className="h-5 w-5 text-gray-400" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" 
              />
            </svg>
          </div>
          
          <input
            type="text"
            value={query}
            onChange={handleInputChange}
            placeholder="Search for products (e.g., 'running shoes', 'winter jacket')"
            disabled={disabled || searching}
            className="block w-full pl-12 pr-32 py-4 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
          />
          
          <div className="absolute inset-y-0 right-0 pr-2 flex items-center">
            <button
              type="submit"
              disabled={disabled || searching || !query.trim()}
              className="px-6 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              {searching ? 'Searching...' : 'Search'}
            </button>
          </div>
        </div>
      </form>

      {/* Search Results Dropdown */}
      {showResults && results.length > 0 && (
        <div className="absolute z-10 mt-2 w-full bg-white rounded-lg shadow-lg border border-gray-200 max-h-96 overflow-y-auto">
          <div className="p-2">
            <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide px-3 py-2">
              {results.length} {results.length === 1 ? 'Result' : 'Results'}
            </div>
            {results.map((product) => (
              <button
                key={product.article_id}
                onClick={() => handleSelectProduct(product)}
                className="w-full text-left px-3 py-3 hover:bg-gray-50 rounded-md transition-colors"
              >
                <div className="font-medium text-gray-900">{product.name}</div>
                {product.category && (
                  <div className="text-sm text-gray-600 mt-1">{product.category}</div>
                )}
                {product.description && (
                  <div className="text-xs text-gray-500 mt-1">{product.description}</div>
                )}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* No Results Message */}
      {showResults && !searching && results.length === 0 && query.trim() && (
        <div className="absolute z-10 mt-2 w-full bg-white rounded-lg shadow-lg border border-gray-200 p-4">
          <p className="text-gray-600 text-center">
            No products found for "{query}". Try a different search term.
          </p>
        </div>
      )}
    </div>
  )
}

