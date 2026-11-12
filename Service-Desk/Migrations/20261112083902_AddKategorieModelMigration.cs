using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Service_Desk.Migrations
{
    /// <inheritdoc />
    public partial class AddKategorieModelMigration : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Kategorie",
                table: "Tickets");

            migrationBuilder.AddColumn<int>(
                name: "KategorieId",
                table: "Tickets",
                type: "int",
                nullable: true);

            migrationBuilder.CreateTable(
                name: "Kategorie",
                columns: table => new
                {
                    KategorieId = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    KategorieName = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Kategorie", x => x.KategorieId);
                });

            migrationBuilder.CreateIndex(
                name: "IX_Tickets_KategorieId",
                table: "Tickets",
                column: "KategorieId");

            migrationBuilder.AddForeignKey(
                name: "FK_Tickets_Kategorie_KategorieId",
                table: "Tickets",
                column: "KategorieId",
                principalTable: "Kategorie",
                principalColumn: "KategorieId");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Tickets_Kategorie_KategorieId",
                table: "Tickets");

            migrationBuilder.DropTable(
                name: "Kategorie");

            migrationBuilder.DropIndex(
                name: "IX_Tickets_KategorieId",
                table: "Tickets");

            migrationBuilder.DropColumn(
                name: "KategorieId",
                table: "Tickets");

            migrationBuilder.AddColumn<int>(
                name: "Kategorie",
                table: "Tickets",
                type: "int",
                nullable: false,
                defaultValue: 0);
        }
    }
}
