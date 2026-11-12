# EU open public tenders (TED)

Contract notices published on [TED](https://ted.europa.eu) (Tenders Electronic Daily) in the last 30 days whose submission deadline has not passed yet. Covers the EU, EEA and other countries that publish on TED. Collected one publication day at a time, with up to 1,000 notices per day, so on the busiest weekdays some notices are missing; use the Actor below for complete results on a narrower filter.

- **Rows:** 22,000
- **Files:** [`eu-open-tenders.csv`](eu-open-tenders.csv) and [`eu-open-tenders.json`](eu-open-tenders.json)
- **Refreshed:** weekly, every Monday

## Columns

| Column | Meaning |
| --- | --- |
| `noticeId` | TED notice ID |
| `publicationDate` | Publication date |
| `submissionDeadline` | Deadline for tenders |
| `title` | Title (English where available) |
| `titleOriginal` | Title in the original language |
| `buyer` | Contracting authority |
| `country` | Buyer country |
| `countryCode` | ISO country code |
| `city` | Buyer city |
| `contractType` | Works, supplies or services |
| `procedureType` | Open, restricted, negotiated and so on |
| `mainCpvCode` | Main CPV code |
| `cpvCodes` | All CPV codes, separated by "; " |
| `estimatedValue` | Estimated value, when published |
| `currency` | Currency of the value |
| `numberOfLots` | Number of lots |
| `url` | Notice page on TED |

## Fresher or filtered data

Built with the [EU Tenders Scraper](https://apify.com/artificially/eu-tenders-scraper) on Apify. Run it yourself to filter by keyword, country, CPV code or value, or get awarded contracts with the winners.
