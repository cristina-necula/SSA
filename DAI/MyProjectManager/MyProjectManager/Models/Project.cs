using System.Collections.Generic;

namespace MyProjectManager.Models
{
	public class Project
	{
		public int ID { get; set; }
		public string Name { get; set; }
		public User ProjectManager { get; set; }
		public List<User> TeamMembers { get; set; }
		public List<Milestone> Milestones { get; set; }
		public List<Sprint> Sprints { get; set; }
	}
}