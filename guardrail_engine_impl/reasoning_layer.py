# reasoning_layer.py

class ReasoningLayer:
    def generate(self, task: dict) -> str:
        """
        Generates a single neutral sentence restating task metadata.
        This output is advisory only and non-authoritative.
        """
        return (
            f"The task specifies a {task['task_type']} operation "
            f"with the provided parameters."
        )
