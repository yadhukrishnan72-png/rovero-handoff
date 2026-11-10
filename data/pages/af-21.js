// Example page data. Replace plans/networks/coverage with the real source (API / CMS).
window.ROVERO_PAGE = {
  "code": "af-21",
  "kind": "region",
  "name": "Africa",
  "the": "Africa",
  "image": "../assets/destinations/af-21.svg",
  "alt": "Illustration: Pyramids, acacia tree, palms (as in the Africa pilot)",
  "_note": "EXAMPLE DATA. Plan sizes, prices, voice/SMS bundles, local flags and networks are placeholders. Country lists come from the plan file coverage groups where noted in the README.",
  "plans": {
    "data": [
      {
        "gb": "1 GB",
        "days": 7,
        "price": 5.99,
        "coverage": "af-8"
      },
      {
        "gb": "3 GB",
        "days": 15,
        "price": 12.99,
        "coverage": "af-14"
      },
      {
        "gb": "5 GB",
        "days": 30,
        "price": 19.99,
        "coverage": "af-21",
        "tag": "Most popular"
      },
      {
        "gb": "10 GB",
        "days": 30,
        "price": 34.99,
        "coverage": "af-21",
        "local": true
      },
      {
        "gb": "20 GB",
        "days": 30,
        "price": 59.99,
        "coverage": "af-21"
      },
      {
        "gb": "100 MB",
        "days": 7,
        "price": 2.99,
        "coverage": "af-8",
        "more": true
      }
    ],
    "voice": [
      {
        "gb": "3 GB",
        "voice": "100 min",
        "sms": "25 SMS",
        "days": 15,
        "price": 17.99,
        "coverage": "af-14"
      },
      {
        "gb": "5 GB",
        "voice": "200 min",
        "sms": "50 SMS",
        "days": 30,
        "price": 26.99,
        "coverage": "af-21",
        "tag": "Most popular",
        "local": true
      },
      {
        "gb": "10 GB",
        "voice": "300 min",
        "sms": "75 SMS",
        "days": 30,
        "price": 42.99,
        "coverage": "af-21"
      }
    ],
    "unlimited": [
      {
        "gb": "Unlimited",
        "perDay": "2 GB/day",
        "days": 3,
        "price": 24.99,
        "coverage": "af-14"
      },
      {
        "gb": "Unlimited",
        "perDay": "2 GB/day",
        "days": 7,
        "price": 44.99,
        "coverage": "af-21",
        "tag": "Most popular"
      },
      {
        "gb": "Unlimited",
        "perDay": "2 GB/day",
        "days": 15,
        "price": 79.99,
        "coverage": "af-21"
      }
    ]
  },
  "coverage": {
    "af-8": [
      "Egypt",
      "Ghana",
      "Kenya",
      "Morocco",
      "Nigeria",
      "South Africa",
      "Tanzania",
      "Tunisia"
    ],
    "af-14": [
      "Egypt",
      "Ethiopia",
      "Ghana",
      "Kenya",
      "Morocco",
      "Nigeria",
      "Rwanda",
      "Senegal",
      "South Africa",
      "Tanzania",
      "Tunisia",
      "Uganda",
      "Zambia",
      "Zimbabwe"
    ],
    "af-21": [
      "Algeria",
      "Cameroon",
      "Chad",
      "Côte d’Ivoire",
      "Democratic Republic of the Congo",
      "Egypt",
      "Ethiopia",
      "Gabon",
      "Ghana",
      "Kenya",
      "Morocco",
      "Mozambique",
      "Nigeria",
      "Rwanda",
      "Senegal",
      "South Africa",
      "Tanzania",
      "Tunisia",
      "Uganda",
      "Zambia",
      "Zimbabwe"
    ]
  },
  "unlimitedNote": {
    "strong": "2 GB of high-speed data every day.",
    "text": " After that, speed reduces to 1 MB/s."
  },
  "related": [
    {
      "label": "Europe",
      "href": "destination.html?d=eu",
      "image": "../assets/destinations/eu.svg"
    },
    {
      "label": "Global (120+ areas)",
      "href": "/destinations/gl-120",
      "image": "../assets/destinations/gl-120.svg"
    },
    {
      "label": "Asia (14 areas)",
      "href": "/destinations/as-14",
      "image": "../assets/destinations/as-14.svg"
    }
  ]
};
