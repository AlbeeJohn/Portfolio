import React, { useState, useEffect } from 'react';
import { usePerformance, useResourceTiming } from '../hooks/usePerformance';

const PerformanceMonitor = ({ enabled = process.env.NODE_ENV === 'development' }) => {
  const [showPanel, setShowPanel] = useState(false);
  const [consoleErrors, setConsoleErrors] = useState([]);
  const metrics = usePerformance();
  const slowResources = useResourceTiming();

  useEffect(() => {
    if (!enabled) return;

    const originalError = console.error;
    console.error = (...args) => {
      setConsoleErrors(prev => [...prev.slice(-4), {
        message: args.join(' '),
        timestamp: new Date().toLocaleTimeString()
      }]);
      originalError.apply(console, args);
    };

    return () => {
      console.error = originalError;
    };
  }, [enabled]);

  if (!enabled) return null;

  const getPerformanceStatus = (metric, thresholds) => {
    if (!metric) return 'unknown';
    if (metric < thresholds.good) return 'good';
    if (metric < thresholds.poor) return 'needs-improvement';
    return 'poor';
  };

  return (
    <>
      {/* Performance Toggle Button */}
      <button
        onClick={() => setShowPanel(!showPanel)}
        className="fixed bottom-4 right-4 bg-blue-600 text-white p-2 rounded-full shadow-lg z-50 text-xs"
        title="Performance Monitor"
      >
        📊
      </button>

      {/* Performance Panel */}
      {showPanel && (
        <div className="fixed bottom-16 right-4 bg-gray-900 text-white p-4 rounded-lg shadow-xl z-50 max-w-sm text-xs border border-gray-700">
          <h3 className="font-bold mb-2 text-blue-400">Performance Metrics</h3>
          
          {metrics ? (
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>Load Time:</span>
                <span className={`font-mono ${
                  getPerformanceStatus(metrics.loadTime, {good: 100, poor: 500}) === 'good' 
                    ? 'text-green-400' 
                    : getPerformanceStatus(metrics.loadTime, {good: 100, poor: 500}) === 'needs-improvement'
                    ? 'text-yellow-400'
                    : 'text-red-400'
                }`}>
                  {metrics.loadTime}ms
                </span>
              </div>
              
              <div className="flex justify-between">
                <span>DOM Ready:</span>
                <span className="font-mono text-blue-400">
                  {metrics.domContentLoaded}ms
                </span>
              </div>
              
              <div className="flex justify-between">
                <span>Response:</span>
                <span className="font-mono text-green-400">
                  {metrics.responseTime}ms
                </span>
              </div>

              {metrics.firstContentfulPaint > 0 && (
                <div className="flex justify-between">
                  <span>FCP:</span>
                  <span className={`font-mono ${
                    getPerformanceStatus(metrics.firstContentfulPaint, {good: 1800, poor: 3000}) === 'good'
                      ? 'text-green-400'
                      : 'text-yellow-400'
                  }`}>
                    {metrics.firstContentfulPaint}ms
                  </span>
                </div>
              )}
            </div>
          ) : (
            <div className="text-gray-400">Loading metrics...</div>
          )}

          {/* Slow Resources */}
          {slowResources.length > 0 && (
            <div className="mt-4">
              <h4 className="font-bold text-yellow-400 mb-1">Slow Resources:</h4>
              {slowResources.slice(0, 3).map((resource, index) => (
                <div key={index} className="text-xs text-gray-300">
                  {resource.name.split('/').pop()} - {resource.duration}ms
                </div>
              ))}
            </div>
          )}

          {/* Console Errors */}
          {consoleErrors.length > 0 && (
            <div className="mt-4">
              <h4 className="font-bold text-red-400 mb-1">Recent Errors:</h4>
              {consoleErrors.slice(-2).map((error, index) => (
                <div key={index} className="text-xs text-red-300 truncate">
                  {error.timestamp}: {error.message}
                </div>
              ))}
            </div>
          )}

          <div className="mt-3 text-xs text-gray-500 border-t border-gray-700 pt-2">
            Updated: {metrics ? new Date(metrics.timestamp).toLocaleTimeString() : 'N/A'}
          </div>
        </div>
      )}
    </>
  );
};

export default React.memo(PerformanceMonitor);