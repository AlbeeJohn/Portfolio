import { useEffect, useState } from 'react';

export const usePerformance = () => {
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    const collectMetrics = () => {
      const navigation = performance.getEntriesByType('navigation')[0];
      const paint = performance.getEntriesByType('paint');
      
      if (navigation && paint.length > 0) {
        const fcp = paint.find(entry => entry.name === 'first-contentful-paint');
        
        setMetrics({
          loadTime: Math.round(navigation.loadEventEnd - navigation.loadEventStart),
          domContentLoaded: Math.round(navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart),
          responseTime: Math.round(navigation.responseEnd - navigation.requestStart),
          firstContentfulPaint: fcp ? Math.round(fcp.startTime) : 0,
          timestamp: Date.now()
        });
      }
    };

    // Collect metrics after page load
    if (document.readyState === 'complete') {
      collectMetrics();
    } else {
      window.addEventListener('load', collectMetrics);
    }

    return () => window.removeEventListener('load', collectMetrics);
  }, []);

  return metrics;
};

export const useResourceTiming = () => {
  const [resources, setResources] = useState([]);

  useEffect(() => {
    const getResourceTiming = () => {
      const resources = performance.getEntriesByType('resource');
      const slowResources = resources
        .filter(resource => resource.duration > 100) // Slow resources
        .map(resource => ({
          name: resource.name,
          duration: Math.round(resource.duration),
          size: resource.transferSize,
          type: resource.initiatorType
        }));
      
      setResources(slowResources);
    };

    setTimeout(getResourceTiming, 2000); // Wait for resources to load
  }, []);

  return resources;
};