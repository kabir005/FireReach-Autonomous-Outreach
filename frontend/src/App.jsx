import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [formData, setFormData] = useState({
    icp_description: '',
    company_name: '',
    recipient_email: ''
  })
  
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [signalFilter, setSignalFilter] = useState('All')
  const [sessionMetrics, setSessionMetrics] = useState({
    signalsHarvested: 0,
    briefsGenerated: 0,
    emailsSent: 0,
    avgTime: 0
  })
  const [startTime, setStartTime] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)
    setStartTime(Date.now())

    try {
      const response = await axios.post(`${API_URL}/api/firereach`, formData)
      setResult(response.data)
      
      const endTime = Date.now()
      const duration = ((endTime - startTime) / 1000).toFixed(1)
      
      setSessionMetrics(prev => ({
        signalsHarvested: prev.signalsHarvested + (response.data.signals?.length || 0),
        briefsGenerated: prev.briefsGenerated + 1,
        emailsSent: prev.emailsSent + (response.data.send_status === 'sent' ? 1 : 0),
        avgTime: duration
      }))
    } catch (err) {
      setError(err.response?.data?.detail || err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setResult(null)
    setError(null)
    setFormData({ icp_description: '', company_name: '', recipient_email: '' })
  }

  const getStepStatus = (step) => {
    if (!result) return 'pending'
    if (result.error && result.current_step === step) return 'error'
    
    const steps = ['harvesting_signals', 'generating_brief', 'sending_email']
    const currentIndex = steps.indexOf(result.current_step)
    const stepIndex = steps.indexOf(step)
    
    if (stepIndex < currentIndex || result.current_step === 'completed') return 'completed'
    if (stepIndex === currentIndex && loading) return 'active'
    return 'pending'
  }

  const filteredSignals = result?.signals?.filter(s => 
    signalFilter === 'All' || s.type.toLowerCase() === signalFilter.toLowerCase()
  ) || []

  const progressPercentage = loading ? 
    (result?.current_step === 'harvesting_signals' ? 33 : 
     result?.current_step === 'generating_brief' ? 66 : 100) : 
    (result ? 100 : 0)

  return (
    <div className="min-h-screen bg-dark text-white">
      {/* Animated Background */}
      <div className="fixed inset-0 bg-gradient-mesh opacity-30 animate-gradient"></div>
      
      {/* Header */}
      <header className="relative border-b border-border backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="text-5xl animate-pulse-slow">🔥</span>
              <div>
                <h1 className="text-4xl font-bold bg-gradient-to-r from-fire-orange to-fire-amber bg-clip-text text-transparent">
                  FireReach
                </h1>
                <p className="text-sm bg-gradient-to-r from-fire-orange to-fire-amber bg-clip-text text-transparent font-medium">
                  Autonomous Outreach. Zero Templates.
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-sm text-gray-400">Agent Ready</span>
            </div>
          </div>
        </div>
        <div className="h-px bg-gradient-to-r from-transparent via-fire-orange to-transparent"></div>
      </header>

      {/* Metrics Bar */}
      <div className="relative bg-card-dark border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <MetricCard icon="🔥" label="Signals Harvested" value={sessionMetrics.signalsHarvested} />
            <MetricCard icon="🧠" label="Briefs Generated" value={sessionMetrics.briefsGenerated} />
            <MetricCard icon="✉️" label="Emails Sent" value={sessionMetrics.emailsSent} />
            <MetricCard icon="⚡" label="Avg. Time" value={`${sessionMetrics.avgTime}s`} />
          </div>
        </div>
      </div>

      <main className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Panel */}
          <div className="space-y-6">
            <div className="bg-card rounded-xl shadow-2xl p-6 border border-border glow-card">
              <h2 className="text-2xl font-semibold mb-6 flex items-center gap-2">
                🎯 <span>Mission Control</span>
              </h2>
              
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Ideal Customer Profile (ICP)
                  </label>
                  <textarea
                    value={formData.icp_description}
                    onChange={(e) => setFormData({...formData, icp_description: e.target.value})}
                    className="w-full px-4 py-3 bg-dark border border-border rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo focus:border-transparent transition-all"
                    rows="4"
                    placeholder="e.g. We sell cybersecurity training to Series B startups scaling their engineering teams"
                    required
                  />
                  <div className="text-xs text-gray-500 mt-1">
                    {formData.icp_description.length} characters
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Target Company Name
                  </label>
                  <div className="relative">
                    <span className="absolute left-3 top-3 text-gray-500">🏢</span>
                    <input
                      type="text"
                      value={formData.company_name}
                      onChange={(e) => setFormData({...formData, company_name: e.target.value})}
                      className="w-full pl-10 pr-4 py-3 bg-dark border border-border rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo focus:border-transparent transition-all"
                      placeholder="e.g., Wiz"
                      required
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Recipient Email
                  </label>
                  <div className="relative">
                    <span className="absolute left-3 top-3 text-gray-500">✉️</span>
                    <input
                      type="email"
                      value={formData.recipient_email}
                      onChange={(e) => setFormData({...formData, recipient_email: e.target.value})}
                      className="w-full pl-10 pr-4 py-3 bg-dark border border-border rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo focus:border-transparent transition-all"
                      placeholder="prospect@company.com"
                      required
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full h-14 bg-gradient-to-r from-fire-orange to-fire-amber hover:shadow-fire disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition-all duration-300 flex items-center justify-center gap-2 shimmer"
                >
                  {loading ? (
                    <>
                      <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                      <span>Running Agent...</span>
                    </>
                  ) : (
                    <>
                      <span>🚀</span>
                      <span>Launch FireReach</span>
                    </>
                  )}
                </button>

                <p className="text-xs text-gray-500 text-center">
                  ⚡ Powered by Groq AI + Live Web Signals
                </p>
              </form>

              {error && (
                <div className="mt-6 bg-red-900/30 border border-red-700 rounded-lg p-4 animate-fade-in">
                  <p className="text-red-200 text-sm">{error}</p>
                </div>
              )}

              {result && (
                <button
                  onClick={handleReset}
                  className="w-full mt-4 py-2 border border-border rounded-lg text-gray-400 hover:text-white hover:border-indigo transition-all"
                >
                  🔄 Reset / New Mission
                </button>
              )}
            </div>
          </div>

          {/* Right Panel */}
          <div className="space-y-6 max-h-screen overflow-y-auto custom-scrollbar">
            {/* Agent Progress */}
            <div className="bg-card rounded-xl shadow-2xl p-6 border border-border glow-card animate-fade-in">
              <h2 className="text-2xl font-semibold mb-4">Agent Progress</h2>
              
              {/* Progress Bar */}
              <div className="h-1 bg-dark rounded-full mb-6 overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-fire-orange to-fire-amber transition-all duration-500"
                  style={{ width: `${progressPercentage}%` }}
                ></div>
              </div>
              
              <div className="space-y-4">
                <StepIndicator
                  icon="🔍"
                  title="Harvesting Signals"
                  description="Fetching live buyer intent data"
                  status={getStepStatus('harvesting_signals')}
                  subtitle={result?.signals ? `✓ ${result.signals.length} signals found across ${new Set(result.signals.map(s => s.type)).size} categories` : null}
                />
                <StepIndicator
                  icon="🧠"
                  title="Generating Brief"
                  description="AI-powered account analysis"
                  status={getStepStatus('generating_brief')}
                  subtitle={result?.pain_points ? `✓ Account brief generated — ${result.pain_points.length} pain points identified` : null}
                />
                <StepIndicator
                  icon="✉️"
                  title="Sending Outreach"
                  description="Drafting & dispatching email"
                  status={getStepStatus('sending_email')}
                  subtitle={result?.message_id ? `✓ Email sent to ${formData.recipient_email} — Message ID: ${result.message_id}` : null}
                />
              </div>
            </div>

            {/* Results */}
            {result && (
              <>
                {/* Signals */}
                {result.signals && result.signals.length > 0 && (
                  <div className="bg-card rounded-xl shadow-2xl p-6 border border-border animate-fade-in">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-xl font-semibold">🔍 Harvested Signals</h3>
                      <span className="text-xs font-semibold px-3 py-1 rounded-full bg-indigo/20 text-indigo border border-indigo/30">
                        {result.signals.length} found
                      </span>
                    </div>
                    
                    {/* Filter Pills */}
                    <div className="flex flex-wrap gap-2 mb-4">
                      {['All', 'Funding', 'Hiring', 'Leadership', 'Tech Stack', 'News'].map(filter => (
                        <button
                          key={filter}
                          onClick={() => setSignalFilter(filter)}
                          className={`px-3 py-1 rounded-full text-xs font-medium transition-all ${
                            signalFilter === filter
                              ? 'bg-indigo text-white'
                              : 'bg-dark text-gray-400 hover:text-white border border-border'
                          }`}
                        >
                          {filter}
                        </button>
                      ))}
                    </div>

                    <div className="space-y-3 max-h-96 overflow-y-auto custom-scrollbar">
                      {filteredSignals.map((signal, idx) => (
                        <SignalCard key={idx} signal={signal} />
                      ))}
                    </div>
                  </div>
                )}

                {/* Account Brief */}
                {result.account_brief && (
                  <div className="bg-card rounded-xl shadow-2xl p-6 border border-border animate-fade-in">
                    <h3 className="text-xl font-semibold mb-4">🧠 Account Intelligence</h3>
                    <div className="border-l-4 border-fire-orange pl-4 mb-4">
                      <p className="text-gray-300 whitespace-pre-line leading-relaxed">{result.account_brief}</p>
                    </div>
                    
                    {result.pain_points && result.pain_points.length > 0 && (
                      <div className="mb-4">
                        <h4 className="text-sm font-semibold text-gray-400 mb-2">Pain Points:</h4>
                        <div className="flex flex-wrap gap-2">
                          {result.pain_points.map((point, idx) => (
                            <span key={idx} className="px-3 py-1 bg-indigo/20 text-indigo rounded-full text-sm border border-indigo/30">
                              {point}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    <div>
                      <h4 className="text-sm font-semibold text-gray-400 mb-2">Strategic Fit Score</h4>
                      <div className="flex items-center gap-3">
                        <div className="flex-1 h-2 bg-dark rounded-full overflow-hidden">
                          <div className="h-full bg-gradient-to-r from-fire-orange to-fire-amber" style={{ width: '85%' }}></div>
                        </div>
                        <span className="text-sm font-semibold text-fire-amber">85%</span>
                      </div>
                      <p className="text-xs text-gray-500 mt-1">ICP Alignment</p>
                    </div>
                  </div>
                )}

                {/* Email Preview */}
                {result.email_subject && (
                  <div className="bg-card rounded-xl shadow-2xl p-6 border border-border animate-fade-in">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-xl font-semibold">📧 Outreach Draft</h3>
                      <span className={`text-xs font-semibold px-3 py-1 rounded-full ${
                        result.send_status === 'sent'
                          ? 'bg-green-900/30 text-green-400 border border-green-700'
                          : 'bg-red-900/30 text-red-400 border border-red-700'
                      }`}>
                        {result.send_status === 'sent' ? 'Sent ✓' : 'Failed ✗'}
                      </span>
                    </div>

                    <div className="bg-dark rounded-lg p-4 space-y-3 border border-border">
                      <div className="flex items-center gap-2 text-sm pb-2 border-b border-border">
                        <span className="text-gray-500">To:</span>
                        <span className="text-white">{formData.recipient_email}</span>
                      </div>
                      <div className="flex items-center gap-2 text-sm pb-2 border-b border-border">
                        <span className="text-gray-500">From:</span>
                        <span className="text-white">FireReach by Rabbitt AI</span>
                      </div>
                      <div className="flex items-center gap-2 text-sm pb-3 border-b border-border">
                        <span className="text-gray-500">Subject:</span>
                        <span className="text-white font-medium">{result.email_subject}</span>
                      </div>
                      <div className="pt-2">
                        <p className="text-gray-300 whitespace-pre-line leading-relaxed">{result.email_body}</p>
                      </div>
                    </div>

                    <div className="flex gap-2 mt-4">
                      <button
                        onClick={() => navigator.clipboard.writeText(result.email_body)}
                        className="flex-1 py-2 border border-border rounded-lg text-sm text-gray-400 hover:text-white hover:border-indigo transition-all"
                      >
                        📋 Copy Email
                      </button>
                      {result.message_id && (
                        <button
                          onClick={() => alert(`Message ID: ${result.message_id}`)}
                          className="flex-1 py-2 border border-border rounded-lg text-sm text-gray-400 hover:text-white hover:border-indigo transition-all"
                        >
                          🔍 View Message ID
                        </button>
                      )}
                    </div>

                    {result.message_id && (
                      <div className="mt-3 text-xs text-gray-500 font-mono bg-dark px-3 py-2 rounded border border-border">
                        {result.message_id}
                      </div>
                    )}
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}

function MetricCard({ icon, label, value }) {
  return (
    <div className="bg-card rounded-lg p-3 border border-border">
      <div className="flex items-center gap-2 mb-1">
        <span className="text-xl">{icon}</span>
        <span className="text-xs text-gray-500">{label}</span>
      </div>
      <div className="text-2xl font-bold text-white">{value}</div>
    </div>
  )
}

function StepIndicator({ icon, title, description, status, subtitle }) {
  const statusStyles = {
    pending: 'bg-dark border-border',
    active: 'bg-indigo/10 border-indigo glow-indigo',
    completed: 'bg-green-900/20 border-green-600 glow-green',
    error: 'bg-red-900/20 border-red-600'
  }

  const statusIcons = {
    pending: <span className="text-gray-600">⏳</span>,
    active: <div className="animate-spin text-indigo">⚡</div>,
    completed: <span className="text-green-500">✓</span>,
    error: <span className="text-red-500">✗</span>
  }

  return (
    <div className={`border-2 rounded-lg p-4 transition-all duration-300 ${statusStyles[status]}`}>
      <div className="flex items-center gap-3">
        <span className="text-2xl">{icon}</span>
        <div className="flex-1">
          <h3 className="text-white font-medium">{title}</h3>
          <p className="text-gray-400 text-sm">{description}</p>
          {subtitle && status === 'completed' && (
            <p className="text-green-400 text-xs mt-1">{subtitle}</p>
          )}
        </div>
        <div className="text-xl">{statusIcons[status]}</div>
      </div>
    </div>
  )
}

function SignalCard({ signal }) {
  const typeColors = {
    funding: 'bg-green-900/30 text-green-400 border-green-700',
    hiring: 'bg-blue-900/30 text-blue-400 border-blue-700',
    leadership: 'bg-purple-900/30 text-purple-400 border-purple-700',
    'tech stack': 'bg-indigo-900/30 text-indigo-400 border-indigo-700',
    news: 'bg-gray-700/30 text-gray-400 border-gray-600'
  }

  const borderColors = {
    funding: 'border-l-green-500',
    hiring: 'border-l-blue-500',
    leadership: 'border-l-purple-500',
    'tech stack': 'border-l-indigo-500',
    news: 'border-l-gray-500'
  }

  const type = signal.type.toLowerCase()
  
  return (
    <div className={`bg-dark rounded-lg p-3 border-l-4 ${borderColors[type] || 'border-l-gray-500'} hover:shadow-lg transition-all hover:-translate-y-0.5`}>
      <div className="flex items-center justify-between mb-2">
        <span className={`text-xs font-semibold px-2 py-1 rounded border ${typeColors[type] || typeColors.news}`}>
          {signal.type.toUpperCase()}
        </span>
        {signal.source_url && (
          <a
            href={signal.source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-gray-500 hover:text-fire-orange transition-colors"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
            </svg>
          </a>
        )}
      </div>
      <p className="text-sm text-gray-300">{signal.summary}</p>
    </div>
  )
}

export default App
