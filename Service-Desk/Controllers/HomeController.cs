using Microsoft.AspNetCore.Mvc;
using Service_Desk.Models;
using System.Diagnostics;

namespace Service_Desk.Controllers
{
    public class HomeController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }

        public IActionResult Privacy()
        {
            return View();

        }

        // Alte Links auf Home/Ticket führen ebenfalls zur Ticketübersicht.
        public IActionResult Ticket()
        {
            return RedirectToAction("Index", "Ticket");
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
