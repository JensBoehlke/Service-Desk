Initial analysis of DbUpdateException from IT_MitarbeiterController.DeleteConfirmed
- Exception: DELETE conflicted with REFERENCE constraint FK_Tickets_Mitarbeiter_MitarbeiterId
- Controller: DeleteConfirmed calls _context.Mitarbeiter.Remove() and _context.SaveChangesAsync()
- Need to find tickets associated with this mitarbeiterid and handle deletion or cascade
- Ask: Should we delete tickets too or change foreign key constraint?