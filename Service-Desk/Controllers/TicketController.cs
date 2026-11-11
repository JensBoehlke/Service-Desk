
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Service_Desk.Models;

public class TicketController : Controller
{
    private readonly ServiceDeskContext _context;

    public TicketController(ServiceDeskContext context)
    {
        _context = context;
    }

    // GET: TICKETS
    public async Task<IActionResult> Index()    
    {
        return View(await _context.Tickets.ToListAsync());
    }

    // GET: TICKETS/Details/5
    public async Task<IActionResult> Details(int? ticketid)
    {
        if (ticketid == null)
        {
            return NotFound();
        }

        var ticket = await _context.Tickets
            .FirstOrDefaultAsync(m => m.TicketId == ticketid);
        if (ticket == null)
        {
            return NotFound();
        }

        return View(ticket);
    }

    // GET: TICKETS/Create
    public IActionResult Create()
    {
        return View();
    }

    // POST: TICKETS/Create
    // To protect from overposting attacks, enable the specific properties you want to bind to.
    // For more details, see http://go.microsoft.com/fwlink/?LinkId=317598.
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create([Bind("TicketId,ErstelltVon,Titel,Beschreibung,Erstellungsdatum,Kategorie,Prioritaet,Status,MitarbeiterId,Mitarbeiter")] Ticket ticket)
    {
        if (ModelState.IsValid)
        {
            _context.Add(ticket);
            await _context.SaveChangesAsync();
            return RedirectToAction(nameof(Index));
        }
        return View(ticket);
    }

    // GET: TICKETS/Edit/5
    public async Task<IActionResult> Edit(int? ticketid)
    {
        if (ticketid == null)
        {
            return NotFound();
        }

        var ticket = await _context.Tickets.FindAsync(ticketid);
        if (ticket == null)
        {
            return NotFound();
        }
        return View(ticket);
    }

    // POST: TICKETS/Edit/5
    // To protect from overposting attacks, enable the specific properties you want to bind to.
    // For more details, see http://go.microsoft.com/fwlink/?LinkId=317598.
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Edit(int? ticketid, [Bind("TicketId,ErstelltVon,Titel,Beschreibung,Erstellungsdatum,Kategorie,Prioritaet,Status,MitarbeiterId,Mitarbeiter")] Ticket ticket)
    {
        if (ticketid != ticket.TicketId)
        {
            return NotFound();
        }

        if (ModelState.IsValid)
        {
            try
            {
                _context.Update(ticket);
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!TicketExists(ticket.TicketId))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }
            return RedirectToAction(nameof(Index));
        }
        return View(ticket);
    }

    // GET: TICKETS/Delete/5
    public async Task<IActionResult> Delete(int? ticketid)
    {
        if (ticketid == null)
        {
            return NotFound();
        }

        var ticket = await _context.Tickets
            .FirstOrDefaultAsync(m => m.TicketId == ticketid);
        if (ticket == null)
        {
            return NotFound();
        }

        return View(ticket);
    }

    // POST: TICKETS/Delete/5
    [HttpPost, ActionName("Delete")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> DeleteConfirmed(int? ticketid)
    {
        var ticket = await _context.Tickets.FindAsync(ticketid);
        if (ticket != null)
        {
            _context.Tickets.Remove(ticket);
        }

        await _context.SaveChangesAsync();
        return RedirectToAction(nameof(Index));
    }

    private bool TicketExists(int? ticketid)
    {
        return _context.Tickets.Any(e => e.TicketId == ticketid);
    }
}
