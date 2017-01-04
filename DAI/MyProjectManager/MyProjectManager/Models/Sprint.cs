using System;
using System.Collections.Generic;

namespace MyProjectManager.Models
{
	public class Sprint
	{
		public int ID { get; set; }
		public DateTime StartDate { get; set; }
		public DateTime EndDate { get; set; }
		public List<Task> Tasks { get; set; }
	}
}