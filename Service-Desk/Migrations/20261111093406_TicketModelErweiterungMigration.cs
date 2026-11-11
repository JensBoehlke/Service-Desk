using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Service_Desk.Migrations
{
    /// <inheritdoc />
    public partial class TicketModelErweiterungMigration : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "ErstelltVon",
                table: "Tickets",
                type: "nvarchar(50)",
                maxLength: 50,
                nullable: false,
                defaultValue: "");

            migrationBuilder.AddColumn<DateTime>(
                name: "Erstellungsdatum",
                table: "Tickets",
                type: "datetime2",
                nullable: false,
                defaultValue: new DateTime(1, 1, 1, 0, 0, 0, 0, DateTimeKind.Unspecified));
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "ErstelltVon",
                table: "Tickets");

            migrationBuilder.DropColumn(
                name: "Erstellungsdatum",
                table: "Tickets");
        }
    }
}
