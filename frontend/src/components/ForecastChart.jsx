/**
 * ForecastChart component - displays demand forecast
 * Shows predictions with confidence intervals
 */
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Area, ComposedChart } from 'recharts'

export default function ForecastChart({ data }) {
  if (!data || !data.forecast || data.forecast.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Demand Forecast</h3>
        <p className="text-gray-500">No forecast data available</p>
      </div>
    )
  }

  // Format data for Recharts
  const chartData = data.forecast.map(point => ({
    date: new Date(point.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    predicted: point.predicted_units,
    lower: point.confidence_lower,
    upper: point.confidence_upper
  }))

  // Custom tooltip
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-semibold text-gray-900">{payload[0].payload.date}</p>
          <p className="text-sm text-purple-600">
            Predicted: {payload[0].value.toFixed(1)} units
          </p>
          <p className="text-xs text-gray-500">
            Range: {payload[0].payload.lower.toFixed(1)} - {payload[0].payload.upper.toFixed(1)}
          </p>
        </div>
      )
    }
    return null
  }

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Demand Forecast</h3>
        <p className="text-sm text-gray-600 mt-1">Next 30 days (Mocked)</p>
      </div>

      {/* Info Badge */}
      <div className="mb-4 inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
        <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
        </svg>
        Method: {data.method.replace(/_/g, ' ')}
      </div>

      {/* Chart */}
      <ResponsiveContainer width="100%" height={300}>
        <ComposedChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis 
            dataKey="date" 
            tick={{ fontSize: 12 }}
            stroke="#9ca3af"
          />
          <YAxis 
            tick={{ fontSize: 12 }}
            stroke="#9ca3af"
            label={{ value: 'Units', angle: -90, position: 'insideLeft', style: { fontSize: 12 } }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          
          {/* Confidence interval area */}
          <Area
            type="monotone"
            dataKey="upper"
            stroke="none"
            fill="#c4b5fd"
            fillOpacity={0.3}
            name="Upper Bound"
          />
          <Area
            type="monotone"
            dataKey="lower"
            stroke="none"
            fill="#c4b5fd"
            fillOpacity={0.3}
            name="Lower Bound"
          />
          
          {/* Prediction line */}
          <Line 
            type="monotone" 
            dataKey="predicted" 
            stroke="#8b5cf6" 
            strokeWidth={3}
            dot={{ fill: '#8b5cf6', r: 4 }}
            name="Predicted Units"
          />
        </ComposedChart>
      </ResponsiveContainer>

      {/* Note */}
      <div className="mt-4 text-xs text-gray-500 italic">
        * Forecast is generated using historical patterns. Confidence intervals widen over time.
      </div>
    </div>
  )
}

