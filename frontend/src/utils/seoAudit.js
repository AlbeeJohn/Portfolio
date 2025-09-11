// SEO Audit Script
const runSEOAudit = () => {
  const audit = {
    title: document.title,
    metaDescription: document.querySelector('meta[name="description"]')?.content,
    headings: {
      h1: document.querySelectorAll('h1').length,
      h2: document.querySelectorAll('h2').length,
      h3: document.querySelectorAll('h3').length,
    },
    images: {
      total: document.querySelectorAll('img').length,
      withAlt: document.querySelectorAll('img[alt]').length,
      withoutAlt: document.querySelectorAll('img:not([alt])').length,
    },
    links: {
      internal: document.querySelectorAll('a[href^="#"], a[href^="/"], a[href*="' + window.location.hostname + '"]').length,
      external: document.querySelectorAll('a[href^="http"]:not([href*="' + window.location.hostname + '"])').length,
      nofollow: document.querySelectorAll('a[rel*="nofollow"]').length,
    },
    structuredData: document.querySelectorAll('script[type="application/ld+json"]').length,
    performance: {
      loadTime: performance.timing?.loadEventEnd - performance.timing?.navigationStart,
      domReady: performance.timing?.domContentLoadedEventEnd - performance.timing?.navigationStart,
    },
    accessibility: {
      skipLinks: document.querySelectorAll('a[href^="#main"], a[href^="#content"]').length,
      landmarks: document.querySelectorAll('main, nav, header, footer, aside, section[aria-label]').length,
    },
    social: {
      openGraph: document.querySelectorAll('meta[property^="og:"]').length,
      twitter: document.querySelectorAll('meta[name^="twitter:"]').length,
    }
  };
  
  console.log('🔍 SEO Audit Results:', audit);
  return audit;
};

// Run on page load
if (typeof window !== 'undefined') {
  window.addEventListener('load', runSEOAudit);
}

export default runSEOAudit;