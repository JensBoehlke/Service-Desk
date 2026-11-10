using System.ComponentModel.DataAnnotations;
using System.Net.Sockets;

namespace Service_Desk.Models
{
    public class IT_Mitarbeiter
    {
        [Key]
        public int MitarbeiterId { get; set; }

        [Required(ErrorMessage = "Bitte einen Vornamen angeben.")]
        [StringLength(50)]
        public string Name { get; set; } = string.Empty;

        public ICollection<Ticket> Tickets { get; set; } = new List<Ticket>();

    }
}
