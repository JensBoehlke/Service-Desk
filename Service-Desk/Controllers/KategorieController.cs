
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Service_Desk.Models;

public class KategorieController : Controller
{
    private readonly ServiceDeskContext _context;

    public KategorieController(ServiceDeskContext context)
    {
        _context = context;
    }

    // GET: KATEGORIES
    public async Task<IActionResult> Index()    
    {
        return RedirectToAction("Index", "IT_Mitarbeiter");
    }


    // GET: KATEGORIES/Details/5
    public async Task<IActionResult> Details(int? kategorieid)
    {
        if (kategorieid == null)
        {
            return NotFound();
        }

        var kategorie = await _context.Kategorie
            .FirstOrDefaultAsync(m => m.KategorieId == kategorieid);
        if (kategorie == null)
        {
            return NotFound();
        }

        return View(kategorie);
    }

    // GET: KATEGORIES/Create
    public IActionResult Create()
    {
        return View();
    }

    // POST: KATEGORIES/Create
    // To protect from overposting attacks, enable the specific properties you want to bind to.
    // For more details, see http://go.microsoft.com/fwlink/?LinkId=317598.
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create([Bind("KategorieId,KategorieName,Tickets")] Kategorie kategorie)
    {
        if (ModelState.IsValid)
        {
            _context.Add(kategorie);
            await _context.SaveChangesAsync();
            return RedirectToAction(nameof(Index));
        }
        return View(kategorie);
    }

    // GET: KATEGORIES/Edit/5
    public async Task<IActionResult> Edit(int? kategorieid)
    {
        if (kategorieid == null)
        {
            return NotFound();
        }

        var kategorie = await _context.Kategorie.FindAsync(kategorieid);
        if (kategorie == null)
        {
            return NotFound();
        }
        return View(kategorie);
    }

    // POST: KATEGORIES/Edit/5
    // To protect from overposting attacks, enable the specific properties you want to bind to.
    // For more details, see http://go.microsoft.com/fwlink/?LinkId=317598.
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Edit(int? kategorieid, [Bind("KategorieId,KategorieName,Tickets")] Kategorie kategorie)
    {
        if (kategorieid != kategorie.KategorieId)
        {
            return NotFound();
        }

        if (ModelState.IsValid)
        {
            try
            {
                _context.Update(kategorie);
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!KategorieExists(kategorie.KategorieId))
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
        return View(kategorie);
    }

    // GET: KATEGORIES/Delete/5
    public async Task<IActionResult> Delete(int? kategorieid)
    {
        if (kategorieid == null)
        {
            return NotFound();
        }

        var kategorie = await _context.Kategorie
            .FirstOrDefaultAsync(m => m.KategorieId == kategorieid);
        if (kategorie == null)
        {
            return NotFound();
        }

        return View(kategorie);
    }

    // POST: KATEGORIES/Delete/5
    [HttpPost, ActionName("Delete")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> DeleteConfirmed(int? kategorieid)
    {
        if (kategorieid == null)
        {
            return NotFound();
        }

        var kategorie = await _context.Kategorie.FindAsync(kategorieid);
        if (kategorie != null)
        {
            var tickets = await _context.Tickets
                .Where(t => t.KategorieId == kategorieid)
                .ToListAsync();

            foreach (var ticket in tickets)
            {
                ticket.KategorieId = null;
            }

            _context.Kategorie.Remove(kategorie);
        }

        await _context.SaveChangesAsync();
        return RedirectToAction(nameof(Index));
    }

    private bool KategorieExists(int? kategorieid)
    {
        return _context.Kategorie.Any(e => e.KategorieId == kategorieid);
    }
}
