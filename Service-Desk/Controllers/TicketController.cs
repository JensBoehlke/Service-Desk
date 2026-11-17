
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Service_Desk.Models;
using Microsoft.AspNetCore.Mvc.Rendering;

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
    //public async Task<IActionResult> Details(int? ticketid)
    //{
    //    if (ticketid == null)
    //    {
    //        return NotFound();
    //    }

    //    var ticket = await _context.Tickets
    //        .FirstOrDefaultAsync(m => m.TicketId == ticketid);
    //    if (ticket == null)
    //    {
    //        return NotFound();
    //    }

    //    return View(ticket);
    //}

    public async Task<IActionResult> Details(int? id)
    {
        if (id == null)
        {
            return NotFound();
        }

        var ticket = await _context.Tickets
            .Include(item => item.Mitarbeiter)
            .Include(item => item.Kategorie)
            .FirstOrDefaultAsync(item => item.TicketId == id);

        if (ticket == null)
        {
            return NotFound();
        }

        return View(ticket);
    }

    // GET: TICKETS/Create
    public async Task<IActionResult> Create() // asyc fürs await
    {
        var kategorien = await _context.Kategorie
        .OrderBy(kategorie => kategorie.KategorieName)
        .ToListAsync();

        ViewBag.KategorieId = new SelectList(
            kategorien,
            nameof(Kategorie.KategorieId),
            nameof(Kategorie.KategorieName));
        return View();
    }

    // POST: TICKETS/Create
    // To protect from overposting attacks, enable the specific properties you want to bind to.
    // For more details, see http://go.microsoft.com/fwlink/?LinkId=317598.
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create([Bind("TicketId,ErstelltVon,Titel,Beschreibung,Erstellungsdatum,KategorieId,Prioritaet,MitarbeiterId")] Ticket ticket)
    {
      // beim neuladen wenn Fehler
        // hier wird einfach immer die letzte kategorie angezeigt
        //sorgt dafür, dass die zuvor ausgewählte Kategorie markiert bleibt.
        var kategorien = await _context.Kategorie
    .OrderBy(kategorie => kategorie.KategorieName)
    .ToListAsync();

        ViewBag.KategorieId = new SelectList(
            kategorien,
            nameof(Kategorie.KategorieId),
            nameof(Kategorie.KategorieName),
            ticket.KategorieId);
        if (ModelState.IsValid)
        {
            ticket.Status = TicketStatus.Offen; // Ticketstatus beim erstellen auf Offen setzen

            _context.Add(ticket);
            await _context.SaveChangesAsync();
            return RedirectToAction("Index", "Home");
        }
        return View(ticket);
    }

}
