class RenderTask():
    def __init__(
        self, blend_file: str, render_engine: str, render_device: str,
        render_samples: int, output_type: str, start_frame: int, end_frame: int,
        output_format: str, output_file: str, python_expressions: str,
        after_rendering: str
    ) -> None:
        self.blend_file = blend_file
        self.render_engine = render_engine
        self.render_device = render_device
        self.render_samples = render_samples
        self.output_type = output_type
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.output_format = output_format
        self.output_file = output_file
        self.python_expressions = python_expressions
        self.after_rendering = after_rendering
