# Case Study: Fintech Feature Adoption Analytics

## Problem Statement
A UPI/wallet fintech needed to understand:
- Which features drive user engagement?
- Where is the biggest drop-off in user journey?
- How to increase feature adoption?

## Solution
Built an analytics pipeline from scratch:
1. **Generated** synthetic dataset (10K users, 51K events)
2. **Loaded** into SQLite with 10 pre-built views
3. **Created** 3-page Power BI dashboard

## Key Findings
| Finding | Impact |
|---------|--------|
| AutoPay users have 5× transactions | Highest-leverage feature |
| KYC drop-off: 2,190 users | ₹79L annual revenue leak |
| 4-feature users spend 9.3× more | Feature adoption drives revenue |

## Recommendations
1. AutoPay onboarding prompt → ₹28L impact
2. Rewards nudge → ₹14L impact  
3. UPI Lite education → ₹10L impact

## Tools Used
Python · SQLite · Power BI · GitHub
