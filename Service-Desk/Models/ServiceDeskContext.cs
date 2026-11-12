using Microsoft.EntityFrameworkCore;
using Service_Desk.Models;

namespace Service_Desk.Models
{
    public class ServiceDeskContext : DbContext
    {
        public DbSet<Service_Desk.Models.Kategorie> Kategorie { get; set; } = default!;
        public ServiceDeskContext(DbContextOptions<ServiceDeskContext> options)
            : base(options) { }

        public DbSet<Ticket> Tickets { get; set; }

        public DbSet<IT_Mitarbeiter> Mitarbeiter { get; set; }

    }
}