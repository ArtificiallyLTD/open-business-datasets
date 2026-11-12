# US federal open contract opportunities (SAM.gov)

Solicitations, combined synopsis/solicitations, presolicitations and sources-sought notices posted on [SAM.gov](https://sam.gov) in the last 30 days that are still open for responses. Contracting officer names, emails and phone numbers are left out.

- **Rows:** 5,839
- **Files:** [`us-federal-open-opportunities.csv`](us-federal-open-opportunities.csv) and [`us-federal-open-opportunities.json`](us-federal-open-opportunities.json)
- **Refreshed:** weekly, every Monday

## Columns

| Column | Meaning |
| --- | --- |
| `noticeId` | SAM.gov notice ID |
| `title` | Notice title |
| `solicitationNumber` | Solicitation number |
| `noticeType` | Solicitation, Combined Synopsis/Solicitation, Presolicitation or Sources Sought |
| `postedDate` | Date posted |
| `responseDeadline` | Response deadline with time zone |
| `department` | Department |
| `subTier` | Sub-tier agency |
| `office` | Contracting office |
| `naicsCode` | Primary NAICS code |
| `pscCode` | Product/service code |
| `setAside` | Small-business set-aside, if any |
| `placeOfPerformanceCity` | Place of performance city (often blank in the source) |
| `placeOfPerformanceState` | Place of performance state (often blank in the source) |
| `samUrl` | Notice page on SAM.gov |

## Fresher or filtered data

Built with the [SAM.gov Contract Opportunities Scraper](https://apify.com/artificially/samgov-opportunities-scraper) on Apify. Run it yourself to filter by NAICS, agency or set-aside, include full descriptions, contacts and attachments, or get only new notices each day.
