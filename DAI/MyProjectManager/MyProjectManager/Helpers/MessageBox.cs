﻿using System;
using System.Web.UI;

namespace MyProjectManager.Helpers
{
	public static class MessageBox
	{
		public static void Show(this Page Page, String Message)
		{
			Page.ClientScript.RegisterStartupScript(
			   Page.GetType(),
			   "MessageBox",
			   "<script language='javascript'>alert('" + Message + "');</script>"
			);
		}
	}
}