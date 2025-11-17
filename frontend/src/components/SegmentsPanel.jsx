/**
 * SegmentsPanel component - displays customer segmentation
 * Shows buyer personas and characteristics (mocked data)
 */
export default function SegmentsPanel({ segments }) {
  if (!segments || !segments.segments) {
    return null
  }

  // Icon for segment
  const SegmentIcon = () => (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
    </svg>
  )

  // Color for likelihood score
  const getLikelihoodColor = (likelihood) => {
    if (likelihood >= 0.75) return 'bg-green-500'
    if (likelihood >= 0.6) return 'bg-yellow-500'
    return 'bg-gray-400'
  }

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      {/* Header */}
      <div className="flex items-center mb-4">
        <div className="flex-shrink-0 w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center mr-3">
          <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
        </div>
        <div>
          <h3 className="text-lg font-semibold text-gray-900">Customer Segments</h3>
          <p className="text-sm text-gray-600">Likely buyer personas (Mocked)</p>
        </div>
      </div>

      {/* Segments */}
      <div className="space-y-4">
        {segments.segments.map((segment, index) => (
          <div 
            key={index}
            className="border border-gray-200 rounded-lg p-4 hover:border-purple-300 transition-colors"
          >
            {/* Segment Header */}
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center">
                <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center text-purple-600 mr-3">
                  <SegmentIcon />
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900">{segment.name}</h4>
                  <p className="text-sm text-gray-600">Age {segment.age_range}</p>
                </div>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-purple-600">
                  {segment.percentage.toFixed(0)}%
                </div>
                <div className="text-xs text-gray-500">of buyers</div>
              </div>
            </div>

            {/* Percentage Bar */}
            <div className="mb-3">
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-purple-600 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${segment.percentage}%` }}
                />
              </div>
            </div>

            {/* Purchase Likelihood */}
            <div className="mb-3 flex items-center">
              <span className="text-sm text-gray-600 mr-2">Purchase Likelihood:</span>
              <div className="flex items-center">
                <div className="flex space-x-1 mr-2">
                  {[...Array(5)].map((_, i) => (
                    <div
                      key={i}
                      className={`w-2 h-4 rounded ${
                        i < Math.round(segment.purchase_likelihood * 5)
                          ? getLikelihoodColor(segment.purchase_likelihood)
                          : 'bg-gray-200'
                      }`}
                    />
                  ))}
                </div>
                <span className="text-sm font-semibold text-gray-700">
                  {Math.round(segment.purchase_likelihood * 100)}%
                </span>
              </div>
            </div>

            {/* Characteristics */}
            <div>
              <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
                Characteristics
              </div>
              <div className="flex flex-wrap gap-2">
                {segment.characteristics.map((char, charIndex) => (
                  <span
                    key={charIndex}
                    className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800"
                  >
                    <svg className="w-3 h-3 mr-1 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    {char}
                  </span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Footer Note */}
      <div className="mt-4 pt-4 border-t border-gray-200">
        <p className="text-xs text-gray-500 italic">
          * Customer segments are generated based on product category and typical buyer patterns. Actual customer data would provide more accurate segmentation.
        </p>
      </div>
    </div>
  )
}

