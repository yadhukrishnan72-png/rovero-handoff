// Example page data. Replace plans/networks/coverage with the real source (API / CMS).
window.ROVERO_PAGE = {
  "code": "eu",
  "kind": "region",
  "name": "Europe",
  "the": "Europe",
  "image": "../assets/destinations/eu.svg",
  "alt": "Illustration: Eiffel Tower, Colosseum, Big Ben skyline",
  "_note": "EXAMPLE DATA. Plan sizes, prices, voice/SMS bundles, local flags and networks are placeholders. Country lists come from the plan file coverage groups where noted in the README.",
  "plans": {
    "data": [
      {
        "gb": "1 GB",
        "days": 7,
        "price": 4.99,
        "coverage": "eu-30"
      },
      {
        "gb": "3 GB",
        "days": 15,
        "price": 9.99,
        "coverage": "eu-33"
      },
      {
        "gb": "5 GB",
        "days": 30,
        "price": 14.99,
        "coverage": "eu-42",
        "tag": "Most popular"
      },
      {
        "gb": "10 GB",
        "days": 30,
        "price": 24.99,
        "coverage": "eu-42",
        "local": true
      },
      {
        "gb": "20 GB",
        "days": 30,
        "price": 39.99,
        "coverage": "eu-42"
      },
      {
        "gb": "100 MB",
        "days": 7,
        "price": 1.99,
        "coverage": "eu-30",
        "more": true
      }
    ],
    "voice": [
      {
        "gb": "3 GB",
        "voice": "100 min",
        "sms": "25 SMS",
        "days": 15,
        "price": 15.99,
        "coverage": "eu-33"
      },
      {
        "gb": "5 GB",
        "voice": "200 min",
        "sms": "50 SMS",
        "days": 30,
        "price": 21.99,
        "coverage": "eu-42",
        "tag": "Most popular",
        "local": true
      },
      {
        "gb": "10 GB",
        "voice": "300 min",
        "sms": "75 SMS",
        "days": 30,
        "price": 34.99,
        "coverage": "eu-42"
      }
    ],
    "unlimited": [
      {
        "gb": "Unlimited",
        "perDay": "2 GB/day",
        "days": 3,
        "price": 19.99,
        "coverage": "eu-33"
      },
      {
        "gb": "Unlimited",
        "perDay": "2 GB/day",
        "days": 7,
        "price": 34.99,
        "coverage": "eu-42",
        "tag": "Most popular"
      },
      {
        "gb": "Unlimited",
        "perDay": "2 GB/day",
        "days": 15,
        "price": 59.99,
        "coverage": "eu-42"
      }
    ]
  },
  "coverage": {
    "eu-30": [
      "Austria",
      "Belgium",
      "Bulgaria",
      "Croatia",
      "Cyprus",
      "Czechia",
      "Denmark",
      "Estonia",
      "Finland",
      "France",
      "Germany",
      "Greece",
      "Hungary",
      "Iceland",
      "Ireland",
      "Italy",
      "Latvia",
      "Liechtenstein",
      "Lithuania",
      "Luxembourg",
      "Malta",
      "Netherlands",
      "Norway",
      "Poland",
      "Portugal",
      "Romania",
      "Slovakia",
      "Slovenia",
      "Spain",
      "Sweden",
      "Switzerland",
      "Turkey",
      "Ukraine",
      "United Kingdom"
    ],
    "eu-33": [
      "Austria",
      "Belgium",
      "Bulgaria",
      "Croatia",
      "Cyprus",
      "Czechia",
      "Denmark",
      "Estonia",
      "Finland",
      "France",
      "Germany",
      "Gibraltar",
      "Greece",
      "Hungary",
      "Iceland",
      "Ireland",
      "Italy",
      "Latvia",
      "Liechtenstein",
      "Lithuania",
      "Luxembourg",
      "Malta",
      "Netherlands",
      "Norway",
      "Poland",
      "Portugal",
      "Romania",
      "Slovakia",
      "Slovenia",
      "Spain",
      "Sweden",
      "Switzerland",
      "United Kingdom"
    ],
    "eu-42": [
      "Aland Islands",
      "Austria",
      "Belgium",
      "Bulgaria",
      "Croatia",
      "Cyprus",
      "Czechia",
      "Denmark",
      "Estonia",
      "Finland",
      "France",
      "Germany",
      "Gibraltar",
      "Greece",
      "Guernsey",
      "Hungary",
      "Iceland",
      "Ireland",
      "Isle of Man",
      "Italy",
      "Jersey",
      "Latvia",
      "Liechtenstein",
      "Lithuania",
      "Luxembourg",
      "Malta",
      "Netherlands",
      "North Macedonia",
      "Norway",
      "Poland",
      "Portugal",
      "Romania",
      "Serbia",
      "Slovakia",
      "Slovenia",
      "Spain",
      "Sweden",
      "Switzerland",
      "Turkey",
      "Ukraine",
      "United Kingdom"
    ]
  },
  "unlimitedNote": {
    "strong": "2 GB of high-speed data every day.",
    "text": " After that, speed reduces to 1 MB/s."
  },
  "related": [
    {
      "label": "Global (120+ areas)",
      "href": "/destinations/gl-120",
      "image": "../assets/destinations/gl-120.svg"
    },
    {
      "label": "Africa",
      "href": "destination.html?d=af-21",
      "image": "../assets/destinations/af-21.svg"
    },
    {
      "label": "Asia (14 areas)",
      "href": "/destinations/as-14",
      "image": "../assets/destinations/as-14.svg"
    }
  ]
};
