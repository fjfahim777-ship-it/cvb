import json
import sys
import os


sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "tools"
    )
)


from code_generator import CodeGenerator
from coding_context import CodingContextBuilder
from fahim_knowledge import FahimKnowledge
from knowledge_manager import KnowledgeManager
from workspace_manager import WorkspaceManager
from project_manager import ProjectManager
from file_reader import read_file
from code_search import search_code
from file_manager import create_file, edit_file
from terminal_manager import run_command
from project_inspector import inspect_project
from task_manager import TaskManager
from requirement_manager import RequirementManager
from task_planner import TaskPlanner
from reasoning_engine import ReasoningEngine


# -----------------------------------
# Setup
# -----------------------------------

workspace_manager = WorkspaceManager()

workspace_path = workspace_manager.workspace_path

project_manager = ProjectManager(
    workspace_path
)

knowledge_manager = KnowledgeManager()

fahim_knowledge = FahimKnowledge(
    os.path.join(
        os.path.dirname(__file__),
        "knowledge"
    )
)


print("Fahim Coding Agent")
print("==================")
print(
    "Type 'help' to see available commands."
)


# -----------------------------------
# Helper
# -----------------------------------

def get_project_path(project_name):

    return os.path.join(
        workspace_path,
        project_name
    )


# -----------------------------------
# Main command loop
# -----------------------------------

while True:

    command = input("\n> ").strip()

    if not command:
        continue


    # -----------------------------------
    # Help
    # -----------------------------------

    if command == "help":

        print("""
Available commands:

help

status

projects

inspect <project>

create tasks <project>

tasks <project>

next <project>

start <project> <task-id>

complete <project> <task-id>

build <project>

read <project>/<file-path>

search <project> <text>

create project <name>

create file <project>/<file-path>

edit <project>/<file-path>

run <project> <command>

exit
""")

        continue


    # -----------------------------------
    # Status
    # -----------------------------------

    if command == "status":

        print("\nAgent Status")
        print("============")

        print(
            f"Workspace: {workspace_path}"
        )

        if workspace_manager.exists():

            print(
                "Workspace status: Available"
            )

        else:

            print(
                "Workspace status: Not found"
            )

        print(
            f"Projects: "
            f"{len(project_manager.list_projects())}"
        )

        continue


    # -----------------------------------
    # Projects
    # -----------------------------------

    if command == "projects":

        projects = project_manager.list_projects()

        print("\nProjects")
        print("========")

        if not projects:

            print(
                "No projects found."
            )

        else:

            for project in projects:

                print(
                    f"- {project}"
                )

        continue


    # -----------------------------------
    # Inspect project
    # -----------------------------------

    if command.startswith("inspect "):

        project_name = command[
            len("inspect "):
        ].strip()

        project_path = get_project_path(
            project_name
        )

        result = inspect_project(
            project_path
        )

        print("\nProject Inspection")
        print("===================")

        print(
            json.dumps(
                result,
                indent=2
            )
        )

        continue


    # -----------------------------------
    # Create tasks
    # -----------------------------------

    if command.startswith("create tasks "):

        project_name = command[
            len("create tasks "):
        ].strip()

        project_path = get_project_path(
            project_name
        )

        if not os.path.isdir(project_path):

            print(
                "Project not found."
            )

            continue

        print(
            "\nEnter project requirement."
        )

        print(
            "Type END on a new line when finished."
        )

        lines = []

        while True:

            line = input()

            if line == "END":
                break

            lines.append(line)

        requirement = "\n".join(
            lines
        )

        requirement_manager = (
            RequirementManager()
        )

        tasks = requirement_manager.create_tasks(
            requirement
        )

        task_manager = TaskManager(
            project_path
        )

        task_manager.create_tasks(
            tasks
        )

        print(
            "\nTasks created:"
        )

        for index, task in enumerate(
            tasks,
            start=1
        ):

            print(
                f"{index}. {task}"
            )

        continue


    # -----------------------------------
    # Tasks
    # -----------------------------------

    if command.startswith("tasks "):

        project_name = command[
            len("tasks "):
        ].strip()

        project_path = get_project_path(
            project_name
        )

        manager = TaskManager(
            project_path
        )

        manager.print_tasks()

        continue


    # -----------------------------------
    # Next task
    # -----------------------------------

    if command.startswith("next "):

        project_name = command[
            len("next "):
        ].strip()

        project_path = get_project_path(
            project_name
        )

        manager = TaskManager(
            project_path
        )

        next_task = manager.get_next_task()

        print("\nNext Task")
        print("=========")

        if next_task:

            print(
                f"{next_task['id']}. "
                f"{next_task['title']}"
            )

        else:

            print(
                "No pending tasks."
            )

        continue


    # -----------------------------------
    # Start task
    # -----------------------------------

    if command.startswith("start "):

        parts = command.split()

        if len(parts) != 3:

            print(
                "Use: start <project> <task-id>"
            )

            continue

        project_name = parts[1]

        try:

            task_id = int(
                parts[2]
            )

        except ValueError:

            print(
                "Task ID must be a number."
            )

            continue

        project_path = get_project_path(
            project_name
        )

        manager = TaskManager(
            project_path
        )

        manager.update_task_status(
            task_id,
            "in_progress"
        )

        print(
            f"Task {task_id} "
            f"marked as in_progress."
        )

        continue


    # -----------------------------------
    # Complete task
    # -----------------------------------

    if command.startswith("complete "):

        parts = command.split()

        if len(parts) != 3:

            print(
                "Use: complete <project> <task-id>"
            )

            continue

        project_name = parts[1]

        try:

            task_id = int(
                parts[2]
            )

        except ValueError:

            print(
                "Task ID must be a number."
            )

            continue

        project_path = get_project_path(
            project_name
        )

        manager = TaskManager(
            project_path
        )

        manager.update_task_status(
            task_id,
            "completed"
        )

        print(
            f"Task {task_id} "
            f"marked as completed."
        )

        continue


    # -----------------------------------
    # Build
    # -----------------------------------

    if command.startswith("build "):

        project_name = command[
            len("build "):
        ].strip()

        project_path = get_project_path(
            project_name
        )

        if not os.path.isdir(project_path):

            print(
                "Project not found."
            )

            continue


        task_manager = TaskManager(
            project_path
        )

        task = task_manager.get_next_task()


        if not task:

            print(
                "No pending tasks."
            )

            continue


        print(
            f"\nBuilding: {task['title']}"
        )


        task_manager.update_task_status(
            task["id"],
            "in_progress"
        )


        # -----------------------------------
        # Planning
        # -----------------------------------

        planner = TaskPlanner()

        project_context = inspect_project(
            project_path
        )

        plan = planner.create_plan(
            task,
            project_context
        )

        print(
            "\nPlan created."
        )


        # -----------------------------------
        # Load Fahim knowledge
        # -----------------------------------

        knowledge = fahim_knowledge.load_all()

        print(
            "\nFahim knowledge loaded."
        )

        print(
            "Knowledge sources:"
        )

        for name in knowledge:

            print(
                f"- {name}"
            )


        # -----------------------------------
        # Build coding context
        # -----------------------------------

        context_builder = CodingContextBuilder()

        coding_context = context_builder.build(
            task,
            plan,
            project_context,
            knowledge
        )

        print(
            "\nCoding context prepared."
        )

        print(
            "\nCoding context contains:"
        )

        print(
            f"- Task: "
            f"{coding_context['task']['title']}"
        )

        print(
            f"- Planned files: "
            f"{len(coding_context['plan']['files'])}"
        )

        print(
            "- Project context: loaded"
        )

        print(
            "- Fahim knowledge: loaded"
        )


        # -----------------------------------
        # Reasoning
        # -----------------------------------

        reasoning_engine = ReasoningEngine()

        reasoning_result = reasoning_engine.reason(
            coding_context
        )

        print(
            "\nReasoning result:"
        )

        print(
            json.dumps(
                reasoning_result,
                indent=2
            )
        )


        # -----------------------------------
        # Code generation
        # -----------------------------------

        code_generator = CodeGenerator()

        generation_result = code_generator.generate(
            coding_context,
            reasoning_result
        )

        print(
            "\nCode generation:"
        )

        print(
            generation_result["message"]
        )

        if generation_result["success"]:

            print(
                "\nGenerated code:"
            )

            print(
                generation_result["code"]
            )

        continue


    # -----------------------------------
    # Read file
    # -----------------------------------

    if command.startswith("read "):

        target = command[
            len("read "):
        ].strip()

        parts = target.split(
            "/",
            1
        )

        if len(parts) != 2:

            print(
                "Use: read <project>/<file-path>"
            )

            continue

        project_name = parts[0]

        file_path = parts[1]

        full_path = os.path.join(
            workspace_path,
            project_name,
            file_path
        )

        try:

            content = read_file(
                full_path
            )

            print(
                "\n" + content
            )

        except FileNotFoundError:

            print(
                "File not found."
            )

        continue


    # -----------------------------------
    # Search code
    # -----------------------------------

    if command.startswith("search "):

        parts = command.split(
            " ",
            2
        )

        if len(parts) != 3:

            print(
                "Use: search <project> <text>"
            )

            continue

        project_name = parts[1]

        search_text = parts[2]

        project_path = get_project_path(
            project_name
        )

        results = search_code(
            project_path,
            search_text
        )

        if not results:

            print(
                "No matches found."
            )

        else:

            for result in results:

                print(
                    f"{result['file']}:"
                    f"{result['line']} - "
                    f"{result['content']}"
                )

        continue


    # -----------------------------------
    # Create project
    # -----------------------------------

    if command.startswith(
        "create project "
    ):

        project_name = command[
            len("create project "):
        ].strip()

        result = project_manager.create_project(
            project_name
        )

        if result["success"]:

            print(
                f"Project created: "
                f"{result['path']}"
            )

        else:

            print(
                f"Failed: "
                f"{result['reason']}"
            )

        continue


    # -----------------------------------
    # Create file
    # -----------------------------------

    if command.startswith(
        "create file "
    ):

        target = command[
            len("create file "):
        ].strip()

        parts = target.split(
            "/",
            1
        )

        if len(parts) != 2:

            print(
                "Use: create file "
                "<project>/<file-path>"
            )

            continue

        project_name = parts[0]

        file_path = parts[1]

        full_path = os.path.join(
            workspace_path,
            project_name,
            file_path
        )

        result = create_file(
            full_path
        )

        if result["success"]:

            print(
                f"File created: "
                f"{result['path']}"
            )

        else:

            print(
                f"Failed: "
                f"{result['reason']}"
            )

        continue


    # -----------------------------------
    # Edit file
    # -----------------------------------

    if command.startswith("edit "):

        target = command[
            len("edit "):
        ].strip()

        parts = target.split(
            "/",
            1
        )

        if len(parts) != 2:

            print(
                "Use: edit <project>/<file-path>"
            )

            continue

        project_name = parts[0]

        file_path = parts[1]

        full_path = os.path.join(
            workspace_path,
            project_name,
            file_path
        )

        print(
            "Enter file content."
        )

        print(
            "Type END on a new line when finished."
        )

        lines = []

        while True:

            line = input()

            if line == "END":
                break

            lines.append(line)

        content = "\n".join(
            lines
        )

        result = edit_file(
            full_path,
            content
        )

        if result["success"]:

            print(
                f"File updated: "
                f"{result['path']}"
            )

        else:

            print(
                f"Failed: "
                f"{result['reason']}"
            )

        continue


    # -----------------------------------
    # Run command
    # -----------------------------------

    if command.startswith("run "):

        parts = command.split(
            " ",
            2
        )

        if len(parts) != 3:

            print(
                "Use: run <project> <command>"
            )

            continue

        project_name = parts[1]

        project_command = parts[2]

        project_path = get_project_path(
            project_name
        )

        result = run_command(
            project_path,
            project_command
        )

        print("\nOutput:")

        print(
            result["stdout"]
        )

        if result["stderr"]:

            print("\nErrors:")

            print(
                result["stderr"]
            )

        print(
            f"\nReturn code: "
            f"{result['return_code']}"
        )

        continue


    # -----------------------------------
    # Exit
    # -----------------------------------

    if command == "exit":

        print(
            "Fahim Coding Agent closed."
        )

        break


    # -----------------------------------
    # Unknown command
    # -----------------------------------

    print(
        "Unknown command. "
        "Type 'help' to see available commands."
    )