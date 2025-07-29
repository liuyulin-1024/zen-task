import os
from importlib import import_module


async def register_routers():
    from main import app

    prefix_directory_mappings = {
        "api": "api",
    }
    for api_prefix, folder_prefix in prefix_directory_mappings.items():
        for folder_name in os.listdir(folder_prefix):
            if not os.path.isdir(os.path.join(folder_prefix, folder_name)):
                continue

            directory = os.path.join(folder_prefix, folder_name)
            for name in os.listdir(directory):
                if not os.path.isfile(os.path.join(directory, name)):
                    continue
                if "views" not in name:
                    continue

                views_name, *_ = name.split(".")
                views = import_module(f"{folder_prefix}.{folder_name}.{views_name}")
                if hasattr(views, "router"):
                    app.include_router(
                        getattr(views, "router"),
                        prefix=f"/{api_prefix}/{folder_name}",
                        tags=[folder_name],
                    )
