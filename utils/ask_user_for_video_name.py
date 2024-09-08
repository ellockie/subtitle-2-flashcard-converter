def ask_user_for_video_name(default_folder_name):
    if default_folder_name:
        prompt = f"Enter a video name (default: {default_folder_name}): "
    else:
        prompt = f"Enter a video name: "
    try:
        video_name = input(prompt).strip().replace("	", ". ")
        return video_name
    except EOFError:
        print(
            f"Running in non-interactive environment. Using default folder name: {default_folder_name}"
        )
        raise EOFError
