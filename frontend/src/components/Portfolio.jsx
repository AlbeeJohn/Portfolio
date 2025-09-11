import React, { useState, useEffect, Suspense, memo } from 'react';
import SEOHead from './SEOHead';
import { InteractiveBackground, FloatingElements, injectFloatingStyles } from './InteractiveBackground';
import PerformanceMonitor from './PerformanceMonitor';
import errorTracker, { trackEvent } from '../utils/errorTracking';
import axios from 'axios';

// Lazy load components for better performance
const Header = React.lazy(() => import('./Header'));
const Hero = React.lazy(() => import('./Hero'));
const About = React.lazy(() => import('./About'));
const Skills = React.lazy(() => import('./Skills'));
const Experience = React.lazy(() => import('./Experience'));
const Projects = React.lazy(() => import('./Projects'));
const Contact = React.lazy(() => import('./Contact'));
const Footer = React.lazy(() => import('./Footer'));

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Memoized loading component
const LoadingSpinner = memo(() => (
  <div className="min-h-screen bg-gray-900 flex items-center justify-center relative">
    <InteractiveBackground />
    <div className="text-center relative z-10">
      <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-blue-500 mx-auto mb-4"></div>
      <p className="text-gray-300 text-lg heading-font">Loading portfolio...</p>
      <p className="text-gray-500 text-sm mt-2 body-font">Preparing an amazing experience...</p>
    </div>
  </div>
));

// Memoized error component
const ErrorDisplay = memo(({ error, onRetry }) => (
  <div className="min-h-screen bg-gray-900 flex items-center justify-center relative">
    <InteractiveBackground />
    <div className="text-center relative z-10">
      <div className="text-red-400 text-6xl mb-4">⚠️</div>
      <p className="text-red-400 text-lg mb-4 heading-font">{error}</p>
      <button 
        onClick={onRetry}
        className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-2 rounded-lg transition-colors duration-300 body-font"
      >
        Retry
      </button>
    </div>
  </div>
));

// Component loading fallback
const ComponentFallback = memo(({ name = 'Component' }) => (
  <div className="flex items-center justify-center py-8">
    <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
    <span className="ml-2 text-gray-400">Loading {name}...</span>
  </div>
));

const Portfolio = memo(() => {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [retryCount, setRetryCount] = useState(0);

  const loadData = async (isRetry = false) => {
    if (isRetry) {
      setRetryCount(prev => prev + 1);
      trackEvent('portfolio_retry', { retryCount: retryCount + 1 });
    }
    
    setIsLoading(true);
    setError(null);
    
    const startTime = performance.now();
    
    try {
      const response = await axios.get(`${API}/portfolio`, {
        timeout: 10000, // 10 second timeout
        headers: {
          'Cache-Control': 'max-age=1800', // 30 minutes cache
        }
      });
      
      const loadTime = performance.now() - startTime;
      
      setData(response.data);
      setError(null);
      
      // Track successful load
      trackEvent('portfolio_loaded', { 
        loadTime: Math.round(loadTime),
        retryCount 
      });
      
      console.log(`✅ Portfolio loaded in ${Math.round(loadTime)}ms`);
      
    } catch (err) {
      const loadTime = performance.now() - startTime;
      const errorMessage = err.response?.status === 404 
        ? 'Portfolio data not found. Please contact the administrator.'
        : err.response?.status >= 500
        ? 'Server error. Please try again later.'
        : err.code === 'ECONNABORTED'
        ? 'Request timed out. Please check your connection.'
        : 'Failed to load portfolio data. Please try again later.';
      
      console.error('Failed to fetch portfolio data:', err);
      errorTracker.track(err, { 
        api: 'portfolio',
        loadTime: Math.round(loadTime),
        retryCount 
      });
      
      setError(errorMessage);
      
      // Track error
      trackEvent('portfolio_error', { 
        error: err.message,
        status: err.response?.status,
        retryCount 
      });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    // Inject floating animation styles
    injectFloatingStyles();
    
    // Load data
    loadData();
    
    // Preload critical resources
    const preloadImage = (src) => {
      const link = document.createElement('link');
      link.rel = 'preload';
      link.as = 'image';
      link.href = src;
      document.head.appendChild(link);
    };
    
    // Preload common images (example)
    // preloadImage('/path-to-profile-image.jpg');
    
  }, []);

  const handleRetry = () => loadData(true);

  // Loading state
  if (isLoading) {
    return <LoadingSpinner />;
  }

  // Error state
  if (error) {
    return <ErrorDisplay error={error} onRetry={handleRetry} />;
  }

  // Main render
  return (
    <>
      <SEOHead 
        title={`${data.personal?.name || 'Albee John'} - ${data.personal?.tagline || 'Data Analysis & Science Enthusiast'} | Portfolio`}
        description={`${data.personal?.description || 'Passionate about transforming raw data into actionable insights through advanced analytics, machine learning, and data-driven decision making.'} Located in ${data.personal?.location || 'Kollam, Kerala'}. Contact: ${data.personal?.email || 'albeejohnwwe@gmail.com'}`}
      />
      
      <div className="min-h-screen bg-gray-900 text-white relative">
        <InteractiveBackground />
        <FloatingElements />
        
        <div className="relative z-10">
          <Suspense fallback={<ComponentFallback name="Navigation" />}>
            <Header />
          </Suspense>
          
          <main role="main">
            <Suspense fallback={<ComponentFallback name="Hero Section" />}>
              <Hero data={data.personal} />
            </Suspense>
            
            <Suspense fallback={<ComponentFallback name="About Section" />}>
              <About data={data.personal} />
            </Suspense>
            
            <Suspense fallback={<ComponentFallback name="Skills Section" />}>
              <Skills data={data.skills} />
            </Suspense>
            
            <Suspense fallback={<ComponentFallback name="Experience Section" />}>
              <Experience data={data.experience} />
            </Suspense>
            
            <Suspense fallback={<ComponentFallback name="Projects Section" />}>
              <Projects data={data.projects} />
            </Suspense>
            
            <Suspense fallback={<ComponentFallback name="Contact Section" />}>
              <Contact data={data.contact} />
            </Suspense>
          </main>
          
          <Suspense fallback={<ComponentFallback name="Footer" />}>
            <Footer />
          </Suspense>
        </div>
      </div>
      
      {/* Performance Monitor (development only) */}
      <PerformanceMonitor enabled={process.env.NODE_ENV === 'development'} />
    </>
  );
});

export default Portfolio;