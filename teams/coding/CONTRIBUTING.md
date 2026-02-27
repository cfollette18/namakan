# Contributing Guidelines

## Team Collaboration Workflow

### Git Branch Strategy
We follow GitFlow-inspired workflow:

- **`main`** - Production-ready code. Protected branch.
- **`develop`** - Integration branch for features. Protected branch.
- **`feature/*`** - Feature branches (e.g., `feature/auth-api`, `feature/note-ui`)
- **`hotfix/*`** - Critical bug fixes for production
- **`release/*`** - Release preparation branches

### Creating a New Feature
1. Create branch from `develop`:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. Make commits following conventions (see below)
3. Push branch and create Pull Request to `develop`
4. Request review from relevant specialists
5. Address review comments
6. Once approved, merge via "Squash and Merge"

### Commit Message Convention
We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semi-colons, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks, dependencies, tooling

**Examples:**
```
feat(auth): implement JWT-based authentication
fix(api): resolve CORS issue with frontend
docs(db): update database schema documentation
refactor(notes): simplify note creation logic
```

### Pull Request Guidelines
1. **Title:** Use conventional commit format
2. **Description:** 
   - What changes were made
   - Why they were made
   - Testing performed
   - Screenshots for UI changes
3. **Linked Issues:** Reference issue numbers (e.g., `Closes #12`)
4. **Reviewers:** Tag relevant specialists based on changes

### Code Review Process
1. **Frontend changes:** Review by Frontend Architect
2. **Backend changes:** Review by Backend Engineer  
3. **Database changes:** Review by Database Specialist
4. **Cross-cutting changes:** Review by multiple specialists
5. **Team Lead:** Final approval for merges to `develop`

### Testing Requirements
- Backend: Unit tests for business logic
- Frontend: Component tests for UI logic
- Integration: End-to-end tests for critical flows
- All tests must pass before merge

### Development Environment
```bash
# Backend
cd backend
npm install
cp .env.example .env  # Edit with your values
npm run dev

# Frontend  
cd frontend
npm install
npm run dev

# Database
docker-compose up -d
npx prisma migrate dev
```

### Specialist Responsibilities

#### Backend Engineer
- API endpoints and business logic
- Authentication/authorization
- Database queries via Prisma
- Input validation and error handling

#### Frontend Architect
- React components and hooks
- State management
- UI/UX implementation
- API integration

#### Database Specialist
- Prisma schema design
- Migrations
- Query optimization
- Data modeling decisions

#### AI Workflow Designer
- Automated testing workflows
- Code review automation
- Development tooling
- CI/CD enhancements

#### Steve Jobs Ideation Engineer
- Product vision alignment
- UX simplicity reviews
- Feature prioritization
- User experience magic

#### GitHub Agent
- Repository management
- Branch/PR workflows
- Release tagging
- CI/CD pipeline

#### Team Lead
- Task coordination
- PR approval and merging
- Progress tracking
- Blockers resolution

### Communication
- **Daily standup:** Update task board with progress
- **Blockers:** Immediately flag in task board
- **Decisions:** Document in relevant docs/ files
- **Questions:** Ask in team channel or create discussion

### Quality Standards
1. **Code Style:** Follow existing patterns, use Prettier/ESLint
2. **Documentation:** Update relevant docs for significant changes
3. **Testing:** Write tests for new functionality
4. **Performance:** Consider impact on app performance
5. **Security:** Follow security best practices

### Getting Help
1. Check existing documentation
2. Review similar code in codebase
3. Ask relevant specialist
4. Escalate to Team Lead if blocked > 2 hours

---
*Established by GitHub Agent with Team Lead - 2026-02-14*