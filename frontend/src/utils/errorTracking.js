class ErrorTracker {
  constructor() {
    this.errors = [];
    this.maxErrors = 50;
    this.init();
  }

  init() {
    // Global error handler
    window.addEventListener('error', (event) => {
      this.logError({
        type: 'javascript',
        message: event.message,
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno,
        stack: event.error?.stack,
        timestamp: new Date().toISOString(),
        url: window.location.href
      });
    });

    // Promise rejection handler
    window.addEventListener('unhandledrejection', (event) => {
      this.logError({
        type: 'promise',
        message: event.reason?.message || 'Unhandled promise rejection',
        stack: event.reason?.stack,
        timestamp: new Date().toISOString(),
        url: window.location.href
      });
    });

    // React Error Boundary handler
    window.addEventListener('react-error', (event) => {
      this.logError({
        type: 'react',
        message: event.detail?.message || 'React error',
        componentStack: event.detail?.componentStack,
        stack: event.detail?.stack,
        timestamp: new Date().toISOString(),
        url: window.location.href
      });
    });
  }

  logError(error) {
    // Add to errors array
    this.errors.unshift(error);
    
    // Keep only recent errors
    if (this.errors.length > this.maxErrors) {
      this.errors = this.errors.slice(0, this.maxErrors);
    }

    // Console log in development
    if (process.env.NODE_ENV === 'development') {
      console.group('🚨 Error Tracked');
      console.error('Message:', error.message);
      console.error('Type:', error.type);
      console.error('Stack:', error.stack);
      console.error('Full Error:', error);
      console.groupEnd();
    }

    // In production, send to monitoring service
    if (process.env.NODE_ENV === 'production') {
      this.sendToMonitoringService(error);
    }
  }

  async sendToMonitoringService(error) {
    try {
      // In a real application, send to your monitoring service
      // Example: Sentry, LogRocket, Bugsnag, etc.
      
      const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
      
      await fetch(`${BACKEND_URL}/api/errors`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          error,
          userAgent: navigator.userAgent,
          timestamp: new Date().toISOString(),
          sessionId: this.getSessionId()
        })
      });
    } catch (e) {
      console.warn('Failed to send error to monitoring service:', e);
    }
  }

  getSessionId() {
    let sessionId = localStorage.getItem('session_id');
    if (!sessionId) {
      sessionId = Math.random().toString(36).substring(2, 15);
      localStorage.setItem('session_id', sessionId);
    }
    return sessionId;
  }

  getRecentErrors(limit = 10) {
    return this.errors.slice(0, limit);
  }

  clearErrors() {
    this.errors = [];
  }

  // Method to manually track errors
  track(error, context = {}) {
    this.logError({
      type: 'manual',
      message: error.message || error.toString(),
      stack: error.stack,
      context,
      timestamp: new Date().toISOString(),
      url: window.location.href
    });
  }
}

// Create global instance
const errorTracker = new ErrorTracker();

// Export for manual error tracking
export default errorTracker;

// Helper function for React components
export const trackError = (error, context) => {
  errorTracker.track(error, context);
};

// Analytics helper
export const trackEvent = (eventName, properties = {}) => {
  if (process.env.NODE_ENV === 'development') {
    console.log('📊 Event Tracked:', eventName, properties);
  }
  
  // In production, send to analytics service
  if (process.env.NODE_ENV === 'production') {
    // Example: Google Analytics, Mixpanel, etc.
    try {
      if (window.gtag) {
        window.gtag('event', eventName, properties);
      }
    } catch (e) {
      console.warn('Failed to track event:', e);
    }
  }
};