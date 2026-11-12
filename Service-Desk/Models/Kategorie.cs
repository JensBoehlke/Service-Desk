using System.ComponentModel.DataAnnotations;
using System.Net.Sockets;

namespace Service_Desk.Models
{
    public class Kategorie
    {
        [Key]
        public int KategorieId { get; set; }

        [Required(ErrorMessage = "Bitte eine Kategorie angeben.")]
        [StringLength(50)]
        public string KategorieName { get; set; } = string.Empty;

        public ICollection<Ticket> Tickets { get; set; } = new List<Ticket>();

    }
}