# Backend - Secure Note-Taking App

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Set up database:
   ```bash
   # Start PostgreSQL (if using Docker)
   docker-compose up -d
   
   # Run migrations
   npx prisma migrate dev --name init
   
   # Generate Prisma Client
   npx prisma generate
   ```

3. Configure environment:
   ```bash
   cp .env.example .env  # Edit with your values
   ```

4. Start development server:
   ```bash
   npm run dev
   ```

## Database Schema

See `/prisma/schema.prisma` for the complete schema. Key models:

### User
- `id` (cuid)
- `email` (unique)
- `password` (bcrypt hashed)
- `name` (optional)
- `notes` (relation to Note model)

### Note
- `id` (cuid)
- `title` (max 255 chars)
- `content` (text, optional)
- `authorId` (foreign key to User)
- `isPublic` (boolean, default false)
- `tags` (string array)
- `createdAt/updatedAt` (timestamps)

## API Endpoints to Implement

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user (protected)

### Notes (Protected)
- `GET /api/notes` - List user's notes
- `GET /api/notes/:id` - Get specific note
- `POST /api/notes` - Create new note
- `PUT /api/notes/:id` - Update note
- `DELETE /api/notes/:id` - Delete note
- `GET /api/notes/public` - List public notes (optional)

## Development Notes

### Prisma Client
Import and use Prisma Client:
```typescript
import { PrismaClient } from '@prisma/client'
const prisma = new PrismaClient()
```

### JWT Authentication
- Use `jsonwebtoken` package
- Secret stored in `JWT_SECRET` env variable
- Implement middleware for protected routes

### Password Hashing
- Use `bcrypt` package
- Hash passwords before storing in database
- Compare hashes during login

### Error Handling
- Use appropriate HTTP status codes
- Return consistent error response format
- Log errors for debugging

## Testing

Run tests:
```bash
npm test
```

## Deployment

Build for production:
```bash
npm run build
```

Start production server:
```bash
npm start
```