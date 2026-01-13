# Architecture Overview – Phase 1

# Commit:
# Initial commit: enterprise LLM governance system with frontend and backend

## Objective
Establish an end-to-end system where a user can submit a business question
and receive a governance decision from a backend service.

## High-Level Architecture

Frontend (React)
    ↓ HTTP POST
Backend API (FastAPI)
    ↓
Governance Engine (placeholder logic)

## Components

### Frontend
- React-based UI
- Collects:
  - prompt_version
  - business_question
- Displays:
  - risk level
  - approval status
  - explanations

### Backend
- FastAPI server
- Exposes /evaluate endpoint
- Handles CORS and request validation

## Outcome
- Verified full frontend ↔ backend connectivity
- Established project skeleton for enterprise governance system
