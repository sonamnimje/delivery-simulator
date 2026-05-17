def build_prompt(situation: str = None, mood: str = None, *, regenerate_scene: dict | None = None) -> str:
    base = (
        "You are a screenwriter for absurd, overdramatic cinematic pieces. "
        "Respond with JSON ONLY matching the requested schema — no explanation, no markdown. "
    )

    cinematic_instructions = (
        "Use exaggerated emotions, slow-motion moments, crowd reactions, cinematic narration, "
        "mass hero entries, interval moments, and funny over-the-top dialogues. "
        "Make it vivid, absurd, and delightfully dramatic. "
    )

    schema = (
        "JSON schema: movie_title, tagline, characters (array of {name, role, description}), "
        "scenes (array of {scene_index:int, scene_title, mood, scene_description, dialogues:[{character,line}] })."
    )

    if regenerate_scene:
        # regenerate a single scene within an existing drama
        scene_index = regenerate_scene.get("scene_index")
        scene_context = regenerate_scene.get("scene_context")
        prompt = (
            f"{base}{cinematic_instructions}\n" 
            f"Regenerate only scene {scene_index} of the drama described below. "
            "Return ONLY the scene object as JSON (not the full drama) with keys: "
            "scene_index, scene_title, mood, scene_description, dialogues (array of {character,line}). "
            "Keep style consistent with the original drama and the requested mood. "
            f"Original scene context:\n{scene_context}\n"
        )
        return prompt

    # full drama generation
    prompt = (
        f"{base}{cinematic_instructions}\nSituation: {situation}\nMood: {mood}\n{schema}"
    )
    return prompt
