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

const Portfolio = () => {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Inject floating animation styles
    injectFloatingStyles();
    
    const loadData = async () => {
      setIsLoading(true);
      try {
        const response = await axios.get(`${API}/portfolio`);
        setData(response.data);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch portfolio data:', err);
        setError('Failed to load portfolio data. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    };
    
    loadData();
  }, []);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center relative">
        <InteractiveBackground />
        <div className="text-center relative z-10">
          <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-300 text-lg heading-font">Loading portfolio...</p>
          <p className="text-gray-500 text-sm mt-2 body-font">Preparing an amazing experience...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center relative">
        <InteractiveBackground />
        <div className="text-center relative z-10">
          <div className="text-red-400 text-6xl mb-4">⚠️</div>
          <p className="text-red-400 text-lg mb-4 heading-font">{error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-2 rounded-lg transition-colors duration-300 body-font"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

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
          <Header />
          <main role="main">
            <Hero data={data.personal} />
            <About data={data.personal} />
            <Skills data={data.skills} />
            <Experience data={data.experience} />
            <Projects data={data.projects} />
            <Contact data={data.contact} />
          </main>
          <Footer />
        </div>
      </div>
    </>
  );
};

export default Portfolio;