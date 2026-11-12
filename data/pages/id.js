// Example page data. Replace plans/networks/coverage with the real source (API / CMS).
window.ROVERO_PAGE = {
  "code": "id",
  "kind": "country",
  "name": "Indonesia",
  "the": "Indonesia",
  "image": "../assets/destinations/id.svg",
  "alt": "Illustration: Balinese split gate and palms at sunset",
  "_note": "EXAMPLE DATA. Plan sizes, prices, voice/SMS bundles, local flags and networks are placeholders.",
  "_globalNote": "PLACEHOLDER country list for plans flagged global:true. Replace with the real coverage.",
  "globalCountries": ["Australia", "Austria", "Belgium", "Brazil", "Cambodia", "Canada", "Chile", "Croatia", "Czechia", "Denmark", "Egypt", "Finland", "France", "Germany", "Greece", "Hungary", "India", "Ireland", "Italy", "Japan", "Kenya", "Malaysia", "Mexico", "Morocco", "Netherlands", "New Zealand", "Norway", "Philippines", "Poland", "Portugal", "Singapore", "South Africa", "South Korea", "Spain", "Sweden", "Switzerland", "Thailand", "Turkey", "United Arab Emirates", "United Kingdom", "United States", "Vietnam"],
  "plans": {
    "data": [
      {
        "gb": "1 GB",
        "days": 7,
        "price": 3.99
      },
      {
        "gb": "3 GB",
        "days": 15,
        "price": 7.99
      },
      {
        "gb": "5 GB",
        "days": 30,
        "price": 11.99,
        "tag": "Most popular"
      },
      {
        "gb": "10 GB",
        "days": 30,
        "price": 19.99,
        "global": true
      },
      {
        "gb": "20 GB",
        "days": 30,
        "price": 32.99,
        "global": true
      },
      {
        "gb": "50 GB",
        "days": 30,
        "price": 64.99
      },
      {
        "gb": "100 MB",
        "days": 7,
        "price": 1.99,
        "more": true
      }
    ],
    "voice": [
      {
        "gb": "3 GB",
        "voice": "100 min",
        "sms": "25 SMS",
        "days": 15,
        "price": 11.99,
        "global": true,
        "number": { "country": "France", "code": "+33" }
      },
      {
        "gb": "5 GB",
        "voice": "200 min",
        "sms": "50 SMS",
        "days": 30,
        "price": 17.99,
        "tag": "Most popular",
        "local": true
      },
      {
        "gb": "10 GB",
        "voice": "300 min",
        "sms": "75 SMS",
        "days": 30,
        "price": 26.99,
        "local": true
      },
      {
        "gb": "20 GB",
        "voice": "Unlimited min",
        "sms": "100 SMS",
        "days": 30,
        "price": 39.99,
        "global": true,
        "number": { "country": "France", "code": "+33" }
      }
    ],
    "unlimited": [
      {
        "gb": "Unlimited",
        "perDay": "2 GB/day",
        "days": 3,
        "price": 14.99
      },
      {
        "gb": "Unlimited",
        "perDay": "2 GB/day",
        "days": 7,
        "price": 27.99,
        "tag": "Most popular"
      },
      {
        "gb": "Unlimited",
        "perDay": "2 GB/day",
        "days": 15,
        "price": 49.99
      }
    ]
  },
  "networks": [
    {
      "name": "Local partner networks",
      "tech": "4G / 5G"
    }
  ],
  "unlimitedNote": {
    "strong": "2 GB of high-speed data every day.",
    "text": " After that, speed reduces to 1 MB/s."
  },
  "related": [
    {
      "label": "Japan",
      "href": "destination.html?d=jp",
      "image": "../assets/destinations/jp.svg"
    },
    {
      "label": "Netherlands",
      "href": "destination.html?d=nl",
      "image": "../assets/destinations/nl.svg"
    },
    {
      "label": "Europe",
      "href": "destination.html?d=eu",
      "image": "../assets/destinations/eu.svg"
    }
  ],
  "relatedTitle": "One eSIM, many trips",
  "relatedText": "Add a plan for your next destination and track all your data in one dashboard."
};
