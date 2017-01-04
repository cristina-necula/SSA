using System;
using System.Collections.Generic;

namespace MyProjectManager.Models
{
	public class Milestone
	{
		public int ID { get; set; }
		public string Description { get; set; }
		public DateTime EstimatedFinishDate { get; set; }
		public DateTime ActualFinishDate { get; set; }

		public List<Sprint> Sprints { get; set; }
	}
}