import express from 'express';
import { authenticateToken } from '../middleware/auth';
import {
  getNotes,
  getNote,
  createNote,
  updateNote,
  deleteNote,
  getPublicNotes
} from '../controllers/noteController';

const router = express.Router();

// All note routes require authentication
router.use(authenticateToken);

// User's notes
router.get('/', getNotes);
router.get('/:id', getNote);
router.post('/', createNote);
router.put('/:id', updateNote);
router.delete('/:id', deleteNote);

// Public notes (optional feature)
router.get('/public', getPublicNotes);

export default router;