using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.EntityFrameworkCore;
using Service_Desk.Models;

namespace Service_Desk.Controllers
{
    public class SupportController : Controller
    {
        private readonly ServiceDeskContext _context;

        public SupportController(ServiceDeskContext context)
        {
            _context = context;
        }

        public async Task<IActionResult> Index(
            TicketStatus? status,
            Prioritaet? prioritaet,
            int? kategorie)
        {
            var tickets = _context.Tickets
                .Include(ticket => ticket.Mitarbeiter)
                .Include(ticket => ticket.Kategorie)
                .AsQueryable();

            if (status.HasValue)
            {
                tickets = tickets.Where(ticket => ticket.Status == status.Value);
            }

            if (prioritaet.HasValue)
            {
                tickets = tickets.Where(ticket => ticket.Prioritaet == prioritaet.Value);
            }

            if (kategorie.HasValue)
            {
                tickets = tickets.Where(ticket => ticket.KategorieId == kategorie.Value);
            }

            await PopulateKategorieDropDownListAsync(kategorie);

            return View(await tickets
                .OrderByDescending(ticket => ticket.Erstellungsdatum)
                .ToListAsync());
        }

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

        public async Task<IActionResult> Create()
        {
            await PopulateMitarbeiterDropDownListAsync();
            await PopulateKategorieDropDownListAsync();
            return View();
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create(
            [Bind("ErstelltVon,Titel,Beschreibung,KategorieId,Prioritaet,Status,MitarbeiterId")]
            Ticket ticket)
        {
            if (ModelState.IsValid)
            {
                ticket.Erstellungsdatum = DateTime.Now;
                _context.Add(ticket);
                await _context.SaveChangesAsync();
                return RedirectToAction(nameof(Index));
            }

            await PopulateMitarbeiterDropDownListAsync(ticket.MitarbeiterId);
            await PopulateKategorieDropDownListAsync(ticket.KategorieId);
            return View(ticket);
        }

        public async Task<IActionResult> Edit(int? id)
        {
            if (id == null)
            {
                return NotFound();
            }

            var ticket = await _context.Tickets.FindAsync(id);
            if (ticket == null)
            {
                return NotFound();
            }
            if (ticket.Status == TicketStatus.Abgeschlossen)
            {
                return RedirectToAction(nameof(Details), new { id = ticket.TicketId });
            }

            await PopulateMitarbeiterDropDownListAsync(ticket.MitarbeiterId);
            await PopulateKategorieDropDownListAsync(ticket.KategorieId);
            return View(ticket);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(int id)
        {
            var ticket = await _context.Tickets.FindAsync(id);
            if (ticket == null)
            {
                return NotFound();
            }
            if (ticket.Status == TicketStatus.Abgeschlossen)
            {
                return RedirectToAction(nameof(Details), new { id = ticket.TicketId });
            }

            if (await TryUpdateModelAsync(
                    ticket,
                    string.Empty,
                    item => item.ErstelltVon,
                    item => item.Titel,
                    item => item.Beschreibung,
                    item => item.KategorieId,
                    item => item.Prioritaet,
                    item => item.Status,
                    item => item.MitarbeiterId))
            {
                try
                {
                    await _context.SaveChangesAsync();
                    return RedirectToAction(nameof(Index));
                }
                catch (DbUpdateConcurrencyException)
                {
                    if (!TicketExists(ticket.TicketId))
                    {
                        return NotFound();
                    }

                    throw;
                }
            }

            await PopulateMitarbeiterDropDownListAsync(ticket.MitarbeiterId);
            await PopulateKategorieDropDownListAsync(ticket.KategorieId);
            return View(ticket);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Reopen(int id)
        {
            var ticket = await _context.Tickets.FindAsync(id);
            if (ticket == null)
            {
                return NotFound();
            }

            ticket.Status = TicketStatus.Offen;
            await _context.SaveChangesAsync();
            return RedirectToAction(nameof(Index));
        }

        public async Task<IActionResult> Delete(int? id)
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

        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DeleteConfirmed(int id)
        {
            var ticket = await _context.Tickets.FindAsync(id);
            if (ticket != null)
            {
                _context.Tickets.Remove(ticket);
                await _context.SaveChangesAsync();
            }

            return RedirectToAction(nameof(Index));
        }

        private async Task PopulateMitarbeiterDropDownListAsync(int? selectedMitarbeiterId = null)
        {
            var mitarbeiter = await _context.Mitarbeiter
                .OrderBy(person => person.Name)
                .ToListAsync();

            ViewBag.MitarbeiterId = new SelectList(
                mitarbeiter,
                nameof(IT_Mitarbeiter.MitarbeiterId),
                nameof(IT_Mitarbeiter.Name),
                selectedMitarbeiterId);
        }

        private async Task PopulateKategorieDropDownListAsync(int? selectedKategorieId = null)
        {
            var kategorien = await _context.Kategorie
                .OrderBy(kategorie => kategorie.KategorieName)
                .ToListAsync();

            ViewBag.KategorieId = new SelectList(
                kategorien,
                nameof(Kategorie.KategorieId),
                nameof(Kategorie.KategorieName),
                selectedKategorieId);
        }

        private bool TicketExists(int id)
        {
            return _context.Tickets.Any(ticket => ticket.TicketId == id);
        }
    }
}


