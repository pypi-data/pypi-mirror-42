import luigi

tasks = {}

def register_task_facade(ruby_obj, task_name):
	attributes = {}
	ruby_class = getattr(ruby_obj, "class")()

	def def_delegate_method(mthd):
		if hasattr(ruby_obj, mthd):
			delegate = getattr(ruby_obj, mthd)
			def handler(self):
				ruby_obj.instance_variable_set("@python_obj", self)
				return delegate()
			return handler

	def register_delegate_method(mthd):
		register_method(mthd, def_delegate_method(mthd))

	def register_method(mthd, handler):
		if handler is not None:
			attributes[mthd] = handler

	def define_output_method():
		defined_outputs = ruby_class.defined_outputs()
		if len(defined_outputs) > 0:
			def handler(self):
				ruby_obj.instance_variable_set("@python_obj", self)
				if len(defined_outputs) == 1:
					return defined_outputs[0]
				else:
					return defined_outputs
			return handler

	def define_requires_method():
		defined_requirements = ruby_class.defined_requirements()
		if len(defined_requirements) > 0:
			def handler(self):
				ruby_obj.instance_variable_set("@python_obj", self)
				if len(defined_requirements) == 1:
					return defined_requirements[0]
				else:
					return defined_requirements
			return handler

	def define_parameters():
		defined_parameters = ruby_class.defined_parameters()
		for name, param in defined_parameters:
			attributes[name] = param

	register_delegate_method("run")
	register_delegate_method("complete")
	register_method("output", define_output_method())
	register_method("requires", define_requires_method())
	define_parameters()

	t = type(task_name, (luigi.Task,), attributes)
	tasks[task_name] = t
