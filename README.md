# Open business datasets

Free, regularly refreshed CSV and JSON datasets of public business data, built with [Artificially's Apify Actors](https://apify.com/artificially). Download a file and open it in Excel, Google Sheets, pandas or DuckDB. No sign-up, no API key.

| Dataset | Rows | What's in it | Refreshed |
| --- | --- | --- | --- |
| [Y Combinator companies](yc-companies/) | ~6,300 | Every company in the YC directory since 2005: website, one-liner, batch, status, industry, location, team size, hiring flag, LinkedIn | Weekly |
| [EU open tenders](eu-open-tenders/) | ~22,000 | Public procurement calls still open for bids from TED (61 countries), published in the last 30 days: buyer, country, CPV codes, estimated value, deadline | Weekly |
| [US federal open opportunities](us-federal-open-opportunities/) | ~5,900 | SAM.gov solicitations, presolicitations and sources-sought notices still open for responses: agency, NAICS, PSC, set-aside, deadline | Weekly |

## Need fresher or filtered data?

These files are snapshots. To pull your own slice on demand (one NAICS code, one country, a specific YC industry) or to monitor for new items, run the Actor that built each dataset. Every Actor has a one-click example and costs a few dollars per thousand results:

- [Y Combinator Scraper](https://apify.com/artificially/ycombinator-scraper), with founders and open jobs
- [EU Tenders Scraper](https://apify.com/artificially/eu-tenders-scraper), with award winners and buyer profiles
- [SAM.gov Contract Opportunities Scraper](https://apify.com/artificially/samgov-opportunities-scraper), with full descriptions, contacts and attachments

There are also [n8n templates](https://github.com/ArtificiallyLTD/n8n-business-data-templates) that send this data to Google Sheets or Slack on a schedule.

## How the data is built

`scripts/refresh.py` runs the Actors through the Apify API and writes one CSV and one JSON per dataset. A GitHub Action reruns it every Monday. Personal contact details (names, emails, phone numbers) are left out on purpose: each row links to the original record if you need more.

## Sources and licenses

- **EU tenders:** [TED](https://ted.europa.eu), © European Union. Reuse is authorised under Commission Decision 2011/833/EU, with attribution.
- **US opportunities:** [SAM.gov](https://sam.gov). This is US federal government data in the public domain.
- **Y Combinator:** the public [YC company directory](https://www.ycombinator.com/companies). Company-level facts only, for research and analysis.

The code in this repository is MIT licensed. The data keeps the terms of its source.
