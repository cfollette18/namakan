# Database Design Document

## Overview
PostgreSQL database design for the Secure Note-Taking App. Uses Prisma ORM for schema management and migrations.

## Schema Design

### User Model (`users` table)
- **id**: Primary key using cuid() for globally unique identifiers
- **email**: Unique, required field for authentication
- **password**: Hashed password (bcrypt)
- **name**: Optional display name
- **createdAt/updatedAt**: Automatic timestamp tracking
- **Indexes**: Email field indexed for fast lookups

### Note Model (`notes` table)  
- **id**: Primary key using cuid()
- **title**: Required, max 255 characters
- **content**: Optional text field for note body
- **authorId**: Foreign key to User with cascade delete
- **isPublic**: Boolean flag for note visibility (default: private)
- **tags**: String array for categorization
- **createdAt/updatedAt**: Automatic timestamp tracking
- **Indexes**: 
  - authorId for user-specific queries
  - createdAt for chronological sorting
  - isPublic for public note queries

## Design Decisions

### 1. **Identifier Strategy**
- Using `cuid()` instead of auto-increment integers for:
  - Global uniqueness
  - No sequential predictability (security)
  - Easier migration if sharding needed

### 2. **Password Storage**
- Passwords stored as bcrypt hashes
- Prisma doesn't handle hashing - application layer responsibility

### 3. **Note Visibility**
- `isPublic` flag allows for future sharing features
- Defaults to private (false) for security

### 4. **Tag System**
- Using PostgreSQL native array type for tags
- Simple implementation, can be normalized later if needed
- Enables efficient tag-based queries

### 5. **Cascade Deletes**
- Notes automatically deleted when user is deleted
- Prevents orphaned records

### 6. **Index Strategy**
- Email indexed for login performance
- AuthorId indexed for user-specific note queries
- CreatedAt indexed for chronological displays
- isPublic indexed for public note queries

## Migration Notes

### Initial Migration
Run: `npx prisma migrate dev --name init`

### Environment Variables
```env
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/notesdb"
```

## Performance Considerations

1. **Text Content**: Using `@db.Text` for note content to handle large notes
2. **Array Fields**: PostgreSQL arrays efficient for simple tag systems
3. **Index Coverage**: All common query paths indexed
4. **Cascade Deletes**: Maintains referential integrity

## Future Extensions

1. **Note Sharing**: Add `sharedWith` relation for user-to-user sharing
2. **Note Versions**: Add version history table
3. **Full-text Search**: Add PostgreSQL full-text search indexes
4. **Tag Normalization**: Convert tags to separate table if needed
5. **Soft Deletes**: Add `deletedAt` timestamp for recovery

## Security Considerations

1. **No Plain Text Passwords**: Application must hash before storage
2. **Private by Default**: Notes default to private
3. **CUIDs**: Non-sequential IDs prevent enumeration attacks
4. **Cascade Protection**: Prevents orphaned data exposure

---
*Database Specialist - 2026-02-14 14:40 CST*