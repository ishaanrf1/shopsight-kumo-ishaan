/**
 * Main App component for ShopSight Analytics Dashboard
 * Orchestrates the search flow and displays analytics panels
 */
import { useState } from 'react'
import SearchBar from './components/SearchBar'
import SalesChart from './components/SalesChart'
import ForecastChart from './components/ForecastChart'
import InsightsPanel from './components/InsightsPanel'
import SegmentsPanel from './components/SegmentsPanel'
import { searchProducts, getProductSales, getProductForecast, getCustomerSegments, generateInsights } from './services/api'

function App() {
  // State management
  const [selectedProduct, setSelectedProduct] = useState(null)
  const [salesData, setSalesData] = useState(null)
  const [forecastData, setForecastData] = useState(null)
  const [insights, setInsights] = useState(null)
  const [segments, setSegments] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  /**
   * Handle product selection from search results
   * Fetches all analytics data for the selected product
   */
  const handleProductSelect = async (product) => {
    setSelectedProduct(product)
    setLoading(true)
    setError(null)

    try {
      // Fetch all data in parallel for better performance
      const [sales, forecast, segmentsData, insightsData] = await Promise.all([
        getProductSales(product.article_id, 90),
        getProductForecast(product.article_id, 30),
        getCustomerSegments(product.article_id),
        generateInsights(product.article_id)
      ])

      setSalesData(sales)
      setForecastData(forecast)
      setSegments(segmentsData)
      setInsights(insightsData)
    } catch (err) {
      console.error('Error fetching product data:', err)
      setError('Failed to load product analytics. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  /**
   * Clear selection and reset to search view
   */
  const handleClearSelection = () => {
    setSelectedProduct(null)
    setSalesData(null)
    setForecastData(null)
    setInsights(null)
    setSegments(null)
    setError(null)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900">
              ShopSight Analytics
            </h1>
            <div className="text-sm text-gray-500">
              AI-Powered E-commerce Insights
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search Bar */}
        <div className="mb-8">
          <SearchBar 
            onProductSelect={handleProductSelect}
            disabled={loading}
          />
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-red-800">{error}</p>
          </div>
        )}

        {/* Empty State */}
        {!selectedProduct && !loading && (
          <div className="text-center py-16">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-full mb-4">
              <svg className="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">
              Search for a product to get started
            </h2>
            <p className="text-gray-600">
              Try searching for "running shoes", "jacket", or any product type
            </p>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="text-center py-16">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mb-4"></div>
            <p className="text-gray-600">Loading analytics...</p>
          </div>
        )}

        {/* Analytics Dashboard */}
        {selectedProduct && !loading && (
          <div className="space-y-6">
            {/* Product Header */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-start justify-between">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">
                    {selectedProduct.name}
                  </h2>
                  {selectedProduct.category && (
                    <p className="text-gray-600">
                      {selectedProduct.category}
                    </p>
                  )}
                  {selectedProduct.description && (
                    <p className="text-sm text-gray-500 mt-1">
                      {selectedProduct.description}
                    </p>
                  )}
                </div>
                <button
                  onClick={handleClearSelection}
                  className="text-gray-400 hover:text-gray-600 transition-colors"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>

            {/* Charts Row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {salesData && (
                <SalesChart data={salesData} />
              )}
              {forecastData && (
                <ForecastChart data={forecastData} />
              )}
            </div>

            {/* Insights Panel */}
            {insights && (
              <InsightsPanel insights={insights} />
            )}

            {/* Segments Panel */}
            {segments && (
              <SegmentsPanel segments={segments} />
            )}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="mt-16 py-8 border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm text-gray-500">
          ShopSight Analytics - Powered by AI
        </div>
      </footer>
    </div>
  )
}

export default App

