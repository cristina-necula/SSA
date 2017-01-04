using MyProjectManager.Models;
using System.Data.Entity;
using System.Data.Entity.ModelConfiguration.Conventions;

namespace MyProjectManager.DAL
{
	public class ProjectManagerContext : DbContext
	{
		public ProjectManagerContext() : base("ProjectManagerContext")
		{
		}

		public DbSet<User> Users { get; set; }
		public DbSet<Milestone> Milestones { get; set; }
		public DbSet<Project> Projects { get; set; }
		public DbSet<Sprint> Sprints { get; set; }
		public DbSet<Task> Tasks { get; set; }
		public DbSet<TaskComponent> TaskComponents { get; set; }

		protected override void OnModelCreating(DbModelBuilder modelBuilder)
		{
			modelBuilder.Conventions.Remove<PluralizingTableNameConvention>();
			base.OnModelCreating(modelBuilder);
		}
	}
}