using MyProjectManager.Enums;
using System.Collections.Generic;

namespace MyProjectManager.Models
{
	public class Task
	{
		public int ID { get; set; }
		public Status Status { get; set; }
		public User Resposible { get; set; }
		public string Summary { get; set; }
		public int EstimatedEffort { get; set; }
		public int ConsumedEffort { get; set; }
		public List<TaskComponent> TaskComponents { get; set; }
	}
}