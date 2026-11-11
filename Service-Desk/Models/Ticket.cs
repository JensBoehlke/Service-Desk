using System.ComponentModel.DataAnnotations;

namespace Service_Desk.Models
{
    public class Ticket
    {
        [Key]
        public int TicketId { get; set; }

        [Required(ErrorMessage = "Bitte Ihre Name angeben.")]
        [Display(Name = "Erstellt Von:")]
        [StringLength(50)]
        public string ErstelltVon { get; set; } = string.Empty;

        [Required(ErrorMessage = "Bitte einen Titel angeben.")]
        [StringLength(100)]
        public string Titel { get; set; } = string.Empty;

        [Required(ErrorMessage = "Bitte eine Beschreibung angeben.")]
        [StringLength(2000)]
        public string Beschreibung { get; set; } = string.Empty;

        [Display(Name = "Erstellungsdatum")]
        [DataType(DataType.DateTime)]
        public DateTime Erstellungsdatum { get; set; } = DateTime.Now;

        public Kategorie Kategorie { get; set; } = Kategorie.Hardware;

        public Prioritaet Prioritaet { get; set; } = Prioritaet.Mittel;

        public TicketStatus Status { get; set; } = TicketStatus.Offen;

        [Display(Name = "Bearbeiter")]
        public int? MitarbeiterId { get; set; }
        public IT_Mitarbeiter? Mitarbeiter { get; set; }
    }
}
