// Define a list of common ad element classes or IDs
const adSelectors = [
    'iframe[src*="ads"]', // Common ad iframe source
    'div[class*="ad"]',    // Div elements with "ad" in their class name
    'img[src*="banner"]',  // Banner ad images
  ];
  
  // Function to hide elements that match the ad selectors
  function blockAds() {
    adSelectors.forEach(selector => {
      const ads = document.querySelectorAll(selector);
      ads.forEach(ad => {
        ad.style.display = 'none'; // Hide the ad
      });
    });
  }
  
  // Run the blockAds function when the page loads
  window.onload = blockAds;
  