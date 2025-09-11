import React from 'react';
import { Helmet } from 'react-helmet-async';

const SEOHead = ({ 
  title = "Albee John - Data Analyst & Science Enthusiast | Portfolio",
  description = "Albee John - Data Analyst & Science Enthusiast passionate about transforming raw data into actionable insights through advanced analytics, data analysis, and data-driven decision making. Expertise in Python, R, SQL, Statistical Analysis, and Data Visualization.",
  keywords = "Albee John, Data Analyst, Science Enthusiast, Data Analysis, Python Developer, R Programming, SQL Expert, Statistical Analysis, Data Visualization, Business Intelligence, Analytics Professional, Kerala Data Analyst, Portfolio, Data Analysis Projects, Business Analytics",
  url = "https://albeejohn.com",
  image = "https://albeejohn.com/og-image.jpg",
  type = "website"
}) => {
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "Albee John",
    "jobTitle": "Data Analyst & Science Enthusiast",
    "description": "Passionate about transforming raw data into actionable insights through advanced analytics, data analysis, and data-driven decision making. Currently pursuing expertise in Data Analysis and advanced analytics.",
    "url": url,
    "image": image,
    "sameAs": [
      "https://linkedin.com/in/albeejohn",
      "https://github.com/albeejohn"
    ],
    "knowsAbout": [
      "Data Analysis",
      "Business Analytics", 
      "Python Programming",
      "R Programming", 
      "Statistical Analysis",
      "Data Visualization",
      "Business Intelligence",
      "Data Modeling",
      "MongoDB",
      "SQL",
      "NumPy",
      "Pandas", 
      "Excel",
      "Tableau",
      "Power BI",
      "Google Analytics"
    ],
    "alumniOf": {
      "@type": "EducationalOrganization",
      "name": "St. Thomas College Of Engineering & Technology"
    },
    "address": {
      "@type": "PostalAddress",
      "addressLocality": "Kollam",
      "addressRegion": "Kerala",
      "addressCountry": "India"
    },
    "email": "albeejohnwwe@gmail.com",
    "telephone": "+91 8943785705"
  };

  return (
    <Helmet>
      {/* Basic Meta Tags */}
      <title>{title}</title>
      <meta name="description" content={description} />
      <meta name="keywords" content={keywords} />
      <meta name="author" content="Albee John" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <meta name="robots" content="index, follow" />
      <link rel="canonical" href={url} />

      {/* Open Graph Tags */}
      <meta property="og:type" content={type} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:url" content={url} />
      <meta property="og:image" content={image} />
      <meta property="og:image:width" content="1200" />
      <meta property="og:image:height" content="630" />
      <meta property="og:site_name" content="Albee John Portfolio" />
      <meta property="og:locale" content="en_US" />

      {/* Twitter Card Tags */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={image} />
      <meta name="twitter:creator" content="@albeejohn" />

      {/* Additional SEO Tags */}
      <meta name="theme-color" content="#1f2937" />
      <meta name="msapplication-TileColor" content="#1f2937" />
      <meta name="application-name" content="Albee John Portfolio" />
      <meta name="mobile-web-app-capable" content="yes" />
      <meta name="apple-mobile-web-app-capable" content="yes" />
      <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
      <meta name="format-detection" content="telephone=no" />
      <meta name="subject" content="Data Analyst & Science Enthusiast Portfolio" />
      <meta name="rating" content="general" />
      <meta name="referrer" content="no-referrer-when-downgrade" />
      
      {/* Geographic Tags */}
      <meta name="geo.region" content="IN-KL" />
      <meta name="geo.placename" content="Kollam, Kerala" />
      <meta name="geo.position" content="8.8932;76.6141" />
      <meta name="ICBM" content="8.8932, 76.6141" />
      
      {/* Language Tags */}
      <meta name="language" content="English" />
      <meta httpEquiv="content-language" content="en-us" />
      
      {/* Cache Control */}
      <meta name="revisit-after" content="7 days" />
      <meta name="expires" content="never" />
      <meta name="distribution" content="web" />
      <meta name="target" content="all" />
      <meta name="audience" content="all" />
      <meta name="resource-type" content="document" />
      <meta name="classification" content="business" />
      
      {/* Structured Data */}
      <script type="application/ld+json">
        {JSON.stringify(structuredData)}
      </script>
      
      {/* Preconnect to external domains */}
      <link rel="preconnect" href="https://fonts.googleapis.com" />
      <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="true" />
      
      {/* DNS Prefetch */}
      <link rel="dns-prefetch" href="//fonts.googleapis.com" />
      <link rel="dns-prefetch" href="//fonts.gstatic.com" />
    </Helmet>
  );
};

export default SEOHead;