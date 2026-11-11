# Fictional data package

This directory contains no real customers, confidential bank information, internal
policies, or proprietary business rules.

`synthetic/` is a deterministic 100-customer slice of the fictional dataset created by
`business-banking-rm-intelligence-hub`. It retains January 2024 through December 2025
history and consistent customer identifiers across all seven CSV files. The slice contains
50 customers with at least one December 2025 retention or product-gap signal and 50
additional customers selected in stable source order for comparison.

`knowledge/` contains the five fictional policy and product documents used by
`business-banking-rag-knowledge-assist`. They are simplified portfolio examples and must
not be treated as real banking guidance.

The copied artifacts make this repository independently runnable. The source projects
remain the authoritative locations for the complete fictional portfolio generator and RAG
pipeline.
