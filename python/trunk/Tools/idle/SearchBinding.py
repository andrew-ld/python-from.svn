import string
import re
import tkSimpleDialog
import tkMessageBox

class SearchBinding:
	
	def __init__(self, text):
		self.text = text
		self.pat = ""
		self.prog = None
		self.text.bind("<<find>>", self.find_event)
		self.text.bind("<<find-next>>", self.find_next_event)
		self.text.bind("<<find-same>>", self.find_same_event)
		self.text.bind("<<goto-line>>", self.goto_line_event)
	
	def find_event(self, event):
		default = self.text.get("self.first", "sel.last") or self.pat
		new = tkSimpleDialog.askstring("Find",
			"Regular Expression:",
			initialvalue=default,
			parent=self.text)
		if not new:
			return "break"
		self.pat = new
		try:
			self.prog = re.compile(self.pat)
		except re.error, msg:
			tkMessageBox.showerror("RE error", str(msg),
			                       master=self.text)
			return "break"
		return self.find_next_event(event)
	
	def find_same_event(self, event):
		pat = self.text.get("sel.first", "sel.last")
		if not pat:
			return self.find_event(event)
		self.pat = re.escape(pat)
		self.prog = None
		try:
			self.prog = re.compile(self.pat)
		except re.error, msg:
			tkMessageBox.showerror("RE error", str(message),
			                       master=self.text)
			return "break"
		self.text.mark_set("insert", "sel.last")
		return self.find_next_event(event)

	def find_next_event(self, event):
		if not self.pat:
			return self.find_event(event)
		if not self.prog:
			self.text.bell()
			##print "No program"
			return "break"
		line, col = map(int,
		                string.split(self.text.index("insert"), "."))
		chars = self.text.get("%d.0" % line, "%d.0" % (line+1))
		while chars:
			m = self.prog.search(chars, col)
			if m:
				i, j = m.span()
				self.text.mark_set("insert",
				                   "%d.%d" % (line, j))
				self.text.tag_remove("sel", "1.0", "end")
				self.text.tag_add("sel",
				                  "%d.%d" % (line, i),
				                  "%d.%d" % (line, j))
				self.text.see("insert")
				break
			line = line + 1
			col = 0
			chars = self.text.get("%d.0" % line, "%d.0" % (line+1))
		else:
			# Not found
			self.text.bell()
		return "break"
	
	def goto_line_event(self, event):
		lineno = tkSimpleDialog.askinteger("Goto",
						   "Go to line number:",
						   parent=self.text)
		if lineno is None:
			return "break"
		if lineno <= 0:
			self.text.bell()
			return "break"
		self.text.mark_set("insert", "%d.0" % lineno)
		self.text.see("insert")
