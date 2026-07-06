# Tracker Dedupe Index

Generated: 2026-06-06T11:44:20.214Z

## Scope

- Tabs scanned: `Agencies`, `Direct Employers`, `WhatsApp Other`, `Applied`, `Follow Ups`, `Needs Email Research`.
- Normalization: company names lowercased and punctuation-stripped; email addresses lowercased; domains taken from company/email cells only, with `www.` removed; phones kept only when explicitly labeled WhatsApp/phone.
- Excluded from domain matching: `Opening Source URL(s)` job-board links, because they create false joins across unrelated companies.

## Counts

- Live rows scanned: 132
- Deduped clusters: 101
- Multi-row clusters: 19
- Cross-tab clusters: 18
- Alias-only clusters: 1
- Clusters with email keys: 79
- Clusters with domain keys: 83
- Clusters with phone keys: 1

## Skip Patterns

When merging unknown-bucket rows, skip candidates that match any row in this index by company, email, domain, or labeled phone lead. The highest-risk duplicate patterns are:

- ADCB -> tabs=Direct Employers|Applied -> emails=careers@adcb.com ; domains=adcb.com
- Adecco -> tabs=Agencies|Applied|Follow Ups -> emails=adeccoae.info@adecco.com ; domains=adecco.com
- ADMS UAE -> tabs=Agencies|Applied|Follow Ups -> emails=info@admsuae.com ; domains=admsuae.com
- AECOM UAE -> tabs=Direct Employers|Needs Email Research -> domains=ae-careers.aecom.com
- AKRS -> tabs=Agencies|Applied|Follow Ups -> emails=info@akrs.ae ; domains=akrs.ae
- Al Mansoor Group -> tabs=Agencies|Applied|Follow Ups -> emails=info@almansoorgroup.com ; domains=almansoorgroup.com
- Al Nahiya -> tabs=Agencies|Applied|Follow Ups -> emails=enquiries@alnahiya.com|info@alnahiya.com ; domains=alnahiya.com
- Al Thawiya -> tabs=Agencies|Applied|Follow Ups -> emails=enquiry@al-thawiya.com ; domains=al-thawiya.com
- Al Vakil -> tabs=Agencies|Applied|Follow Ups -> emails=adminmumbai@alvakil.net|jobs@alvakil.net ; domains=alvakil.net
- Antal -> tabs=Agencies|Applied|Follow Ups -> emails=info@antal.com ; domains=antal.com
- ASRS -> tabs=Agencies|Applied|Follow Ups -> emails=info@asrs.ae ; domains=asrs.ae
- BAC Middle East -> tabs=Agencies|Applied|Follow Ups -> emails=mabel@bacme.com|recruit@bacme.com|submit@bacme.com ; domains=bacme.com
- Carrefour UAE -> tabs=Direct Employers|Needs Email Research -> domains=carrefouruaecareers.com
- Etisalat / Etisalat (e&) -> tabs=Direct Employers -> emails=careers@etisalat.ae ; domains=etisalat.ae|careers.etisalat.ae
- EVOQ (Real Estate) -> tabs=Direct Employers|WhatsApp Other -> phones=971523321256
- Majid Al Futtaim -> tabs=Direct Employers|Needs Email Research -> domains=careers.majidalfuttaim.com
- Property Finder -> tabs=Direct Employers|Applied|Follow Ups -> emails=careers@propertyfinder.ae ; domains=propertyfinder.ae
- Rotana Hotels -> tabs=Direct Employers|Needs Email Research -> domains=rotanacareers.com
- Ziina -> tabs=Direct Employers|Applied|Follow Ups -> emails=anton.badashov@ziina.com|jocelyn.meyer@ziina.com ; domains=ziina.com

## Use

- Use the CSV as the lookup table.
- Match on company first, then split semicolon-delimited emails, then compare domains, then compare labeled phone/WhatsApp numbers.
- Do not use job-board source URLs as dedupe keys.
