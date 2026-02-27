# Task Assignment: Authentication API Implementation

**Assigned To:** Backend Engineer  
**Status:** IN PROGRESS (Database Schema Complete)  
**Priority:** High

## Objective
Implement user authentication API endpoints (register, login) with JWT token-based authentication for our secure note-taking app.

## Prerequisites
- Database schema must be finalized and migrations ready
- Prisma Client must be generatable

## Requirements
1. Set up Express server structure in `/home/cfollette18/.openclaw/workspace/team-coding/backend/src/`
2. Implement user registration endpoint (`POST /api/auth/register`)
   - Validate input (email, password, name)
   - Hash password using bcrypt
   - Create user in database
   - Return JWT token
3. Implement user login endpoint (`POST /api/auth/login`)
   - Validate credentials
   - Verify password hash
   - Return JWT token
4. Create JWT middleware for protecting routes
5. Implement user profile endpoint (`GET /api/auth/me`) protected by JWT
6. Add proper error handling and validation

## Acceptance Criteria
- [ ] Express server runs without errors
- [ ] Registration endpoint works with proper validation
- [ ] Login endpoint validates credentials and returns JWT
- [ ] JWT middleware correctly protects routes
- [ ] Profile endpoint returns authenticated user data
- [ ] All endpoints return appropriate HTTP status codes
- [ ] Password hashing uses bcrypt with proper salt rounds
- [ ] Error handling for duplicate emails, invalid credentials, etc.

## Dependencies
- Database schema completion (Database Specialist)
- Prisma Client generation

## Files to Create/Modify
- `/home/cfollette18/.openclaw/workspace/team-coding/backend/src/index.ts` - Main server file
- `/home/cfollette18/.openclaw/workspace/team-coding/backend/src/middleware/auth.ts` - JWT middleware
- `/home/cfollette18/.openclaw/workspace/team-coding/backend/src/routes/auth.ts` - Auth routes
- `/home/cfollette18/.openclaw/workspace/team-coding/backend/src/utils/validation.ts` - Input validation helpers

## Communication
Update the task board when you start. Coordinate with Database Specialist for any schema questions. Flag blockers immediately.

---
*Team Lead - 2026-02-14 14:30 CST*