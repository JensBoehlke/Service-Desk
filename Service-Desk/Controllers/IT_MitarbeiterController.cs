
using Azure.Core;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Service_Desk.Models;

public class IT_MitarbeiterController : Controller
{
    private readonly ServiceDeskContext _context;

    public IT_MitarbeiterController(ServiceDeskContext context)
    {
        _context = context;
    }

    // GET: IT_MITARBEITERS
    public async Task<IActionResult> Index()    
    {
        ViewBag.Kategorien = await _context.Kategorie.ToListAsync();
        return View(await _context.Mitarbeiter.ToListAsync());
    }

    // GET: IT_MITARBEITERS/Details/5
    public async Task<IActionResult> Details(int? mitarbeiterid)
    {
        if (mitarbeiterid == null)
        {
            return NotFound();
        }

        var it_mitarbeiter = await _context.Mitarbeiter
            .FirstOrDefaultAsync(m => m.MitarbeiterId == mitarbeiterid);
        if (it_mitarbeiter == null)
        {
            return NotFound();
        }

        return View(it_mitarbeiter);
    }

    // GET: IT_MITARBEITERS/Create
    public IActionResult Create()
    {
        return View();
    }

    // POST: IT_MITARBEITERS/Create
    // To protect from overposting attacks, enable the specific properties you want to bind to.
    // For more details, see http://go.microsoft.com/fwlink/?LinkId=317598.
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create([Bind("MitarbeiterId,Name,Tickets")] IT_Mitarbeiter it_mitarbeiter)
    {
        if (ModelState.IsValid)
        {
            _context.Add(it_mitarbeiter);
            await _context.SaveChangesAsync();
            return RedirectToAction(nameof(Index));
        }
        return View(it_mitarbeiter);
    }

    // GET: IT_MITARBEITERS/Edit/5
    public async Task<IActionResult> Edit(int? mitarbeiterid)
    {
        if (mitarbeiterid == null)
        {
            return NotFound();
        }

        var it_mitarbeiter = await _context.Mitarbeiter.FindAsync(mitarbeiterid);
        if (it_mitarbeiter == null)
        {
            return NotFound();
        }
        return View(it_mitarbeiter);
    }

    // POST: IT_MITARBEITERS/Edit/5
    // To protect from overposting attacks, enable the specific properties you want to bind to.
    // For more details, see http://go.microsoft.com/fwlink/?LinkId=317598.
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Edit(int? mitarbeiterid, [Bind("MitarbeiterId,Name,Tickets")] IT_Mitarbeiter it_mitarbeiter)
    {
        if (mitarbeiterid != it_mitarbeiter.MitarbeiterId)
        {
            return NotFound();
        }

        if (ModelState.IsValid)
        {
            try
            {
                _context.Update(it_mitarbeiter);
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!IT_MitarbeiterExists(it_mitarbeiter.MitarbeiterId))
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
        return View(it_mitarbeiter);
    }

    // GET: IT_MITARBEITERS/Delete/5
    public async Task<IActionResult> Delete(int? mitarbeiterid)
    {
        if (mitarbeiterid == null)
        {
            return NotFound();
        }

        var it_mitarbeiter = await _context.Mitarbeiter
            .FirstOrDefaultAsync(m => m.MitarbeiterId == mitarbeiterid);
        if (it_mitarbeiter == null)
        {
            return NotFound();
        }

        return View(it_mitarbeiter);
    }

    // POST: IT_MITARBEITERS/Delete/5
    [HttpPost, ActionName("Delete")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> DeleteConfirmed(int? mitarbeiterid)
    {
        var it_mitarbeiter = await _context.Mitarbeiter.FindAsync(mitarbeiterid);
        if (it_mitarbeiter != null)
        {
            _context.Mitarbeiter.Remove(it_mitarbeiter);
        }

        await _context.SaveChangesAsync();
        return RedirectToAction(nameof(Index));
    }

    private bool IT_MitarbeiterExists(int? mitarbeiterid)
    {
        return _context.Mitarbeiter.Any(e => e.MitarbeiterId == mitarbeiterid);
    }
}
